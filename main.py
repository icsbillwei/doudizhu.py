import card as c
import random


def print_deck(list_cards):
    """
    Prints the cards into the same row
    Parameter: list_cards - list of card object
    Return: None
    """
    line1 = [x.line1 for x in list_cards]
    line2 = [x.line2 for x in list_cards]
    line3 = [x.line3 for x in list_cards]
    deck = c.Deck(" ".join(line1), " ".join(line2), " ".join(line3))
    print(deck)


def generate_deck():
    numbers = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    suit = ["\u2660", "\u2665", "\u2666", "\u2663"]
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
    Return: None
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

    print_deck(dizhu_cards)
    print_deck(p1cards)
    print_deck(p2cards)
    print_deck(p3cards)


game_deck = generate_deck()
distribute_cards(game_deck)
