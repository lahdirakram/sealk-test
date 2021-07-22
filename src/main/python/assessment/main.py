import sys
import click
import logging
from os import path, pardir
import threading, queue, csv

# Local imports
sys.path.append(path.abspath(path.join(path.dirname(__file__), pardir)))
from common.dummy_ai import getCompanyAttractiveness

# Logger definition
logging.basicConfig(format="%(message)s", level=logging.INFO)

@click.command()
@click.option(
    "--filename",
    default="nasdaq-company-list.csv",
    help="Input CSV file name"
)
@click.option(
    "--top",
    default=50,
    help="Number of companies Symbols to print at the end"
)

@click.option(
    "--threads",
    default=8,
    help="Number of threads to use"
)
def main(filename: str, threads: int, top=10) -> None:
    """
    Args:
        filename (str): Input CSV file name
        top (int, optional): Number of companies Symbols to print at the end. Defaults to 10.
    """
    fileContent = list(csv.DictReader(open(filename)))

    for row in fileContent:
        waitingQueue.put(row["Symbol"])

    threadsList=[]
    for _ in range(threads):
        threadsList.append(threading.Thread(target=computingRunner))
    for th in threadsList:
        th.start()
    for th in threadsList:
        th.join()

    sortedResults = sorted(
        resultQueue.queue, 
        key=lambda result: result["score"], 
        reverse=True
        )

    toPrint = ", ".join(
        [result["id"] for result in sortedResults[:top]]
        )

    logging.info(toPrint)

def computingRunner():

    global waitingQueue, resultQueue

    while not waitingQueue.empty():
        symbole = waitingQueue.get()
        ca = getCompanyAttractiveness(symbole) 
        resultQueue.put(ca)


if __name__ == "__main__":

    waitingQueue = queue.Queue()
    resultQueue = queue.Queue()
    main()
