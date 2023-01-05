import card as c
import random

# def print_deck(list_cards):
#     """
#     Prints the cards into the same row
#     Parameter: list_cards - list of card object
#     Return: None
#     """
#     line1 = [x.line1 for x in list_cards]
#     line2 = [x.line2 for x in list_cards]
#     line3 = [x.line3 for x in list_cards]
#     deck = c.Deck(" ".join(line1), " ".join(line2), " ".join(line3))
#     print(deck)


def generate_deck():
    numbers = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    #suit = ["\u2660", "\u2665", "\u2666", "\u2663"]
    suit = ["A", "B", "C", "D"]
    deck = []
    for i in numbers:
        for j in range(4):
            deck.append(c.Card(i, suit[j]))
    deck.append(c.Card('BJ', " "))
    deck.append(c.Card('RJ', " "))

    return deck


def distribute_cards(game_deck):
    """
    Distribute a deck of  cards into 3 dizhu_cards, and 17 cards for each player
    Return: dizhu_cards, p1cards, p2cards, p3cards
    """
    dizhu_cards, p1cards, p2cards, p3cards = [], [], [], []
    for i in range(3):
        dizhu_cards.append(game_deck.pop(random.randint(0, 53 - i)))
    i = 0
    while i < 50:
        p1cards.append(game_deck.pop(random.randint(0, 50 - i)))
        i += 1
        p2cards.append(game_deck.pop(random.randint(0, 50 - i)))
        i += 1
        if i == 50:
            break
        p3cards.append(game_deck.pop(random.randint(0, 50 - i)))
        i += 1
    p3cards.append(game_deck.pop())

    # sort the decks using values, then suit (Spades - Clubs - Heart - Diamond order)
    p1cards.sort(key=lambda x: (x.val, x.suit))
    p2cards.sort(key=lambda x: (x.val, x.suit))
    p3cards.sort(key=lambda x: (x.val, x.suit))

    return [dizhu_cards, p1cards, p2cards, p3cards]


def turn(playerslist, priority):
    curr_player = priority
    player_decks = [x.deck for x in playerslist]
    player_names = [x.name for x in playerslist]
    last_move = []

    while True:  # exit loop when a round with one type of card finishes
        print("\n    -------------------------------   \n")
        print("    It's", player_names[curr_player], "\'s turn now (player number", str(curr_player + 1) + ")")
        while True:  # exit loop until a valid input is received
            print("\n", player_names[curr_player], "\'s current deck:")
            print(player_decks[curr_player])
            print("\n What's your move? (Type in values of your move, separated with space.")
            print("type p to pass")
            move = input(player_names[curr_player] + " > ").split(" ")
            if move[0] == "p":
                break

            # print(move)
            if player_decks[priority].play_card(move, last_move):  # if input is valid
                print(player_decks[priority])  # player's deck after playing card
                last_move = move


        curr_player += 1
        if curr_player > 2:
            curr_player = 0

        # todo: 检测如果一个回合结束了，然后break和return


players = []
for i in range(3):
    print()
    print("Player number", i + 1)
    name = input("What is your name? ")
    players.append(c.User(name, i, 0, [], False))

print("\n\n")

starting_deck = generate_deck()
split_deck = distribute_cards(starting_deck)

# Associate the player with one hand of cards
for i, player in enumerate(players):
    player.deck = c.Deck(split_deck[i + 1])
    print("Deck of", player.name, ":")
    print(player.deck)


# the equivalent of flipping a card during card distribution to see who gets dizhu priority
dizhu = random.randint(0, 2)
print("Player", players[dizhu].name, "gets 地主 priority")
print()

# 叫地主
points = [-1, -1, -1]
for i, player in enumerate(players):
    print()
    print("Player", player.name)

    # Friendly reminder for dizhu wanters
    if i != 0 and i != dizhu:
        print("You must call higher than", max(points), "if you want to be the 地主")
    point = int(input("How many points would you like to call? (1 - 3)"))
    points[i] = point

    if point == 3 and i == dizhu:
        player.dizhu = True
        dizhu = i
        break

maxVal = max(points)
if points[dizhu] == maxVal:
    print()
    print("Player", players[dizhu].name, "is the 地主")
    players[dizhu].dizhu = True
else:
    for i in range(len(points)):
        if points[i] == maxVal:
            print()
            print("Player", players[i].name, "is the 地主")
            players[i].dizhu = True
            dizhu = i
            break

print(players[dizhu].deck)
# Reveal dizhu cards
print("The dizhu cards are: ")
print(c.Deck(split_deck[0]))

# Add the 3 cards into dizhu deck
players[dizhu].deck.extend(split_deck[0])
print("The dizhu's cards after extend are: ")
print(players[dizhu].deck)


print("\n\n    --------  new game  --------    \n\n")
# turn是一种牌的回合
# 如果回合结束的话开启下一个turn
# todo: 从一个回合转到下一个回合
# todo: 如果有人赢了，结束这一局
turn(players, dizhu)


