import tkinter as tk
from tkinter import filedialog as fd

import sys
from datetime import datetime
from os import walk
from os.path import join, relpath, splitext
from zipfile import ZipFile
import traceback as tb

from typing import cast

from src.visualization_driver import VisualizationDriver
from src.aggregation_driver import AggregationDriver
from src.utilities.read_data import read_data
from src.utilities.paths import Paths
from src.utilities.column import Column


class AnalyzeSpending(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        width = 600
        height = 300

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.spending_sheet = tk.Button(self, text="Select spreadsheet to analyze:")
        self.spending_sheet.config(
            command=lambda path=".": self.file_handler(path)  # type: ignore
        )
        self.spending_sheet.place(x=width / 2, y=height / 2)
        self.spending_sheet.pack()

        self.output_label = tk.Label(self, text="Awaiting data.")
        self.output_label.pack()

        def exit() -> None:
            self.destroy()
            sys.exit(0)

        self.quit_button = tk.Button(self, text="Quit", command=exit)
        self.quit_button.pack()

    def file_handler(self, path: str) -> None:
        """
        Processes the files and creates the plots and aggregations.

        Parameters:
            path (str): the path to the spreadsheet

        Returns:
            None
        """
        allowed_extns = {
            ".csv",
            ".txt",
            ".xlsx",
            ".numbers",
        }
        self.output_label.config(text="...processing data...")
        refs = fd.askopenfilename(
            parent=self,
            title="Spreadsheet to analyze:",
            initialdir=path,
            filetypes=(("spreadsheets", ["*" + e for e in allowed_extns]),),
        )

        try:
            df = read_data(refs)
            new_year = cast(datetime, df[Column.DATE].median()).year
            Paths._year_mut[0] = new_year
            Paths._sheet_override[0] = refs

            AnalyzeSpending.analyze_spending(verbose=False)
        except Exception as e:
            self.output_label.config(text=f"Something went wrong: {str(e)}")
            print(tb.format_exc())
            return

        self.output_label.config(text="Processing complete! Archiving data..")

        try:
            out_name = fd.asksaveasfilename(
                filetypes=[("Archive Files", "*.zip")], defaultextension=".zip"
            )

            with ZipFile(out_name, "w") as archive:
                archive.write(Paths.aggregation_path(), ".")

                for dir_path, _, file_names in walk(Paths.this_years_data()):
                    for file in file_names:
                        if splitext(file)[1] not in allowed_extns:
                            full_path = join(dir_path, file)
                            archive_path = relpath(full_path, Paths.this_years_data())
                            archive.write(full_path, archive_path)

            self.output_label.config(text="Archive created!")

        except Exception as e:
            self.output_label.config(
                text=f"Something went wrong saving the zip file: {e}"
            )
            return

    @staticmethod
    def analyze_spending(verbose: bool = True) -> None:
        """
        Runs the visualization script and performs aggregations.

        Parameters:
            verbose (bool): whether to print the time taken. Default is True

        Returns:
            None
        """
        start = datetime.now()
        VisualizationDriver().visualize()
        AggregationDriver().aggregate()
        if verbose:
            print(
                f"Completed in {round((datetime.now() - start).microseconds / 1e5, 2)}"
                + " seconds."
            )
