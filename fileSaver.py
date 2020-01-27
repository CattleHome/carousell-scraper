from carousell import CarousellItem
import os


class CarouRecord:
    def __init__(self, carouItem):
        self.text = carouItem.seller + ";" + carouItem.time + ";" + carouItem.name + \
            ";" + str(carouItem.price) + ";" + carouItem.desc + \
            ";" + carouItem.used + "\n"


class FileSaver:
    def __init__(self, itemName):
        self.itemName = itemName
        self.fileName = "carousell_{}.txt".format(itemName)

    def updateFile(self, carouItem):
        if not self.checkForExistingRecord(carouItem):
            self.saveToFile(carouItem)
            return True
        return False

    def saveToFile(self, carouItem):
        with open(self.fileName, "a") as f:
            cr = CarouRecord(carouItem)
            f.write(cr.text)

    def checkForExistingRecord(self, carouItem):
        if not os.path.isfile(self.fileName):
            print("creating new file")
            with open(self.fileName, "w") as f:
                return False

        with open(self.fileName, "r") as f:
            for record in f:
                item = self.getItemFromLine(record)
                if item.isSameAs(carouItem):  # found matching item
                    return True
            return False

    def getItemFromLine(self, text):
        array = text.split(";")
        item = CarousellItem(array[0], array[1],
                             array[2], array[3], array[4], array[5])
        return item

    def searchFileForItem(self, seller_id):
        with open(self.fileName, "r") as f:
            lines = f.readlines()
            for line in lines:
                item = self.getItemFromLine(line)
                if item.seller == seller_id:
                    return item
            return None
