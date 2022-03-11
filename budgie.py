class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        total = 0
        for x in self.ledger:
            items += f"{x['description'][0:23]:23}" + f"{x['amount']:>7.2f}" + "\n"

            total += x["amount"]
        output = title + items + "Total: " + str(total)
        return output

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if (self.check_funds(amount)):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total_cash = 0
        for i in self.ledger:
            total_cash += i["amount"]

        return total_cash

    def transfer(self, amount, category):
        if (self.check_funds(amount)):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        return False

    def check_funds(self, amount):
        if (self.get_balance() >= amount):
            return True
        return False

    def get_withdrawals(self):
        total = 0
        for x in self.ledger:
            if x["amount"] < 0:
                total += x["amount"]
        return total

def truncate(n):
    multiplier = 10
    return int(n * multiplier) / multiplier

def get_totals(categories):
    total = 0
    breakdown = []
    for category in categories:
        total += category.get_withdrawals()
        breakdown.append(category.get_withdrawals())

    rounded = list(map(lambda x: truncate(x/total), breakdown))

    return rounded


def create_spend_chart(categories):
    res = "Percentage spent by category\n"
    i = 100
    totals = get_totals(categories)
    while i >= 0:
        cat_spaces = " "
        for total in totals:
            if total * 100 >= i:
                cat_spaces += "o  "
            else:
                cat_spaces += "   "
        res += str(i).rjust(3) + "|" + cat_spaces + ("\n")
        i -= 10

    dashes = "-" + "---" * len(categories)
    names = []
    x_axis = ""
    for category in categories:
        names.append(category.name)

    maxi = max(names, key=len)

    for x in range(len(maxi)):
        nameStr = '     '
        for name in names:
            if x >= len(name):
                nameStr += '   '
            else:
                nameStr += name[x] + '  '

        if (x != len(maxi) - 1):
            nameStr += "\n"

        x_axis += nameStr

    res += dashes.rjust(len(dashes) + 4) + "\n" + x_axis
    return res


food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
print(food)
print(entertainment)
print(business)
print(create_spend_chart([business, food, entertainment]))


