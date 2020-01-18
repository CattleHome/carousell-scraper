import requests
import json
from bs4 import BeautifulSoup


class CarousellSearch:
    def __init__(self, url="", results=10, query=[]):
        BASE_URL = "http://sg.carousell.com/search/"
        self.url = BASE_URL

    def addQueries(self, query_string):
        self.query = query_string.split(" ")
        query = "%20".join(self.query)
        self.url += query
        print(self.url)

    def sendRequest(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')

        p_tags = soup.find_all('p')
        for tag in p_tags:
            print(tag)


if __name__ == "__main__":
    c = CarousellSearch()
    c.addQueries("iPhone X 256GB")
    c.sendRequest()
