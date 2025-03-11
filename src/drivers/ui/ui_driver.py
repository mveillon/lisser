import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd

import sys
from datetime import datetime, date
from os import walk
from os.path import join, relpath, splitext, exists
from zipfile import ZipFile
import traceback as tb
import re

from typing import cast, Dict, Any, Callable

from src.analyze_spending import analyze_spending
from src.read_data.read_data import read_data
from src.models.paths import Paths, ALLOWED_EXTNS
from src.read_data.column import Column
from src.read_data.write_data import write_data

from src.drivers.ui.styling import ColorScheme, FONT, PADDING
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

        self.config(bg=ColorScheme.BACKGROUND)
        self.title("Spending Tracking")

        self._add_title_frame()

        self.lower_frame = frame(self, with_hightlight=False)
        self.lower_frame.grid(padx=PADDING, pady=PADDING, row=1, column=0)

        self._add_input_frame()
        if exists(Paths.spending_path()):
            self._add_output_frame()

    def _add_title_frame(self) -> None:
        """
        Adds the title frame part of the UI.
        """
        self.title_frame = frame(self)
        self.title_frame.grid(padx=PADDING, pady=PADDING, row=0, column=0)

        self.title_label = label(self.title_frame, "Spending Tracking")
        self.title_label.config(font=(FONT[0], FONT[1] + 4))
        self.title_label.grid(
            padx=PADDING, pady=(PADDING, PADDING / 2), row=0, column=0
        )

        self.info_label = label(self.title_frame, "Awaiting data...")
        self.info_label.grid(padx=PADDING, pady=PADDING / 2, row=1, column=0)

        self.quit_button = button(self.title_frame, "Quit", self.quit)
        self.quit_button.grid(
            padx=PADDING, pady=(PADDING / 2, PADDING), row=2, column=0
        )

    def _add_input_frame(self) -> None:
        """
        Adds the input frame part of the UI.
        """
        self.input_frame = frame(self.lower_frame)
        self.input_frame.grid(padx=PADDING, pady=PADDING, row=0, column=0)

        self.analyze_prompt = label(
            self.input_frame, "Select a spreadsheet to analyze:"
        )
        self.analyze_prompt.grid(
            padx=PADDING, pady=(PADDING, PADDING / 2), row=0, column=0
        )

        self.spending_sheet = button(self.input_frame, "Select file", self.file_handler)
        self.spending_sheet.grid(
            padx=PADDING, pady=(PADDING / 2, PADDING), row=1, column=0
        )

    def _add_output_frame(self) -> None:
        """
        Adds the output frame part of the UI.
        """
        self.output_frame = frame(self.lower_frame)
        self.output_frame.grid(padx=PADDING, pady=PADDING, row=0, column=1)

        self.fmt = "%m/%d/%Y"

        self.transaction_prompt = label(
            self.output_frame, "Add a transaction to an existing spreadsheet:"
        )
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
            self.output_frame, "Add transaction", self.transaction_handler
        )
        self.transaction_submit.grid(padx=PADDING, pady=PADDING, row=2, column=2)

    def quit(self) -> None:
        """
        Quits the application.

        Parameters:
            None

        Returns:
            None
        """
        self.destroy()
        sys.exit(0)

    def file_handler(self, path: str = ".") -> None:
        """
        Processes the files and creates the plots and aggregations.

        Parameters:
            path (str): the path to the spreadsheet

        Returns:
            None
        """
        self.info_label.config(text="...processing data...")
        refs = fd.askopenfilename(
            parent=self,
            title="Spreadsheet to analyze:",
            initialdir=path,
            filetypes=(("spreadsheets", ["*" + e for e in ALLOWED_EXTNS]),),
        )

        try:
            df = read_data(refs)
            new_year = cast(datetime, df[Column.DATE].median()).year
            Paths._year_mut[0] = new_year
            Paths._sheet_override[0] = refs

            analyze_spending(verbose=False)
        except Exception as e:
            self.info_label.config(text=f"Something went wrong: {str(e)}")
            print(tb.format_exc())
            return

        self.info_label.config(text="Processing complete! Archiving data...")

        try:
            out_name = fd.asksaveasfilename(
                filetypes=[("Archive Files", "*.zip")], defaultextension=".zip"
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
            self.info_label.config(
                text=f"Something went wrong saving the zip file: {e}"
            )
            print(tb.format_exc())
            return

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
        self.info_label.config(text=f"Transaction added to {Paths.spending_path()}")

        for col, var in self.transaction_vars.items():
            var.set(self.defaults.get(cast(Column, col), ""))
