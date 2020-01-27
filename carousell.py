class CarousellItem:
    def __init__(self, seller, time, name, price, desc, used):
        self.seller = seller
        self.time = time
        self.name = name
        self.price = price
        self.desc = desc
        self.used = used

    def toString(self):
        print("Seller:", self.seller)
        print("Time:", self.time)
        print("Name:", self.name)
        print("Price:", self.price)
        print("Description:", self.desc)
        print("Condition:", self.used)
        print("\n")

    def isValidItem(self):
        # drops items in spotlight; usually these results are useless
        v = True
        v = v and self.time[0].isnumeric() and self.used in [
            "Used", "New"]
        return v

    def isSameAs(self, cItem):
        # lazy checking
        return (self.seller == cItem.seller) and (self.time == cItem.time) and (self.desc == cItem.desc)
