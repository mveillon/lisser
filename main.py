import sys

from src.analyze_spending import AnalyzeSpending
from src.initialize import initialize
from src.utilities.parse_args import parse_args, Subcommand

if __name__ == "__main__":
    cmd = parse_args().subparser_name
    if cmd == Subcommand.INIT:
        initialize()
    elif cmd == Subcommand.CLI:
        AnalyzeSpending.analyze_spending()
    elif cmd == Subcommand.UI:
        AnalyzeSpending().mainloop()
    else:
        raise ValueError(f"Invalid subcommand {sys.argv[1]}")
