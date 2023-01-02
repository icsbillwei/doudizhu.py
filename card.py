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
        为了方便打印牌
        line1 = 第一行的string
        line2 = 第二行的string
        line3 = 第三行的string
        """
        try:
            self.val = int(index)
            if self.val == 2:
                self.val = 15
        except ValueError:
            self.val = self.valRef[index]

        self.suit = suit
        if self.val == 10:
            self.line1 = "|" + suit + "   |"
            self.line2 = "| " + str(index) + " |"
            self.line3 = "|    |"
        elif self.val < 16:
            self.line1 = "|" + suit + "  |"
            self.line2 = "| " + str(index) + " |"
            self.line3 = "|   |"
        else:
            self.line1 = "|    |"
            self.line2 = "| " + str(index) + " |"
            self.line3 = "|    |"

    def __str__(self):
        return "{}\n{}\n{}\n".format(self.line1, self.line2, self.line3)


class Deck:

    def __init__(self, line1, line2, line3):
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3

    def __str__(self):
        return "{}\n{}\n{}\n".format(self.line1, self.line2, self.line3)


class User:
    def __init__(self, order, points, cards):
        """
        dizhu = 地主 - bool
        order = 出牌顺序 - int
        win = 获胜次数 - int
        points = 积分？不确定 - int
        name = string
        """
        self.bool = False
        self.order = order
        self.win = 0
        self.points = 0
        self.deck = player_deck

    def play_turn(self):
        pass

    def respond_turn(self):
        pass
