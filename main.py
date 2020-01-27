import requests
import json
import helper as Helper
from bs4 import BeautifulSoup
from carousell import CarousellItem
from fileSaver import FileSaver


class CarousellSearcher:

    BASE_URL = "http://sg.carousell.com/search/"

    def __init__(self, url="", results_count=10, query=[]):
        self.url = self.BASE_URL
        self.results = []

    def updateQueriesAndGetResults(self, query_string):
        print("Getting results from: ", end="")
        self.addQueries(query_string)
        self.sendRequest()
        print("...")
        self.filterResultsByPrice()

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
                array[j], array[j+1], array[j+2], Helper.castPriceAsInt(array[j+3]), array[j+4], array[j+5])
            # validate items
            if carouResult.isValidItem():
                new_array.append(carouResult)
        return new_array

    def filterResultsByPrice(self):
        mean = Helper.getMean(self.results)
        minPrice = 0.6 * mean    # 40% price buffer
        maxPrice = 1.4 * mean
        for item in self.results:
            if not (minPrice < item.price < maxPrice):
                self.results.remove(item)
        print("There are {} results.".format(len(self.results)))

    def printCheapest(self):
        result = Helper.getCheapest(self.results)
        print("Lowest price: S$", result.price)


if __name__ == "__main__":
    c = CarousellSearcher()
    c.updateQueriesAndGetResults("iPhone X 256GB")
    c.printCheapest()

    fs = FileSaver("records.txt")
    updatedCount = 0
    for item in c.results:
        if fs.updateFile(item):
            updatedCount += 1
    print("Number of new items:", updatedCount)

    search = input("Enter a seller's id")
    item = fs.searchFileForItem(search)
    if item:
        item.toString()
    else:
        print("No such item found.")
