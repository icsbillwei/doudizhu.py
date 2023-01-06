class Card:
    string = ""
    val = 0
    valRef = {
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
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
        self.string = index

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

    def play_card(self, values, last):
        """
        values: list[int]
        last: list[Cards] played last time
        return: removed_deck list[Cards] OR None if invalid
        """
        # print(">>>>>", [x.val for x in last])
        originaldeck = self.card_list[:]
        removed_deck = []
        for i in values:
            deckvalues = [x.string for x in self.card_list]
            try:
                idx = deckvalues.index(i)
                # print("idx:", idx)
                removed_deck.append(self.card_list.pop(idx))
            except ValueError:
                print("Invalid input: card not found in your deck")
                self.card_list = originaldeck
                return None

        removed_deck.sort(key=lambda x: (x.val, x.suit))
        print("XXXXXXXXXXX", Deck(removed_deck).identify_type())
        if len(last) == 0 and (Deck(removed_deck).identify_type() != ""
                               and Deck(removed_deck).identify_type() is not None):  # if the input is first in the round
            return removed_deck
        elif len(last) == 0:  # if the input is first in the round
            print("Invalid input: not a valid set of cards to play")
            self.card_list = originaldeck
            return None
        else:  # looks at the card last person played
            print(removed_deck)
            if valid_play(last, removed_deck) is True:
                return removed_deck
            elif valid_play(last, removed_deck) is False:
                print("The cards you played are not bigger than the previous player")
                self.card_list = originaldeck
                return None
            else:
                print("That was not a valid set of cards to play on top of the previous ones")
                self.card_list = originaldeck
                return None

    def __str__(self):
        # 还是把生成line放在这里，因为之后拍的变化会很大，最好自己每次print出来的时候就重新生成
        self.line1 = " ".join([x.line1 for x in self.card_list])
        self.line2 = " ".join([x.line2 for x in self.card_list])
        self.line3 = " ".join([x.line3 for x in self.card_list])
        return "{}\n{}\n{}\n".format(self.line1, self.line2, self.line3)

    def identify_type(self):
        # 单牌
        if len(self.card_list) == 1:
            return "Single"
        # 对子
        elif len(self.card_list) == 2 and self.card_list[0].val == self.card_list[1].val:
            return "Double"
        # 三个
        elif len(self.card_list) == 3 and self.card_list[0].val == self.card_list[1].val == self.card_list[2].val:
            return "Triple"
        # 三带一
        elif len(self.card_list) == 4:
            if self.card_list[0].val == self.card_list[1].val == self.card_list[2].val \
                    or self.card_list[1].val == self.card_list[2].val == self.card_list[3].val:
                return "Triple + Single"
        # 三带二
        elif len(self.card_list) == 5:  # todo: fix this
            print("ZZZZZZZZZZZ 3 + 2")  # debug
            if (self.card_list[0].val == self.card_list[1].val == self.card_list[2].val \
                and self.card_list[3].val == self.card_list[4].val) \
                    or (self.card_list[2].val == self.card_list[3].val == self.card_list[4].val \
                        and self.card_list[0].val == self.card_list[1].val):
                return "Triple + Double"
        elif len(self.card_list) >= 5:  # todo: fix this
            # 顺子
            print("ZZZZZZZZZZZ shunzi")
            straight = True
            for index in range(len(self.card_list) - 1):
                if self.card_list[index] + 1 != self.card_list[index + 1]:
                    straight = False
                    break
            if straight: return "Straight"
            # 连对
            if len(self.card_list % 2 == 0):  # length must be a multiple of 2
                consec_pairs = True
                print("ZZZZZZZZZZZ 334455")
                for index in range(0, len(self.card_list) - 1, 2):
                    if self.card_list[index] != self.card_list[index + 1]:
                        consec_pairs = False
                if consec_pairs: return "Consecutive Pairs"
        # todo: 飞机
        # 四个（炸弹）
        elif len(self.card_list) == 4 and self.card_list[0].val == self.card_list[1].val == self.card_list[2].val == \
                self.card_list[3].val:
            return "Bomb"
        # 王炸
        elif len(self.card_list) == 2 and self.card_list[0].string == "BJ" and self.card_list[1].string == "RJ":
            return "Joker Bomb"
        else:
            return ""


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

    def play_turn(self, last_move):
        # first - bool - if this person is the first of a round to play
        print("\n-------------------------------\n")
        print("It's " + self.name + "\'s turn now (player number", str(self.order + 1) + ")")
        valid_input = False
        while valid_input is False:  # exit loop until a valid input is received
            print("\n" + self.name + "\'s current deck:")
            print(self.deck)
            if len(last_move) != 0:
                print("\n You must play a hand that is larger than:")
                last = Deck(last_move)
                print(last)
            print("\nWhat's your move? (Type in values of your move, separated with space, or type p to pass.)")
            move = input(self.name + " > ").upper().split(" ")
            if move == ["P"]:
                return []
            played = self.deck.play_card(move, last_move)  # if input is valid
            if played is not None:
                print(self.name + " has played:")
                print(Deck(played))
                print(self.name + "'s updated deck is:")
                print(self.deck)
                return played

    def __str__(self):
        return self.name


def valid_play(last_played: list[Card], played: list[Card]):
    """
    last_played: what the player played last time, list[Cards]
    played: what the player played this time, list[Cards]
    return: whether if it's a valid play - bool
    """
    print(played,last_played)
    last_played_type = Deck(last_played).identify_type()
    played_type = Deck(played).identify_type()
    # print(" >>>>>>>>>>>>>>>>>>>>>>>>", played_type)

    if last_played_type == played_type:
        # 单牌，对子，三个，炸弹，顺子，连对比较方式一样
        if played_type == "Single" or played_type == "Double" or played_type == "Triple" or played_type == "Bomb" \
                or played_type == "Straight" or played_type == "Consecutive Pairs":
            return played[0].val > last_played[0].val
        # 三带一
        elif played_type == "Triple + Single":
            # 直接比较第二位这样不管单排在前还是后都在比较三个的
            return played[1].val > last_played[1].val
        # 三带二
        elif played_type == "Triple + Double":
            # 直接比较第三位这样不管对子在前还是后都在比较三个的
            return played[2].val > last_played[2].val
        # todo: 飞机

    # 如果出的炸弹
    elif last_played_type != "Bomb" and played_type == "Bomb":
        return True
    # 如果出的王炸
    elif played_type == "Joker Bomb":
        return True
    else:
        return None
