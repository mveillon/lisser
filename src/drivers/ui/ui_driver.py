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
from src.drivers.ui.color_scheme import ColorScheme


class UIDriver(tk.Tk):
    """
    Class to run the UI.
    """

    def __init__(self) -> None:
        super().__init__()

        width = 600
        height = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.padding = 10
        self.config(bg=ColorScheme.BACKGROUND)

        self._add_title_frame()
        self._add_input_frame()

        if exists(Paths.spending_path()):
            self._add_output_frame()

    def _add_title_frame(self) -> None:
        """
        Adds the title frame part of the UI.
        """
        self.title_frame = tk.Frame(
            self,
            highlightbackground=ColorScheme.ACCENT,
            highlightthickness=2,
            bg=ColorScheme.BACKGROUND,
        )
        self.title_frame.pack(padx=self.padding, pady=self.padding, side=tk.TOP)

        self.title_label = tk.Label(
            self.title_frame,
            text="Spending Tracking",
            fg=ColorScheme.TEXT,
            bg=ColorScheme.BACKGROUND,
        )
        self.title_label.pack(padx=self.padding, pady=(self.padding, self.padding / 2))

        self.info_label = tk.Label(
            self.title_frame,
            text="Awaiting data.",
            fg=ColorScheme.TEXT,
            bg=ColorScheme.BACKGROUND,
        )
        self.info_label.pack(padx=self.padding, pady=self.padding / 2)

        self.quit_button = tk.Button(
            self.title_frame,
            text="Quit",
            command=self.quit,
            fg=ColorScheme.BUTTON_TEXT,
            bg=ColorScheme.ACCENT,
        )
        self.quit_button.pack(padx=self.padding, pady=(self.padding / 2, self.padding))

    def _add_input_frame(self) -> None:
        """
        Adds the input frame part of the UI.
        """
        self.input_frame = tk.Frame(
            self,
            highlightbackground=ColorScheme.ACCENT,
            highlightthickness=2,
            bg=ColorScheme.BACKGROUND,
        )
        self.input_frame.pack(padx=self.padding, pady=self.padding, side=tk.LEFT)

        self.analyze_prompt = tk.Label(
            self.input_frame,
            text="Select a spreadsheet to analyze:",
            fg=ColorScheme.TEXT,
            bg=ColorScheme.BACKGROUND,
        )
        self.analyze_prompt.pack(
            padx=self.padding, pady=(self.padding, self.padding / 2)
        )

        self.spending_sheet = tk.Button(
            self.input_frame,
            text="Select file",
            fg=ColorScheme.BUTTON_TEXT,
            bg=ColorScheme.ACCENT,
        )
        self.spending_sheet.config(
            command=lambda path=".": self.file_handler(path)  # type: ignore
        )
        self.spending_sheet.pack(
            padx=self.padding, pady=(self.padding / 2, self.padding)
        )

    def _add_output_frame(self) -> None:
        """
        Adds the output frame part of the UI.
        """
        self.output_frame = tk.Frame(
            self,
            highlightbackground=ColorScheme.ACCENT,
            highlightthickness=2,
            bg=ColorScheme.BACKGROUND,
        )
        self.output_frame.pack(padx=self.padding, pady=self.padding, side=tk.RIGHT)

        self.fmt = "%m/%d/%Y"

        self.transaction_prompt = tk.Label(
            self.output_frame,
            text="Add a transaction to an existing spreadsheet.",
            fg=ColorScheme.TEXT,
            bg=ColorScheme.BACKGROUND,
        )
        self.transaction_prompt.pack(
            padx=self.padding, pady=(self.padding, self.padding / 2)
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
        for col in col_names:
            self.transaction_vars[col] = tk.StringVar(
                self.output_frame, value=self.defaults.get(cast(Column, col), "")
            )

            self.transaction_labels[col] = tk.Label(
                self.output_frame,
                text=col,
                fg=ColorScheme.TEXT,
                bg=ColorScheme.BACKGROUND,
            )
            self.transaction_labels[col].pack(padx=self.padding, pady=self.padding / 2)

            if col in dropdowns:
                self.transaction_entries[col] = tk.OptionMenu(
                    self.output_frame,
                    self.transaction_vars[col],
                    "True",
                    "False",
                )
                self.transaction_entries[col].config(
                    fg=ColorScheme.BUTTON_TEXT,
                    bg=ColorScheme.ACCENT,
                )
            else:
                self.transaction_entries[col] = tk.Entry(
                    self.output_frame,
                    textvariable=self.transaction_vars[col],
                    fg=ColorScheme.TEXT,
                    bg=ColorScheme.BACKGROUND,
                )
            self.transaction_entries[col].pack(padx=self.padding, pady=self.padding / 2)

        self.transaction_submit = tk.Button(
            self.output_frame,
            text="Add transaction",
            command=self.transaction_handler,
            fg=ColorScheme.BUTTON_TEXT,
            bg=ColorScheme.ACCENT,
        )
        self.transaction_submit.pack(padx=self.padding, pady=self.padding)

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

    def file_handler(self, path: str) -> None:
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
