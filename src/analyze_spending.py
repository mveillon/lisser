import tkinter as tk
from tkinter import filedialog as fd

from datetime import datetime
from shutil import copyfile
from os import walk
from os.path import abspath, join, relpath, splitext
from zipfile import ZipFile

from typing import cast

from src.visualization_driver import VisualizationDriver
from src.aggregation_driver import AggregationDriver
from src.utilities.read_data import read_data
from src.utilities.paths import Year, spending_path, this_years_data, aggregation_path
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

    def file_handler(self, path: str) -> None:
        """
        Processes the files and creates the plots and aggregations.

        Parameters:
            path (str): the path to the spreadsheet

        Returns:
            None
        """
        self.output_label.config(text="...processing data...")
        refs = fd.askopenfilename(
            parent=self,
            title="Spreadsheet to analyze:",
            initialdir=path,
            filetypes=(("spreadsheets", "*.txt *.csv *.xlsx *.numbers"),),
        )

        df = read_data(refs)
        Year.year = cast(datetime, df[Column.DATE].median()).year
        if abspath(refs) != abspath(spending_path()):
            copyfile(refs, spending_path())
        AnalyzeSpending.analyze_spending(verbose=False)

        self.output_label.config(text="Processing complete!")

        out_name = fd.asksaveasfilename(filetypes=[("Archive Files", "*.zip")], defaultextension=".zip")
        
        skip_extns = {
            ".csv",
            ".txt",
            ".xlsx",
            ".numbers",
        }
        with ZipFile(out_name, "w") as archive:
            archive.write(aggregation_path(), ".")

            for dir_path, _, file_names in walk(this_years_data()):
                for file in file_names:
                    if splitext(file)[1] not in skip_extns:
                        full_path = join(dir_path, file)
                        archive_path = relpath(full_path, this_years_data())
                        archive.write(full_path, archive_path)

        

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
