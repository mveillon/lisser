import sys

from src.analyze_spending import AnalyzeSpending
from src.initialize import initialize
from src.utilities.parse_args import Subcommand, get_subcommand

if __name__ == "__main__":
    cmd = get_subcommand()
    if cmd == Subcommand.INIT:
        initialize()
    elif cmd == Subcommand.CLI:
        AnalyzeSpending.analyze_spending()
    elif cmd == Subcommand.UI:
        AnalyzeSpending().mainloop()
    else:
        # raise ValueError(f"Invalid subcommand {sys.argv[1]}")
        print("Doing nothing")
