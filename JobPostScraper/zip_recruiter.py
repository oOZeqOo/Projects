import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from html5print import HTMLBeautifier

template = "https://www.ziprecruiter.com/search?form=jobs-landing&search={}&location={}"
card_identifier = "job_content"
list_of_jobs = []


def get_url(position, location):
    return f"https://www.ziprecruiter.com/search?form=jobs-landing&search={position}&l={location}"


def scrape_zip_recruiter(position, location, print_out=False):
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.body.find_all("div", "inner ")
        print(cards)
        return
        for card in cards:
            curr_job = get_record(card)
            list_of_jobs.append(curr_job)
        try:
            url = "https://www.indeed.com" + soup.find("a", {"aria-label": "Next"}).get(
                "href"
            )
        except AttributeError:
            break

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


def get_record(card, url="https://www.indeed.com"):
    curr_job = {}

    curr_job["Link"] = url + card.get("href")
    title = card.find("h2", "jobTitle").find_all("span")
    if len(title) > 1:
        title = title[1]
    else:
        title = title[0]

    curr_job["Title"] = title.text

    company = card.find("span", "companyName")
    # print(company)
    if company.a:
        company = company.a
    curr_job["Company"] = company.text

    curr_job["Location"] = card.find("div", "companyLocation").get_text()

    curr_job["Date"] = card.find("span", "date").text

    salary = card.find("span", "salary-snippet")
    if salary:
        salary = salary.text

    curr_job["Salary"] = salary

    rating = card.find("span", "ratingNumber")
    if rating:
        rating = rating.get_text("aria-label")
    curr_job["Rating"] = rating

    description_list = card.find("div", "job-snippet").ul
    description = ""
    for item in description_list.find_all("li"):
        description += item.text + "\n\t\t"

    curr_job["Description"] = description.rstrip(",")
    return curr_job


if __name__ == "__main__":
    scrape_zip_recruiter("python programmer", "San Antonio, TX", print_out=True)
