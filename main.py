import card as c


def generate_deck():
    numbers = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    deck = []
    for i in numbers:
        for j in range(4):
            deck.append(c.Card(i))
    deck.append(c.Card('BJ'))
    deck.append(c.Card('RJ'))

    for i in deck:
        print(i, end=" ")


generate_deck()

