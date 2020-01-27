
def getMean(results):
    p = 0
    count = 0
    for item in results:
        if item.price != 0:
            p += item.price
            count += 1
    return round(p / count, 2)


def getCheapest(results):
    p = 100000000
    for item in results:
        if item.price < p:
            p = item.price
            cheapestItem = item
    return cheapestItem


def castPriceAsInt(priceString):
    if "," in priceString:
        priceString = priceString.replace(",", "")
    if "S$" in priceString:
        priceString = priceString.replace("S$", "")
    return int(priceString)
