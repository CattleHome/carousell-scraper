import requests
import json
from bs4 import BeautifulSoup


class CarousellItem:
    def __init__(self, seller, time, name, price, desc, used):
        self.seller = seller
        self.time = time
        self.name = name
        self.price = price
        self.desc = desc
        self.used = used

    def toString(self):
        print("Seller:" + self.seller)
        print("Time:" + self.time)
        print("Name:" + self.name)
        print("Price:" + self.price)
        print("Description:" + self.desc)
        print("Condition:" + self.used)
        print("\n")

    def isValidItem(self):
        # drops items in spotlight; usually these results are useless
        v = True
        v = v and self.time[0].isnumeric() and self.price[0:2] == "S$" and self.used in [
            "Used", "New"]
        return v


class CarousellSearch:

    BASE_URL = "http://sg.carousell.com/search/"

    def __init__(self, url="", results_count=10, query=[]):
        self.url = self.BASE_URL
        self.results = []

    def updateQueriesAndGetResults(self, query_string):
        print("Getting results from: ", end="")
        self.addQueries(query_string)
        self.sendRequest()
        print("...")
        print("There are {} results.".format(len(self.results)))

    def addQueries(self, query_string):
        self.query = query_string.split(" ")
        query = "%20".join(self.query)
        self.url += query
        print(self.url)

    def sendRequest(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')

        p_tags = soup.find_all('p')
        tags = []
        for tag in p_tags:
            tags.append(tag.text)
        self.results = self.parse_results(tags)

    def clearSearchResults(self):
        self.url = self.BASE_URL
        self.results = []

    def parse_results(self, array):
        new_array = []
        # find the start of first result; may break on update
        for i in range(len(array)):
            if array[i] == "Mailing & Delivery" and array[i-1] == "Meet-up":
                start_line = i+1
        for j in range(start_line, len(array), 7):
            if (array[j] == "Follow us"):
                break
            carouResult = CarousellItem(
                array[j], array[j+1], array[j+2], array[j+3], array[j+4], array[j+5])
            # validate items
            if carouResult.isValidItem():
                new_array.append(carouResult)
            else:
                carouResult.toString()
        return new_array


if __name__ == "__main__":
    c = CarousellSearch()
    c.updateQueriesAndGetResults("iPhone X 256GB")
