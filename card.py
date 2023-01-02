class Card:
    string = ""
    val = 0
    valRef = {
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
      # '2': 15,
        'BJ': 16,
        'RJ': 17
    }

    def __init__(self, index, suit):
        """
        index = 数字
        suit = 花色
        """
        try:
            self.val = int(index)
            if self.val == 2:
                self.val = 15
        except ValueError:
            self.val = self.valRef[index]

        self.string = index
        self.suit = suit

    def __str__(self):
        if self.val == 10:
            return """
|{1}   |
| {0} |
|    |
            """.format(self.string, self.suit)
        elif self.val < 16:
            return """
|{1}  |
| {0} |
|   |
""".format(self.string, self.suit)
        else:
            return """
|{1}  |
| {0} |
|    |
""".format(self.string, self.suit)
