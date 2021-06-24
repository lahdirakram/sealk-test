import sys
import click
import logging
from os import path, pardir

# Local imports
sys.path.append(path.abspath(path.join(path.dirname(__file__), pardir)))
from common.dummy_ai import getCompanyAttractiveness

# Logger definition
logging.basicConfig(format="%(message)s", level=logging.INFO)

@click.command()
@click.option(
    "--filename",
    default="/tmp/nasdaq-company-list.csv",
    help="Input CSV file name"
)
@click.option(
    "--top",
    default=50,
    help="Number of companies Symbols to print at the end"
)
def main(filename: str, threads: int, top=10) -> None:
    """
    Args:
        filename (str): Input CSV file name
        top (int, optional): Number of companies Symbols to print at the end. Defaults to 10.
    """
    logging.info(getCompanyAttractiveness("GOOGL"))


if __name__ == "__main__":
    main()
