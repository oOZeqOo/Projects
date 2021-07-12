import requests
import json
import csv
import pprint
from jobs_scraper import JobsScraper
from stackoverflow import scrape_linkedin
from indeed import scrape_indeed

from datetime import datetime

WANTED_TAGS = ["python"]


def get_jobs(
    position,
    location=None,
    print_out=False,
    remote=False,
    tags=None,
    linkedin=False,
    indeed=False,
):
    list_of_jobs = []
    print("Starting job search")

    if indeed:
        print("Searching Indeed.com")
        start = datetime.now()
        list_of_jobs += scrape_indeed(position, location, "7", print_out=False)
        end = datetime.now()
        elapsed_time = (end - start).seconds
        print(f"Completed the search Indeed.com in {elapsed_time}s")

    if linkedin:
        print("Searching LinkedIn.com")
        start = datetime.now()
        list_of_jobs += scrape_linkedin(
            position,
            location=location,
            print_out=print_out,
            remote=remote,
            tags=tags,
        )
        end = datetime.now()
        elapsed_time = (end - start).seconds
        print(f"Completed the search LinkedIn.com in {elapsed_time}s")

    print("Completed Job search\nWriting to an Excel file")

    start = datetime.now()
    write_jobs(list_of_jobs)
    end = datetime.now()
    elapsed_time = (end - start).seconds
    print(f"Finished writing jobs in {elapsed_time}s")
    return


def write_jobs(list_of_jobs):
    with open("JobPostScraper/results.csv", "w+", newline="", encoding="utf-8") as f:
        keys = list_of_jobs[0].keys()
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_jobs)


if __name__ == "__main__":
    get_jobs(
        "python programmer",
        location="San Antonio",
        tags=WANTED_TAGS,
        linkedin=True,
        indeed=True,
    )
