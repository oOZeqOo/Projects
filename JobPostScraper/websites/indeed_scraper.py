import requests

from bs4 import BeautifulSoup
from websites.progress_bar import progressBar

template = "https://www.indeed.com/jobs?q={}&l={}"
card_identifier = "tapItem"
list_of_jobs = []


def get_url(position, location, radius):
    return f"https://www.indeed.com/jobs?q={position}&l={location}&radius={radius}"


def scrape_indeed(position, location, radius, print_out=False):
    url = get_url(position, location, radius)

    page = 1
    while True:

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("a", card_identifier)
        number_of_pages = int(soup.find_all("span", "pn")[-2].text)
        if page > number_of_pages:
            page = number_of_pages
        progressBar(page, number_of_pages)
        for card in cards:
            curr_job = get_record(card)
            list_of_jobs.append(curr_job)
        try:
            url = "https://www.indeed.com" + soup.find("a", {"aria-label": "Next"}).get(
                "href"
            )
        except AttributeError:
            break
        page += 1
    print("\n")
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

    return list_of_jobs


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
    if description_list is not None:
        for item in description_list.find_all("li"):
            description += item.text + "\n\t\t"

    curr_job["Description"] = description.rstrip(",")
    return curr_job


if __name__ == "__main__":
    scrape_indeed("python", "San Antonio, TX", "7", print_out=False)
