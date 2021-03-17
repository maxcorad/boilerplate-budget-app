class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        funds = self.check_funds(amount)
        if funds:
            self.ledger.append({"amount": -amount, "description": description})
        return funds

    def get_balance(self):
        movements = [self.ledger[i]["amount"] for i in range(len(self.ledger))]
        return sum(movements)

    def transfer(self, amount, other):
        funds = self.check_funds(amount)
        if funds:
            self.withdraw(amount, description=f"Transfer to {other.name}")
            other.deposit(amount, description=f"Transfer from {self.name}")
        return funds

    def check_funds(self, amount):                
        print(self.get_balance(), amount)
        return False if self.get_balance() < amount else True

    def __str__(self):
        title = self.name.center(30, "*")
        total = f"Total: {self.get_balance()}"
        ledger = self.ledger
        desc = lambda x: ledger[x]["description"]
        amnt = lambda x: "%.2f" % ledger[x]["amount"]
        desc_just = lambda x, y: desc(x)[:y] if len(desc(x)) > y else desc(x).ljust(y)
        amnt_just = lambda x, y: amnt(x)[:y] if len(amnt(x)) > y else amnt(x).rjust(y)
        items = [desc_just(i, 23) + amnt_just(i, 7) for i in range(len(ledger))]
        item_str = "\n".join(items)
        return title + "\n" + item_str + "\n" + total


def create_spend_chart(categories):
    pass
