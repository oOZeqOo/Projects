import csv
import requests

from bs4 import BeautifulSoup
from pprint import pprint


template = "https://www.linkedin.com/jobs/search?keywords={}&location={}&vjk={}"
card_identifier = "base-card"
list_of_jobs = []


def get_url(position, location, id=None):
    if not id:
        return f"https://www.linkedin.com/jobs/search?keywords={position}&location={location}"
    return f"https://www.linkedin.com/jobs/search?keywords={position}&location={location}&vjk={id}"


def scrape_linkedin(position, location, print_out=False):
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup.prettify())
        links = soup.find_all("div", card_identifier)
        print(links[0])
        return

    if print_out:
        for job in list_of_jobs:
            print("\n===========================================")
            print("Title: ", job["Title"])
            print("Salary: ", job["Salary"])
            print("Location: ", job["Location"])
            print("Rating: ", job["Rating"])
            print("Company: ", job["Company"])
            print("Date Posted: ", job["Date"])
            print("Description: ", job["Description"])
            print("Link: ", job["Link"])
            print("\n===========================================")

    with open("JobPostScraper/results.csv", "w+", newline="", encoding="utf-8") as f:
        keys = list_of_jobs[0].keys()
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_jobs)


# Need Link, Title, Salary, Location, Rating, Company, Date Posted, Description
def get_record(card, url="https://www.indeed.com"):
    curr_job = {}

    curr_job["Link"] = url + card.get("href")

    return curr_job


if __name__ == "__main__":
    scrape_linkedin("python programmer", "San Antonio, TX", print_out=False)
