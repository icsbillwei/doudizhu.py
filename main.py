import card as c
import random
import discord
from discord.ext import commands


# bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

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
    # suit = ["\u2660", "\u2665", "\u2666", "\u2663"]
    # suit = ["A", "B", "C", "D"]
    suit = ["<:aspade:1061103128759521371>", "<:bheart:1061103493773017199>", "<:cdiamond:1061103591730970675>",
            ":fleur_de_lis:"]
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


async def turn(playerslist, priority, channels):
    """
    playerslist: all players. - List[User]
    priority: the one who is the first of a round. - int index of curr player
    player who is the start of the next round. - int player index who goes first for the next round
    """
    curr_player = priority
    last_move = []
    num_passes = 0
    beginning_of_round = True
    while True:  # exit loop when a round with one round finishes
        chan = channels[curr_player]
        move = await playerslist[curr_player].play_turn(last_move, chan, channels, client)

        while move == [] and beginning_of_round and curr_player == priority:
            # print("You are the first to play in this round, you cannot pass.")
            chan.send("You are the first to play in this round, you cannot pass.")
            move = await playerslist[curr_player].play_turn(last_move, chan, channels, client)

        # Check if this player has won
        if len(playerslist[curr_player].deck.card_list) == 0:
            return 100 + curr_player
        beginning_of_round = False
        curr_player += 1
        if curr_player > 2:
            curr_player = 0
        # print("next player", curr_player+1)
        for chn in channels:
            if chn == channels[curr_player]:
                await chn.send("You are the next player")
            else:
                await chn.send("next player is " + playerslist[curr_player].name)

        # Check if the round has finished
        if int(len(move)) == 0:
            num_passes += 1
        elif int(len(move)) > 0:
            num_passes = 0
        if int(num_passes) == 2:
            # print("No one responded to", playerslist[curr_player].name + "\'s cards.")
            for chn in channels:
                if chn == channels[curr_player]:
                    await chn.send("No one responded to your cards.")
                else:
                    await chn.send("No one responded to " + playerslist[curr_player].name + "\'s cards.")
            return curr_player

        if int(len(move)) != 0:  # 如果上一个玩家pass了的话, last_move不会是空白
            last_move = move
        else:
            pass


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@client.event
async def on_ready():
    print("doudizhu.py online")


inp = ""

'''
@client.event
async def on_message(msg):

    if msg.content.startswith(">"):
        global inp
        inp = msg
        print(msg)
    await client.process_commands(msg)
'''

@client.command()
async def start(ctx):
    await ctx.reply("Game started")

    chan1 = client.get_channel(1061044080848666634)
    chan2 = client.get_channel(1061044227372494971)
    chan3 = client.get_channel(1061044465042731148)
    channels = [chan1, chan2, chan3]

    for chan in channels:
        await chan.send("_ _")
        await chan.send(" ----------------------- New Game -----------------------  ")

    players = []
    for i in range(3):
        # print()
        # print("Player number", i + 1)
        await channels[i].send("What is your name, Player number " + str(i + 1) + "?")

        def check(m):
            return m.channel == channels[i]

        name = await client.wait_for('message', check=check)
        players.append(c.User(name.content, i, 0, [], False))

    # print("\n\n")

    starting_deck = generate_deck()
    '''
    for card in starting_deck:
        card.print(channels[0])
    '''

    split_deck = distribute_cards(starting_deck)

    # Associate the player with one hand of cards
    for i, player in enumerate(players):
        player.deck = c.Deck(split_deck[i + 1])
        # print("Deck of", player.name, ":")
        await channels[i].send("Your deck: ")
        await player.deck.print(channels[i])


    # the equivalent of flipping a card during card distribution to see who gets dizhu priority
    dizhu = random.randint(0, 2)
    for i, chan in enumerate(channels):
        if i == dizhu:
            await chan.send("You get the 地主 priority")
        else:
            await chan.send("Player " + players[dizhu].name + " gets 地主 priority")
        if i != 0:
            await chan.send("Waiting for players in front of you to call their points")

    # 叫地主
    points = [-1, -1, -1]
    for i, player in enumerate(players):

        for j, point in enumerate(points):
            if point != -1:
                await channels[i].send("Player " + players[j].name + " called " + str(point) + " points")

        while True:
            # print("Player", player.name)

            await channels[i].send("Player " + player.name + ", How many points would you like to call? (1 - 3)")

            # Friendly reminder for dizhu wanters
            if i != 0 and i != dizhu:
                # print("You must call higher than", max(points), "if you want to be the 地主")
                await channels[i].send("You must call higher than " + str(max(points)) + " if you want to be the 地主")
            # point = int(input("How many points would you like to call? (1 - 3) > "))

            def check(m):
                return m.channel == channels[i]

            pointMsg = await client.wait_for('message', check=check)
            try:
                point = int(pointMsg.content)
            except ValueError:
                await channels[i].send("Invalid input")
                continue

            if 3 >= point >= 1:
                await channels[i].send("You called " + str(point) + " points.")
                break
            else:
                await channels[i].send("Invalid input")

        points[i] = point

        if point == 3 and i == dizhu:
            player.dizhu = True
            dizhu = i


    maxVal = max(points)
    if points[dizhu] == maxVal:
        # print("Player", players[dizhu].name, "is the 地主")
        for i, chan in enumerate(channels):
            if i == dizhu:
                await chan.send("You are the 地主")
            else:
                await chan.send("Player " + players[dizhu].name + " is the 地主")
        players[dizhu].dizhu = True
    else:
        for i in range(len(points)):
            if points[i] == maxVal:
                # print("Player", players[i].name, "is the 地主")
                for chan in channels:
                    await chan.send("Player " + players[i].name + " is the 地主")
                players[i].dizhu = True
                dizhu = i
                break

    # print(players[dizhu].deck)
    # Reveal dizhu cards
    # print("The dizhu cards are: ")
    # print(c.Deck(split_deck[0]))

    for chan in channels:
        await chan.send("The 地主 cards are:")
        await c.Deck(split_deck[0]).print(chan)

    # Add the 3 cards into dizhu deck
    players[dizhu].deck.extend(split_deck[0])
    # print("The dizhu's cards after extend are: ")
    # print(players[dizhu].deck)
    await channels[dizhu].send("Your deck after adding the 地主 cards:")
    await players[dizhu].deck.print(channels[dizhu])

    # print("\n\n    --------  new game  --------    \n")
    for chan in channels:
        await chan.send("__ __")
        await chan.send(" **-Game Start-**")

    # turn是一种牌的回合
    # 如果回合结束的话开启下一个turn
    dizhu = int(dizhu)
    actual_dizhu = dizhu + 0
    while dizhu < 100:
        dizhu = await turn(players, dizhu, channels)

    # print("Congratulations player" ,players[dizhu%100])
    for chan in channels:
        chan.send("Congratulations player " + players[dizhu%100].name)
        if actual_dizhu == dizhu % 100:
            chan.send("The 地主 has won this game")
        else:
            chan.send("The farmers have won this game")


client.run('MTA2MTAwMDg2NDgyMDY0NTg4OQ.GDMsA8.kpXKP8G1EVqMpYFgcfHl3c2MayDQ_RCT-PqaXM')

