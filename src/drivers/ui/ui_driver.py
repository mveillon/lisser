import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd

from datetime import datetime, date
from os import walk, makedirs
from os.path import join, relpath, splitext, exists, abspath
from pathlib import Path
import platform

from zipfile import ZipFile
import traceback as tb
import re

from typing import cast, Dict, Any, Callable

from src.analyze_spending import analyze_spending
from src.models.paths import Paths, ALLOWED_EXTNS
from src.initialize import add_spending_sheet

from src.read_data.read_data import read_data
from src.read_data.column import Column
from src.read_data.write_data import write_data

from src.drivers.ui.styling import ColorScheme, PADDING, TITLE
from src.drivers.ui.widgets import (
    frame,
    label,
    button,
    entry,
    option_menu,
)


class UIDriver(tk.Tk):
    """
    Class to run the UI.
    """

    def __init__(self) -> None:
        super().__init__()
        if platform.system() == "Windows":
            self.state("zoomed")

        makedirs(Paths.this_years_data(), exist_ok=True)
        if not exists(Paths.spending_path()):
            add_spending_sheet()

        self.config(bg=ColorScheme.BACKGROUND)
        self.title("Spending Tracking")

        self._add_title_frame()

        self.lower_frame = frame(self, with_hightlight=False)
        self.lower_frame.grid(padx=PADDING, pady=PADDING, row=1, column=0)

        self._add_input_frame()
        self._add_output_frame()

    def _add_title_frame(self) -> None:
        """
        Adds the title frame part of the UI.
        """
        self.title_frame = frame(self)
        self.title_frame.grid(padx=PADDING, pady=PADDING, row=0, column=0)

        self.title_label = label(self.title_frame, "Spending Tracking")
        self.title_label.config(font=TITLE)
        self.title_label.grid(
            padx=PADDING, pady=(PADDING, PADDING / 2), row=0, column=0
        )

        self.filename_label = label(
            self.title_frame, self.filename_text(Paths.spending_path())
        )
        self.filename_label.grid(padx=PADDING, pady=PADDING / 2, row=1, column=0)

        self.info_label = label(self.title_frame, "")
        self.info_label.grid(padx=PADDING, pady=PADDING / 2, row=2, column=0)

        self.quit_button = button(self.title_frame, "Quit", self.quit)
        self.quit_button.grid(
            padx=PADDING, pady=(PADDING / 2, PADDING), row=3, column=0
        )

    def _add_input_frame(self) -> None:
        """
        Adds the input frame part of the UI.
        """
        self.input_frame = frame(self.lower_frame)
        self.input_frame.grid(padx=PADDING, pady=PADDING, row=0, column=0)

        self.analyze_prompt = label(self.input_frame, "Analyze Data")
        self.analyze_prompt.config(font=TITLE)
        self.analyze_prompt.grid(
            padx=PADDING, pady=(PADDING, PADDING / 2), row=0, column=0
        )

        self.new_path_button = button(self.input_frame, "Change path", self.change_path)
        self.new_path_button.grid(padx=PADDING, pady=PADDING / 2, row=1, column=0)

        self.analyze_button = button(
            self.input_frame, "Start analysis", self.file_handler
        )
        self.analyze_button.grid(
            padx=PADDING, pady=(PADDING / 2, PADDING), row=2, column=0
        )

    def _add_output_frame(self) -> None:
        """
        Adds the output frame part of the UI.
        """
        self.output_frame = frame(self.lower_frame)
        self.output_frame.grid(padx=PADDING, pady=PADDING, row=0, column=1)

        self.fmt = "%m/%d/%Y"

        self.transaction_prompt = label(self.output_frame, "Add Transaction")
        self.transaction_prompt.config(font=TITLE)
        self.transaction_prompt.grid(
            padx=PADDING,
            pady=(PADDING, PADDING / 2),
            row=0,
            column=0,
        )

        self.transaction_vars: Dict[str, tk.StringVar] = {}
        self.transaction_labels: Dict[str, tk.Label] = {}
        self.transaction_entries: Dict[str, tk.Entry | tk.OptionMenu] = {}

        df = read_data(Paths.spending_path())
        dropdowns = {Column.IS_FOOD, Column.CONTROLLABLE}
        self.defaults = {
            Column.DATE: date.today().strftime(self.fmt),
            Column.IS_FOOD: "False",
            Column.CONTROLLABLE: "False",
        }
        col_names = [col for col in df.columns.tolist() if col != Column.TRANSACTION_ID]

        self.transaction_frames = [
            frame(self.output_frame, with_hightlight=False),
            frame(self.output_frame, with_hightlight=False),
        ]
        self.transaction_frames[0].grid(
            padx=(PADDING, PADDING / 2),
            pady=(PADDING / 2, PADDING),
            row=1,
            column=0,
        )
        self.transaction_frames[1].grid(
            padx=(PADDING, PADDING / 2),
            pady=(PADDING / 2, PADDING),
            row=1,
            column=1,
        )

        for i, col in enumerate(col_names):
            frame_ind = i & 1
            self.transaction_vars[col] = tk.StringVar(
                self.transaction_frames[frame_ind],
                value=self.defaults.get(cast(Column, col), ""),
            )

            self.transaction_labels[col] = label(
                self.transaction_frames[frame_ind], col
            )
            self.transaction_labels[col].grid(
                padx=PADDING, pady=PADDING / 2, row=i, column=0
            )

            if col in dropdowns:
                self.transaction_entries[col] = option_menu(
                    self.transaction_frames[frame_ind],
                    self.transaction_vars[col],
                    ["True", "False"],
                )
            else:
                self.transaction_entries[col] = entry(
                    self.transaction_frames[frame_ind],
                    self.transaction_vars[col],
                )
            self.transaction_entries[col].grid(
                padx=PADDING, pady=PADDING / 2, row=i + 1, column=0
            )

        self.transaction_submit = button(
            self.output_frame, "Submit", self.transaction_handler
        )
        self.transaction_submit.grid(padx=PADDING, pady=PADDING, row=2, column=2)

    def change_path(self) -> None:
        """
        Changes the path to point the UI at.

        Parameters:
            None

        Returns:
            None
        """
        refs = fd.askopenfilename(
            parent=self,
            title="Spreadsheet to analyze:",
            initialdir=Paths.this_years_data(),
            filetypes=(("spreadsheets", ["*" + e for e in ALLOWED_EXTNS]),),
        )

        try:
            df = read_data(refs)
            new_year = cast(datetime, df[Column.DATE].median()).year
            Paths._year_mut[0] = new_year
            Paths._sheet_override[0] = refs
            self.filename_label.config(text=self.filename_text(Paths.spending_path()))

        except Exception as e:
            self.error(str(e))

    def file_handler(self) -> None:
        """
        Processes the files and creates the plots and aggregations.

        Parameters:
            None

        Returns:
            None
        """
        self.info_label.config(text="...processing data...")
        analyze_spending(verbose=False)

        self.info_label.config(text="Processing complete! Archiving data...")

        try:
            out_name = fd.asksaveasfilename(
                filetypes=[("Archive Files", "*.zip")],
                defaultextension=".zip",
                initialdir=str(Path(Paths.spending_path()).parent),
            )

            with ZipFile(out_name, "w") as archive:

                def add_file(add_path: str) -> None:
                    archive_path = relpath(add_path, Paths.this_years_data())
                    archive.write(add_path, archive_path)

                add_file(Paths.aggregation_path())

                for dir_path, _, file_names in walk(Paths.this_years_data()):
                    for file in file_names:
                        if splitext(file)[1] not in ALLOWED_EXTNS:
                            add_file(join(dir_path, file))

            self.info_label.config(text="Archive created!")

        except Exception as e:
            self.error(str(e))

    def transaction_handler(self) -> None:
        """
        Validates and writes transaction input.

        Parameters:
            None

        Returns:
            None
        """
        flag_converter = lambda s: 1 if s == "True" else 0
        converters: Dict[str, Callable[[str], Any]] = {
            Column.DATE: lambda s: datetime.strptime(s, self.fmt).date(),
            Column.PRICE: lambda s: float(re.sub(r"[^\d\-.]", "", s)),
            Column.IS_FOOD: flag_converter,
            Column.CONTROLLABLE: flag_converter,
        }
        cols: Dict[str, Any] = {}

        for col, var in self.transaction_vars.items():
            val = self.transaction_vars[col].get()
            try:
                cols[col] = [converters.get(col, lambda s: s)(val)]
            except ValueError:
                self.info_label.config(text=f"Invalid value for {col}: '{val}'")
                return

        Paths._year_mut[0] = cols[Column.DATE][0].year
        write_data(pd.DataFrame(cols), Paths.spending_path(), mode="a")
        self.info_label.config(text="Transaction added!")

        for col, var in self.transaction_vars.items():
            var.set(self.defaults.get(cast(Column, col), ""))

    def error(self, message: str) -> None:
        """
        Raises an error gracefully without closing the application.

        Parameters:
            message (str): the message to display

        Returns:
            None
        """
        self.info_label.config(text=f"Something went wrong: {message}")
        print(tb.format_exc())

    def filename_text(self, path: str) -> str:
        """
        Creates what the filename label should say.

        Parameters:
            path (str): the new path

        Returns:
            None
        """
        return f"Currently pointing at {abspath(path)}"
