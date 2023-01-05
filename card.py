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

    def __init__(self, card_list):
        # card_list = list[Cards]
        self.card_list = card_list

    def extend(self, dizhu_cards):
        # Extend into the card_list
        self.card_list.extend(dizhu_cards)
        # Sort again
        self.card_list.sort(key=lambda x: (x.val, x.suit))

    def __str__(self):
        # 还是把生成line放在这里，因为之后拍的变化会很大，最好自己每次print出来的时候就重新生成
        self.line1 = " ".join([x.line1 for x in self.card_list])
        self.line2 = " ".join([x.line2 for x in self.card_list])
        self.line3 = " ".join([x.line3 for x in self.card_list])
        return "{}\n{}\n{}\n".format(self.line1, self.line2, self.line3)


class User:
    def __init__(self, name, order, points, player_deck, dizhu):
        """
        name = 玩家名 - string
        order = 出牌顺序 - int
        points = 积分？不确定 - int
        player_deck = 牌组 - Deck object
        win = 获胜次数 - int
        dizhu = 地主 - bool
        """
        self.name = name
        self.order = order
        self.points = points
        self.win = 0
        self.deck = player_deck
        self.dizhu = dizhu

    def play_turn(self):
        pass

    def respond_turn(self):
        pass
