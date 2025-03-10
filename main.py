import sys

from src.analyze_spending import analyze_spending
from src.drivers.ui.ui_driver import UIDriver
from src.initialize import initialize
from src.utilities.parse_args import parse_args, Subcommand

if __name__ == "__main__":
    cmd = parse_args().subparser_name
    if cmd == Subcommand.INIT:
        initialize()
    elif cmd == Subcommand.CLI:
        analyze_spending()
    elif cmd == Subcommand.UI:
        UIDriver().mainloop()
    else:
        raise ValueError(f"Invalid subcommand {sys.argv[1]}")
