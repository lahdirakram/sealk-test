import sys
import click
import logging
from os import path, pardir

# MultiProcessing imports
import multiprocessing
import csv

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
    default=10,
    help="Number of companies Symbols to print at the end"
)
@click.option(
    "--threads",
    default=multiprocessing.cpu_count(),
    help="Number of threads to use."
)
def main(filename: str, threads: int, top=10) -> None:
    """
    Args:
        filename (str): Input CSV file name
        top (int, optional): Number of companies Symbols to print at the end. Defaults to 10.
    """
    # loading data from csv file
    data = [row['Symbol'] for row in csv.DictReader(open(filename))]

    # creating a pool of processes
    pool = multiprocessing.Pool(processes=threads)

    # launching multiprocessing on data with paralel threads  
    results = pool.map(getCompanyAttractiveness, data)
    
    # sorting data processing result by the score of Company Attractiveness in descending order
    sortedResults = sorted(
        results, 
        key=lambda result: result["score"], 
        reverse=True
        )
    
    # keeping top results only
    topResults = sortedResults[:top]
    
    logging.info(topResults)
    
if __name__ == "__main__":
    main()