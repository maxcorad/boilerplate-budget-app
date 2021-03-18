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
    title = "Percentage spent by category"

    # calculate total amount withdrawn per category
    amnt = lambda cat, i: cat.ledger[i]["amount"]
    cat_withdr = lambda cat: [
        amnt(cat, i) for i in range(len(cat.ledger)) if amnt(cat, i) < 0
    ]
    expenses = {cat: -sum(cat_withdr(cat)) for cat in categories}

    # calculate percentages relative to total expenditure
    expenditure = sum(expenses.values())
    pct = lambda cat: 100 * expenses[cat] / expenditure

    # define graph with axes, bars and labels
    graph = {
        "x_axis": "-",
        # vertical axis: percentages by 10
        "y_axis": [
            (str(i * 10) + "|").rjust(4) for i in reversed(range(11))
            ],
        "bars": {},
        "labels": {}
    }

    # populate graph with data from each category
    for cat in categories:
        graph["x_axis"] += "---"        # extend x-axis 3 dashes per cat.

        # create bars as sequence of characters to visualize percentages,
        # rounded down to tens with 'o' for each segment, justified right
        graph["bars"][cat] = ("o" + int(pct(cat) / 10) * "o").rjust(11)

        # asociate each label to its length.
        graph["labels"][cat.name] = len(cat.name)
    
    x_axis = "    " + graph["x_axis"]    # obtain x-axis as line of dashes
    
    # create chart portion above the x-axis line

    bars = list(graph["bars"].values())  # obtain list of bar strings

    # 'flip' bars to vertical by zipping all characters for each bar string.
    # as zip returns tuples, use join to convert to strings with whitespaces
    bars_lines = ["  ".join(t) + "  " for t in zip(*bars)]

    # join list of bar lines with vertical axis, convert to string
    graph_lines = [" ".join(t) for t in zip(graph["y_axis"], bars_lines)]
    graph_lines = "\n".join(graph_lines)

    # create chart portion below x-x_axis
    
    # calculate length of longest label
    max_len = max(graph["labels"].values())
    # list of label strings, completed with whitespaces for equal length
    labels = [label.ljust(max_len) for label in graph["labels"]]
    # flip to vertical by zip; add whitespace; join
    label_lines = ["     " + "  ".join(t) + "  " for t in zip(*labels)]
    label_lines = "\n".join(label_lines)

    # create chart by merging all sections
    chart = "\n".join([title, graph_lines, x_axis, label_lines])
    return chart
