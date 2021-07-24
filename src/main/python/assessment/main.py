import sys
import click
import logging
from os import path, pardir

# MultiProcessing imports
import threading, multiprocessing
import queue
import csv

# Local imports
sys.path.append(path.abspath(path.join(path.dirname(__file__), pardir)))
from common.dummy_ai import getCompanyAttractiveness

# Logger definition
logging.basicConfig(format="%(message)s", level=logging.INFO)

# Getting cpu count
cpu_count = multiprocessing.cpu_count()

# Queues definition
waitingQueue = queue.Queue()
resultQueue = queue.Queue()

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
@click.option(
    "--threads",
    default= cpu_count,
    help="Number of threads to use."
)
def main(filename: str, threads: int, top=10) -> None:
    """
    Args:
        filename (str): Input CSV file name
        top (int, optional): Number of companies Symbols to print at the end. Defaults to 10.
    """
    # loading data from csv file
    data = csv.DictReader(open(filename))

    # puting data in waitingQueue to be processed
    for row in data:
        waitingQueue.put(row["Symbol"])

    # creating threads
    threadList=[]
    for index in range(threads):
        thread = threading.Thread(
            target=runner, 
            args=(
                index,
                getCompanyAttractiveness,
                )
            )
        threadList.append(thread)

    # starting threads
    for thread in threadList:
        thread.start()

    # waiting for threads to finish processing data
    for thread in threadList:
        thread.join()
    
    # sorting data processing result by the score of Company Attractiveness in descending order
    sortedResults = sorted(
        resultQueue.queue, 
        key=lambda result: result["score"], 
        reverse=True
        )
    
    # keeping top results only
    topResults = sortedResults[:top]
    
    logging.info(topResults)
    
def runner(id, task):

    global waitingQueue, resultQueue

    logging.info(f"runner {id} starting now")

    while not waitingQueue.empty():
        # pickup data
        data = waitingQueue.get() 
        # run task on data
        result = task(data) 
        # store task result
        resultQueue.put(result) 
    
    logging.info(f"runner {id} finished processing")


if __name__ == "__main__":
    main()