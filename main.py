from bs4 import BeautifulSoup
import requests
import json


URL = "https://quotes.toscrape.com"
FILE_QUOTES = "quotes.json"
FILE_AUTHORS = "authors.json"


def get_about_author(link_about: str) -> tuple[str, ...]:
    response = requests.get(f"{URL}{link_about}")
    author_born_date = ""
    author_born_location = ""
    description = ""
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        author_born_date = soup.find("span", class_="author-born-date").text.strip()
        author_born_location = soup.find("span", class_="author-born-location").text.strip()
        description = soup.find("div", class_="author-description").text.strip()
    return author_born_date, author_born_location, description


def parse_data() -> tuple[list, list]:
    result_authors = []
    result_quotes = []
    num_page = 1
    while True:
        response = requests.get(f"{URL}/page/{num_page}/")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            div_quotes = soup.find_all('div', class_='quote')
            for div_quote in div_quotes:
                tags = []
                quote = div_quote.find("span", class_="text").text
                author = div_quote.find("small", class_="author").text
                link_about = div_quote.find("a").get("href")
                born, location, description = get_about_author(link_about)
                a_tags = div_quote.find("div", class_="tags").find_all("a")
                for a_tag in a_tags:
                    tags.append(a_tag.text)
                result_authors.append({"fullname": author,
                                       "born_date": born,
                                       "born_location": location,
                                       "description": description})
                result_quotes.append({"tags": tags,
                                      "author": author,
                                      "quote": quote})
            button_next = soup.find('li', class_='next')
            if button_next is None:
                return result_authors, result_quotes

        else:
            print("Not found")
        num_page += 1


def run():
    authors, quotes = parse_data()
    save_to_file(authors, quotes)


def save_to_file(authors: list, quotes: list):
    with open(FILE_AUTHORS,"w") as file:
        json.dump(authors, file, indent=4)
    with open(FILE_QUOTES,"w") as file:
        json.dump(quotes, file, indent=4)


if __name__ == "__main__":
    run()
