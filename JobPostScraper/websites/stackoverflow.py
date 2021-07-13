import requests
import tqdm
import sys

from bs4 import BeautifulSoup
from pprint import pprint
from progress_bar import progressBar

# tl = tags separated by '+'
template = "https://stackoverflow.com/jobs?q={}&r={}&tl={}&l={}"
card_identifier = "js-result"
list_of_jobs = []


def get_url(position, location=None, tags=None, remote=False):
    url = f"https://stackoverflow.com/jobs?q={position}"
    if remote:
        url += f"&r={remote}"

    url += add_var_to_path(tags, "&tl=")
    url += add_var_to_path(location, "&l=")

    return url


def add_var_to_path(words, tag):
    if words is None or len(words) < 1:
        return ""
    if isinstance(words, str):
        words = words.replace(",", "").split(" ")

    fixed_path = tag
    for word in words[:-1]:
        fixed_path += word + "+"
    fixed_path += words[-1]

    return fixed_path


def scrape_stackoverflow(
    position, location=None, print_out=False, remote=False, tags=None
):
    url = get_url(position, location=location, tags=tags, remote=remote)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", card_identifier)
    number_of_pages = soup.find_all("a", "s-pagination--item")[-2].span.text
    print(f"Found {number_of_pages} pages to look through")
    page = 1
    while True:
        progressBar(page, int(number_of_pages))
        count = 1
        for card in cards:
            curr_job = get_record(card)
            list_of_jobs.append(curr_job)
            count += 1
        try:
            a = soup.find_all("a", "s-pagination--item")[-1]

            if a.span.text == "next":
                url = "https://stackoverflow.com" + a.get("href")
            else:
                break
        except IndexError:
            break
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", card_identifier)
        page += 1

    print(f"\nFound {len(list_of_jobs)} potential jobs")
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


def get_record(card, url="https://stackoverflow.com"):
    curr_job = {}

    curr_job["Link"] = url + card.find("a", "s-link stretched-link").get("href")
    curr_job["Title"] = card.find("a", "s-link stretched-link").get("title")
    curr_job["Company"] = (
        card.find("h3", "fc-black-700 fs-body1 mb4")
        .span.text.rstrip(" ")
        .replace("\r", "")
        .replace("\n", "")
    )
    curr_job["Location"] = (
        card.find("span", "fc-black-500")
        .text.rstrip(" ")
        .replace("\r", "")
        .replace("\n", "")
    )

    ul = card.find("ul", "mt4 fs-caption fc-black-500 horizontal-list")

    for li in ul.find_all("li"):
        if (
            "Salary" not in curr_job
            and li.has_attr("title")
            and "Dollars" in li.get("title")
        ):
            curr_job["Salary"] = li.get("title")
        elif "Date" not in curr_job and li.span and "d ago" in li.span.text:
            curr_job["Date"] = li.span.text

    if "Date" not in curr_job:
        curr_job["Date"] = None

    if "Salary" not in curr_job:
        curr_job["Salary"] = None

    curr_job["Rating"] = None
    curr_job["Description"] = None

    return curr_job


if __name__ == "__main__":
    scrape_stackoverflow(
        "python programmer",
        location="San Antonio, TX",
        print_out=False,
        remote=True,
        tags=["python"],
    )
