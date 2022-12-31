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

    def __init__(self, index):
        try:
            self.val = int(index)
            if self.val == 2:
                self.val = 15
        except ValueError:
            self.val = self.valRef[index]

        self.string = index

    def __str__(self):
        if self.val < 16:
            return """
|   |
| {0} |
|   |
""".format(self.string)
        else:
            return """
|    |
| {0} |
|    |
""".format(self.string)
