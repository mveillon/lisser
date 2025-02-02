from src.analyze_spending import AnalyzeSpending
from src.utilities.parse_args import parse_args

if __name__ == "__main__":
    if parse_args().tkinter:
        AnalyzeSpending().mainloop()
    else:
        AnalyzeSpending.analyze_spending()
