#!/usr/bin/python
# -*- coding: UTF_8 -*-

# GitHub: https://github.com/Nagidal/poker

# NEEDS: defusedxml

# How to debug this:
# set path to Python27
# run cmd in winpdb dir, then start winpdb by "python winpdb.py"
# set path to Python34
# run a new instance of cmd from the dir of poker.py
# type "python <winpdb dir>rpdb2.py -pahoj -d poker.py" (password is "ahoj"
# type 'python "y:\sven\My Dropbox\Dropbox\python\winpdb\rpdb2.py" -pahoj -d poker.py'
# we need the following keypress routine in order to attach the script to the winpdb debugger (workaround for a bug in rpdb2.py)

import msvcrt
msvcrt.getch()

import argparse, warnings, random, math, copy, inspect
import init
import brain
import shuffling
import messenger as m
from enum import Enum
from lib import rndint # needed for true random shuffle of the deck of cards
from collections import OrderedDict
from defusedxml import ElementTree

# Shortcuts and aliases:
messenger = m.messenger

# Parsing the arguments requires this modified version of FileType for argparse
# source: http://stackoverflow.com/questions/8236954/specifying-default-filenames-with-argparse-but-not-opening-them-on-help
class ForgivingFileType(argparse.FileType):
    def __call__(self, string):
        try:
            super(ForgivingFileType,self).__call__(string)
        except IOError as err:
            warnings.warn(err)

parser = argparse.ArgumentParser(prog="Poker Pie")
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Report internal stuff")
parser.add_argument("-n", "--nolog", dest="log", action="store_false", default=True, help="Don't log")
parser.add_argument("-s", "--shuffleOnly", action="store_true", default=False, help="Shuffle only")
parser.add_argument("-r", "--requirements", dest="requiredHandsFileName", metavar="file", default="", type=str, help="Read requirements from file (default: requirements.xml)")
args = parser.parse_args()

init.verbose = args.verbose
init.log = args.log
init.shuffleOnly = args.shuffleOnly
init.requiredHands = args.requiredHandsFileName

## OptionParser will parse command line argumenty
#parser = OptionParser(usage="%prog", version="%prog 0.0.2", prog="Poker Pie")
#parser.add_option("-v", "--verbose",dest="verbose", default=True, action="store_true", help="Report internal stuff")
#parser.add_option("-n", "--nolog", dest="log", default=True, action="store_false", help="Don't log")
## If the script is executed with the shuffle option, the program will only generate shuffled decks and store them in a file.
#parser.add_option("-s", "--shuffle", dest="shuffleOnly", default=False, action="store_true", help="Shuffle only")
#parser.add_option("-r", "--required", dest="requiredHands", default=False, action="store_true", help="Play the hands defined in the XML")
#(options,args) = parser.parse_args()


#init.verbose = options.verbose
#init.log = options.log
#init.shuffleOnly = options.shuffleOnly
#init.requiredHands = options.requiredHands

# If logging is enabled, create the necessary files:
if init.log:
    # general log file
    logfile = open("log.txt", mode="w", encoding="UTF_8")
    # include this logfile in the set of targets for messages
    init.msgTarget["logfile"] = logfile

# Card names:
# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
class CardValue(Enum):
    ace = 14
    king = 13
    queen = 12
    jack = 11
    ten = 10
    nine = 9
    eight = 8
    seven = 7
    six = 6
    five = 5
    four = 4
    trey = 3
    deuce = 2

cardNames = dict(zip((CardValue.ace, CardValue.king, CardValue.queen, CardValue.jack, CardValue.ten, CardValue.nine, CardValue.eight, CardValue.seven, CardValue.six, CardValue.five, CardValue.four, CardValue.trey, CardValue.deuce), ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")))

# Color names:
# S = spades, H = hearts, D = diamonds, C = clubs
class CardColor(Enum):
    spades = 3
    hearts = 2
    diamonds = 1
    clubs = 0

cardColors = dict(zip((CardColor.spades, CardColor.hearts, CardColor.diamonds, CardColor.clubs), ("S", "H", "D", "C")))

# Pocket cards:
# AKs = A and K of the same color (s = suited)

class Card():
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.orderNumber = None
    def __call__(self, parameter="short"):
        if parameter == "short":
            return cardNames[self.value] + cardColors[self.color]
        if parameter == "text":
            return self.value.name + " of " + self.color.name

class Deck():
    def __init__(self):
        self.SA = Card(CardValue.ace, CardColor.spades)
        self.SK = Card(CardValue.king, CardColor.spades)
        self.SQ = Card(CardValue.queen, CardColor.spades)
        self.SJ = Card(CardValue.jack, CardColor.spades)
        self.ST = Card(CardValue.ten, CardColor.spades)
        self.S9 = Card(CardValue.nine, CardColor.spades)
        self.S8 = Card(CardValue.eight, CardColor.spades)
        self.S7 = Card(CardValue.seven, CardColor.spades)
        self.S6 = Card(CardValue.six, CardColor.spades)
        self.S5 = Card(CardValue.five, CardColor.spades)
        self.S4 = Card(CardValue.four, CardColor.spades)
        self.S3 = Card(CardValue.trey, CardColor.spades)
        self.S2 = Card(CardValue.deuce, CardColor.spades)
        self.HA = Card(CardValue.ace, CardColor.hearts)
        self.HK = Card(CardValue.king, CardColor.hearts)
        self.HQ = Card(CardValue.queen, CardColor.hearts)
        self.HJ = Card(CardValue.jack, CardColor.hearts)
        self.HT = Card(CardValue.ten, CardColor.hearts)
        self.H9 = Card(CardValue.nine, CardColor.hearts)
        self.H8 = Card(CardValue.eight, CardColor.hearts)
        self.H7 = Card(CardValue.seven, CardColor.hearts)
        self.H6 = Card(CardValue.six, CardColor.hearts)
        self.H5 = Card(CardValue.five, CardColor.hearts)
        self.H4 = Card(CardValue.four, CardColor.hearts)
        self.H3 = Card(CardValue.trey, CardColor.hearts)
        self.H2 = Card(CardValue.deuce, CardColor.hearts)
        self.DA = Card(CardValue.ace, CardColor.diamonds)
        self.DK = Card(CardValue.king, CardColor.diamonds)
        self.DQ = Card(CardValue.queen, CardColor.diamonds)
        self.DJ = Card(CardValue.jack, CardColor.diamonds)
        self.DT = Card(CardValue.ten, CardColor.diamonds)
        self.D9 = Card(CardValue.nine, CardColor.diamonds)
        self.D8 = Card(CardValue.eight, CardColor.diamonds)
        self.D7 = Card(CardValue.seven, CardColor.diamonds)
        self.D6 = Card(CardValue.six, CardColor.diamonds)
        self.D5 = Card(CardValue.five, CardColor.diamonds)
        self.D4 = Card(CardValue.four, CardColor.diamonds)
        self.D3 = Card(CardValue.trey, CardColor.diamonds)
        self.D2 = Card(CardValue.deuce, CardColor.diamonds)
        self.CA = Card(CardValue.ace, CardColor.clubs)
        self.CK = Card(CardValue.king, CardColor.clubs)
        self.CQ = Card(CardValue.queen, CardColor.clubs)
        self.CJ = Card(CardValue.jack, CardColor.clubs)
        self.CT = Card(CardValue.ten, CardColor.clubs)
        self.C9 = Card(CardValue.nine, CardColor.clubs)
        self.C8 = Card(CardValue.eight, CardColor.clubs)
        self.C7 = Card(CardValue.seven, CardColor.clubs)
        self.C6 = Card(CardValue.six, CardColor.clubs)
        self.C5 = Card(CardValue.five, CardColor.clubs)
        self.C4 = Card(CardValue.four, CardColor.clubs)
        self.C3 = Card(CardValue.trey, CardColor.clubs)
        self.C2 = Card(CardValue.deuce, CardColor.clubs)
        self.cards = list((self.SA, self.SK, self.SQ, self.SJ, self.ST, self.S9, self.S8, self.S7, self.S6, self.S5, self.S4, self.S3, self.S2, self.HA, self.HK, self.HQ, self.HJ, self.HT, self.H9, self.H8, self.H7, self.H6, self.H5, self.H4, self.H3, self.H2, self.DA, self.DK, self.DQ, self.DJ, self.DT, self.D9, self.D8, self.D7, self.D6, self.D5, self.D4, self.D3, self.D2, self.CA, self.CK, self.CQ, self.CJ, self.CT, self.C9, self.C8, self.C7, self.C6, self.C5, self.C4, self.C3, self.C2))
        self.cards.reverse()
        # We need to creade a dicitonary of pointers to the cards of this deck
        # We use a custom function to list all attributes and methods of this class
        def get_user_attributes(cls):
            """found at http://stackoverflow.com/questions/4241171/inspect-python-class-attributes"""
            boring = dir(type('dummy', (object,), {}))
            return [item
                for item in inspect.getmembers(cls)
                if item[0] not in boring]
        self.pointersToCards = dict(get_user_attributes(self))
        # delete unnecessary entries in pointersToCards
        for key in list(self.pointersToCards.keys()):
            # delete every key which is longer than two characters (all cards are tewo characters long, they will remain in the dictionary)
            if len(key) > 2:
                del self.pointersToCards[key]
        del get_user_attributes
    def __call__(self, parameter="short"):
        listOfCards = list()
        for card in self.cards:
            listOfCards.append(card(parameter))
        return listOfCards
    def cut(self):
        """Take 1/3 or 2/3 of a deck, place it aside, put the remaining cards on top of it."""
        #Sample (1/3): 18, 24, 21, 20, 21, 20, 19, 17, 18, 21, 18, 18, 18, 21, 17 (mean: 19.4) 17-24 µ=19.5, σ=2.2
        #Sample (2/3): 15, 11, 17, 18, 17, 19, 16, 16, 19, 13, 15, 17, 15, 21, 17 (mean: 16,4) 14-21 µ=16.5, σ=2.2
        # We will use Gaussian distribution, with µ=19.4, s=2.2 for upper third, and µ=16.4, s=2.2 for lower third.
        # artificial boundaries will be set by ±4
        # decide whether to take the upper of lower half
        # if upper half, then µ is 19.5
        if bool(random.getrandbits(1)):
            µ = 19.5
        else:
            µ = 35.5 # [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
        σ = 2.2
        # we set an upper and lower limit to the Gaussian distribution
        limitDistribution = 4
        cardsTaken = 0
        while (cardsTaken < math.floor(µ - limitDistribution)) or (cardsTaken > math.ceil(µ + limitDistribution)):
            cardsTaken = random.gauss(µ, σ)
        cardsTaken = int(round(cardsTaken, 0))
        self.cards = self.cards[cardsTaken:] + self.cards[:cardsTaken]
    def box(self):
        """This divides the deck roughly into quarters and reverses their order."""
        # Deck = Q1, Q2, Q3, Q4. Boxed deck = Q4, Q3, Q2, Q1
        # we have 52 cards in the deck
        cards = len(self.cards)
        # prepare card counts in the quarters (here called boxes)
        boxes = [0, 0, 0]
        # gather boxing parameters from the init module
        mus = (init.boxQ1mu, init.boxQ2mu, init.boxQ3mu)
        sigmas = (init.boxQ1sigma, init.boxQ2sigma, init.boxQ3sigma)
        limits = (init.boxQ1Limit, init.boxQ2Limit, init.boxQ3Limit)
        # zip everything together
        parameters = zip(boxes, mus, sigmas, limits, range(len(boxes)))
        # we find the card counts (integers) in the first three quarters (loops 3x)
        for box, mu, sigma, limit, boxIndex in parameters:
            roundedMu = round(mu * cards)
            while box not in range(roundedMu - limit, roundedMu + limit + 1):
                box = round(cards * random.gauss(mu, sigma))
            boxes[boxIndex] = box
            # count the number of the remaining cards
            cards = cards - box
        # the fourth quarter's card count is the number of remaining cards after three quarters have been taken from it.
        boxes.append(cards)
        # Now we know the number of cards in each quarter of the deck, e.g. boxes = [14, 16, 12, 10]
        # We must re-order the deck appropriately. That is:
        # reorder the cards in the stack by grouping them into four groups and reversing the order of these groups. 
        # the numbers of cards in each group is given in the list boxes, e.g. boxes = [14, 16, 12, 10]
        self.cards = self.cards[sum(boxes[:3]):sum(boxes)] + self.cards[sum(boxes[:2]):sum(boxes[:3])] + self.cards[boxes[0]:sum(boxes[:2])] + self.cards[:boxes[0]]
    def riffle(self):
        # pick a riffle pattern:
        pattern = random.choice(shuffling.listOfPatterns)
        # divide the deck into an upper and a lower half, according to the pattern:
        self.cards.reverse()
        upperHalf = self.cards[:sum(pattern.upper)]
        lowerHalf = self.cards[sum(pattern.upper):]
        # create a dictionary of deck halves according to the pattern
        halves = dict(zip([False, True], [upperHalf, lowerHalf]))
        # riffle the cards according to the pattern
        riffledCards = list()
        for n, b in pattern:
            for counter in range(n):
                riffledCards.append(halves[b].pop())
        self.cards = riffledCards
    def casinoShuffle(self):
        random.shuffle(self.cards)
        self.riffle()
        self.riffle()
        self.box()
        self.riffle()
        self.cut()
    def randomOrgShuffle(self):
        # Seed Random Generator with true Random Value ans shuffle list
        # random.seed(rndint.get(0, len(self.cards), 1).pop())
        # random.shuffle(self.cards)
        # rndint.get function reference: https://code.google.com/p/pyrndorg/source/browse/trunk/rndint.py?r=2
        pass
    def pop(self):
        return self.cards.pop()
    def store(self, filename="shuffled.dex"):
        # An efficient way how to store the sequence of the cards in the deck was suggested by Ross Millikan:
        # http://math.stackexchange.com/questions/134815/minimum-number-of-bits-required-to-store-the-order-of-a-deck-of-cards
        # For storing the order of cards in the deck most efficiently, we encode the fist 20 cards in it with 6 bits/card
        # Then there are only 32 cards left to be encoded. The order of the first 16 of them can be stored only with 5 bits/card.
        # Then there are only 16 cards left to be encoded. The order of the first 8 of them can be stored only with 4 bits/card.
        # Then there are only 8 cards left to be encoded. The order of the first 4 of them can be stored only with 3 bits/card.
        # Then there are only 4 cards left to be encoded. The order of the first 2 of them can be stored only with 2 bits/card.
        # Then there are only 2 cards left to be encoded. The order of the first 1 of them can be stored only with 1 bits/card.
        # Then there is only 1 card left. Its order does not need to be stored. It is the last card in the deck (0 bits/card).
        # The order of cards in the whole deck needs 1*0+1*1+2*2+4*3+8*4+16*5+20*6 = 249 bits = 32 bytes
        # We will do the following:
        # Take first 20 cards from the shuffled deck. For each card find its position in the sorted reference deck of cards.
        # Append the card's reference position number to the list of numbers to be saved in the first 120 (20*6) bits.
        # After this is done, remove these positions from the reference deck.
        cardsToSkipAtTheBeginningOfShuffledDeck = 0
        # create a sorted reference deck of cards.
        refDeck = sorted(copy.copy(self.cards), key = lambda card: (card.color.value, card.value.value), reverse = False)
        # prepare the list of card's reference position numbers
        with open(filename, mode="ab+") as shufflings:
            for cardsToStore, bitsPerCard, bytesToBeUsed in zip(init.cardsToStoreEachLoop, init.bitsPerCardEachLoop, init.bytesEachLoop):
                numbersToStore = list()
                for i in range(cardsToStore):
                    # find the position of the ith card in the deckToStore in the reference deck and append it to the list of numbers to be stored
                    numbersToStore.append(refDeck.index(self.cards[i+cardsToSkipAtTheBeginningOfShuffledDeck]))
                cardsToSkipAtTheBeginningOfShuffledDeck = cardsToSkipAtTheBeginningOfShuffledDeck + cardsToStore
                # store the numbers from the list numbersToStore in a huge integer
                hugeInteger = 0
                for number in numbersToStore:
                    hugeInteger = hugeInteger << bitsPerCard
                    hugeInteger = hugeInteger ^ number
                # write the hugeInteger as bytes into the file.
                shufflings.write((hugeInteger).to_bytes(bytesToBeUsed, byteorder="big"))
                # remove the numbers from the saved list from the reference deck
                numbersToStore.sort(reverse=True)
                for number in numbersToStore:
                    refDeck.remove(refDeck[number])
    def readFromFile(self, filename="shuffled.dex"):
        # prepare a reference deck:
        refDeck = sorted(copy.copy(self.cards), key = lambda card: (card.color.value, card.value.value), reverse = False)
        # prepare an empty deck
        loadedDeck = list()
        cardsToSkipAtTheBeginningOfLoadedDeck = 0
        with open(filename, mode="rb") as shufflings:
            # We will read the saved information in similar loops like we saved them in .store()
            for cardsToDecode, bitsPerCard, bytesToBeRead in zip(init.cardsToStoreEachLoop, init.bitsPerCardEachLoop, init.bytesEachLoop):
                # prepare a list for the decoded numbers (cards's reference position numbes)
                decodedNumbers = list()
                hugeInteger = int.from_bytes(shufflings.read(bytesToBeRead), byteorder="big")
                # We prepare a 6-bit filter (like a window) to read parts of the hugeInteger
                window = 2 ** bitsPerCard - 1 # binary: 111111, 11111, 1111, 111, 11
                for i in range(cardsToDecode):
                    decodedNumbers.append(hugeInteger & window)
                    hugeInteger = hugeInteger >> bitsPerCard
                # reverse the list of decoded numbers
                decodedNumbers.reverse()
                # put the cards in the loadedDeck
                for number in decodedNumbers:
                    loadedDeck.append(refDeck[number])
                # remove the loaded cards from the reference Deck
                for card in loadedDeck[cardsToSkipAtTheBeginningOfLoadedDeck:]:
                    refDeck.remove(card)
                cardsToSkipAtTheBeginningOfLoadedDeck = cardsToSkipAtTheBeginningOfLoadedDeck + cardsToDecode
        self.cards = loadedDeck

class Player():
    def __init__(self, playerName, brain, requiredCards="", requiredHandType="", requiredSeat=None):
        self.name = playerName
        self.brain = brain
        self.cards = set()
        self.requiredCards = requiredCards
        self.requiredHandType = requiredHandType
        try:
            self.requiredSeat = requiredSeat - 1 # we subtract one from the seat number because list of seats starts with 0
        except TypeError:
            self.requiredSeat = requiredSeat
    def receiveCard(self, card):
            self.cards.add(card)
    def pocketCards(self):
        # this return the cards in a list ordered by the cards' value
        return sorted(self.cards, key = lambda card: (card.value.value, card.color.value), reverse = True)
    def typePocketCards(self, parameter="short"):
        for card in self.pocketCards():
            print(card(parameter))
    def pocketPair(self):
        """returns True if cards are pocket pair, else: False"""
        return self.pocketCards()[0].value == self.pocketCards()[1].value
    def suitedCards(self):
        """returns True if cards are suited, False if off-suite"""
        return self.pocketCards()[0].color == self.pocketCards()[1].color


#next:
# Class Hand(listOfPlayers)

class Hand():
    """All steps of a hand of poker will be run by this class"""
    pass
        

class Game():
    """Currently it incorporates the rules of Texas Hold'em. We can later have a Rules() class which's instance can be given to either Game() or Dealer() to tell them how the game should be run.
The game will also have an endGameCondition (as an instance of Condition()) to tell when this game ends.
Right now this is simplified to a given numberOfHands which are played and then the game is over."""
    def __init__(self, numberOfHands):
        # number of hands is a preliminary construct, until we have implemented the custom endGameConditions properly.
        # until then, the game ends when a certain number of hands have been played.
        self.numberOfHands = numberOfHands

class Dealer():
    """dealer who runs the game of poker (tells whose turn is it), deals the cards to players and manages the pot at a table."""
    def __init__(self, deck, game, table, setOfPlayers):
        self.deck = deck
        self.game = game
        self.table = table
        self.setOfPlayers = setOfPlayers
        self.FTPNRAS = list() # of players who are forced to play but do not require any particular seat
        self.WTPNRASNFTP = list() # of players who want to play, do not require any particular seat and are not forced to play
    def invitePlayers(self):
        """This function maps players who want to join a game to a seat at the table."""
        # We will go through all seats at the table.
        # if there are any unseated players we will try to fill this seat with a player.
        # certain players are more important to get a seat than others.
        # There is four priority groups of players ranked in this order:
        # 1. FTP & RTS (players who are Forced To Play and Require This Seat)
        # 2. WTP & RTS & NFTP (players who Want To Play and Require This Seat but are Not Forced to Play)
        # 3. FTP & NRTS (players who are Forced To Play but do not Require This Seat)
        # 4. WTP & NFTP & RAS (players who Want To Play, but are Not Forced To Play and do not Require Any Seat)
        # before we seat the players, we will create the list of candidates for each seat
        for player in self.setOfPlayers:
            # if a player is forced to play and requires a particular seat, append him to the appropriate list
            if player.brain.forcedToPlay and (player.requiredSeat is not None):
                # append him to the FTPRTS list
                self.table.seat[player.requiredSeat].FTPRTS.append(player)
            # if the player wants to play, requires a particular seat, but is not forced to play
            elif player.brain.wantToJoinAGame and (player.requiredSeat is not None) and (not player.brain.forcedToPlay):
                # append him to the WTPRTSNFTP list
                self.table.seat[player.requiredSeat].WTPRTSNFTP.append(player)
            # if the player is forced to play but does not require any particular seat
            elif player.brain.forcedToPlay and (player.requiredSeat is None):
                # append him to the FTPNRAS list
                self.FTPNRAS.append(player)
            # if the player wants to play, does not require any particular seat and is not forced to play
            elif player.brain.wantToJoinAGame and (player.requiredSeat is None) and (not player.brain.forcedToPlay):
                # append him to the WTPNRASNFTP list
                self.WTPNRASNFTP.append(player)
        # each seat now has filled its lists of candidates with players who are interested in that seat.
        # go through the seats and pick a player for it from the higherst ranked list of candidates
        for thisSeat in self.table.seat:
            # find the highest ranked non-empty list:
            highestList = [x for x in [thisSeat.FTPRTS, thisSeat.WTPRTSNFTP, self.FTPNRAS, self.WTPNRASNFTP] if x != list()]
            # pick a random member of the highestList of the ranked player lists
            for aList in highestList:
                # seat the player
                thisSeat.player = random.choice(aList)
                # delete the player from the list
                aList.remove(thisSeat.player)
                # prepare the message about this player taking this seat
                m.playerTakesSeatNumberX.whatToTransmit[1] = str(thisSeat.number)
                m.playerTakesSeatNumberX.updatePlayerName(thisSeat.player)
                # transmit the message
                messenger.transmit(m.playerTakesSeatNumberX)
                break
            # empty thisSeat's candidate lists to prepare them for the next round
            thisSeat.FTPRTS = list()
            thisSeat.WTPRTSNFTP = list()
        # empty the general lists to prepare them for the next round
        self.FTPNRAS = list()
        self.WTPNRASNFTP = list()
    def letPlayersGo(self):
        # Until players get more sophisticated brains, they decide randomly whether they want to leave the table or not.
        for thisSeat in self.table.seat:
            # We have to check whether a player is sitting at this seat
            if thisSeat.player is not None:
                # let the player decide whether he wants to leave the table
                if thisSeat.player.brain.wantToLeaveAGame():
                    # update the message about player leaving the seat
                    m.playerLeavesSeatNumberX.updatePlayerName(thisSeat.player)
                    # update the seatnumber in the message
                    m.playerLeavesSeatNumberX.whatToTransmit[1] = str(thisSeat.number)
                    messenger.transmit(m.playerLeavesSeatNumberX)
                    thisSeat.player = None
    def dealCard(self, player):
        # update the message about the dealer giving this player this card.
        m.dealerGivesPlayerACard.whatToTransmit[1] = self.deck.cards[-1]()
        # take the first card from the deck and give it to the player
        player.receiveCard(self.deck.pop())
        # update the player's name in the message
        m.dealerGivesPlayerACard.updatePlayerName(player)
        # transmit the message
        messenger.transmit(m.dealerGivesPlayerACard)
    def dealCardsToAllPlayers(self):
        # Dealer deals in two rounds, each round he gives one card to each players.
        for counter in range(2):
            for player in self.table.listOfPlayersAtTheTable():
                self.dealCard(player)
    def collectAllCards(self):
        # After each hand the dealer collects all cards from the players.
        for player in self.table.listOfPlayersAtTheTable():
            while player.cards:
                self.deck.cards.append(player.cards.pop())
                # update the player name in the message
                m.dealerTakesACardFromPlayer.updatePlayerName(player)
                # update the message about this card being collected.
                m.dealerTakesACardFromPlayer.whatToTransmit[1] = self.deck.cards[-1]()
                # transmit the message
                messenger.transmit(m.dealerTakesACardFromPlayer)
        # dealer will later also collect the community cards laid out on the table (a.k.a. 'the board')
        # dealer will later also collect the cards which have been 'burned' before flop, turn, and river.
    def playAHand(self):
        # increment the hand counter
        init.counter["hand"] = init.counter["hand"] + 1
        # before we type out the number of hand which is being played we update the message:
        m.aNewHandStarts.whatToTransmit[1] = str(init.counter["hand"])
        messenger.transmit(m.aNewHandStarts)
        messenger.transmit(m.shufflingCardsPLACEHOLDER)
        self.deck.casinoShuffle()
        messenger.transmit(m.whoIsTheButtonPLACEHOLDER)
        messenger.transmit(m.placeBlindsPLACEHOLDER)
        # Dealer deals to the players
        messenger.transmit(m.dealCardsToPlayersPLACEHOLDER)
        self.dealCardsToAllPlayers()
        messenger.transmit(m.preFlopBetPLACEHOLDER)
        messenger.transmit(m.uncoverFlopPLACEHOLDER)
        messenger.transmit(m.flopBetPLACEHOLDER)
        messenger.transmit(m.uncoverTurnPLACEHOLDER)
        messenger.transmit(m.turnBetPLACEHOLDER)
        messenger.transmit(m.uncoverRiverPLACEHOLDER)
        messenger.transmit(m.riverBetPLACEHOLDER)
        messenger.transmit(m.showdownPLACEHOLDER)
        messenger.transmit(m.whoIsTheWinnerPLACEHOLDER)
        messenger.transmit(m.transferPotToWinnerPLACEHOLDER)
        # dealer collects cards from the players and the table.
        self.collectAllCards()
        messenger.transmit(m.collectCardsToDeckPLACEHOLDER)
    def playGame(self):
        # update the game counter
        init.counter["game"] = init.counter["game"] + 1
        # update the game counter in the message
        m.playingGameNumberX.whatToTransmit[1] = str(init.counter["game"])
        # transmit the message that a game is played.
        messenger.transmit(m.playingGameNumberX)
        for hand in range(self.game.numberOfHands):
            # Verbose typeout "Checking whether any players want to join the game."
            messenger.transmit(m.checkPlayersJoinGame)
            # Check for empty seats at the table and seat the players.
            self.invitePlayers()
            # Check whether there are enough players to play poker (at least 2)
            if len(self.table.listOfPlayersAtTheTable()) > 1:
                # play the hand
                # update the message about how many players want to join a game
                m.xPlayersPlayAHand.whatToTransmit[0] = str(len(self.table.listOfPlayersAtTheTable()))
                # transmit the message
                messenger.transmit(m.xPlayersPlayAHand, positionInWhatToTransmitWhichShouldBeRandomized=1)
                self.playAHand()
                messenger.transmit(m.checkPlayersLeaveGame)
                self.letPlayersGo()
            # otherwise the last remaining player will leave the table. (This mustn't be elif!)
            if len(self.table.listOfPlayersAtTheTable()) == 1:
                # we will tell his brain that he wants to leave the table
                self.table.listOfPlayersAtTheTable()[0].brain.wantToLeaveTheTable = True
                # update the player's name in the message
                m.lastPlayerHasLeft.updatePlayerName(self.table.listOfPlayersAtTheTable()[0])
                # transmit the message that the player has left the table
                messenger.transmit(m.lastPlayerHasLeft)
                self.letPlayersGo()
            # otherwise the game is over (This mustn't be elif!)
            if len(self.table.listOfPlayersAtTheTable()) == 0:
                break
        # reset the hand counter
        init.counter["hand"] = 0
        # update the game counter in the message
        m.endingGameNumberX.whatToTransmit[1] = str(init.counter["game"])
        messenger.transmit(m.endingGameNumberX)

class Seat():
    """A seat will keep track of the players who are interested in taking it.
    It will distiguish between different groups of players, ranked by the importance of their presence at the table."""
    def __init__(self, number, player):
        self.number = number # technically, we are storing the seat number twice. Once as an index of the list table.seat and then here. /-:
        self.FTPRTS = list() # list of players who are forced to play and require this seat
        self.WTPRTSNFTP = list() # list of players who want to play, require this seat but are not forced to play
        # [list of players who are forced to play but do not require any particular seat] will not be stored in any seat since it is the same list for every seat. This list will be generated externally.
        # [list of players who want to play, do not require any particular seat and are not forced to play] will not be stored in any seat since it is the same list for every seat. This list will be generated externally.
        self.player = None

class Table():
    """A table has a limited number of seats for the players and it holds the community cards, a.k.a. 'the board'.
It also inherently has a dealer who deals the cards to players and manages the pot."""
    def __init__(self, numberOfSeats):
        self.numberOfSeats = numberOfSeats
        # listof seats at the poker table (later used for mapping Players to seat numbers)
        self.seat = [Seat(x + 1, None) for x in range(self.numberOfSeats)]
    def listOfPlayersAtTheTable(self):
        """This returns the list of players currently sitting at the table and playing"""
        #listOfPlayersPlayingAtTheTable = list()
        return [thisSeat.player for thisSeat in self.seat if thisSeat.player is not None]
        #for thisSeat in self.seat:
        #    if thisSeat.player is not None:
        #        listOfPlayersPlayingAtTheTable.append(thisSeat.player)
        #return listOfPlayersPlayingAtTheTable

class Requirements():
    def __init__(self, sessionRequirements):
        """This will parse one <session> tag in requirement.xml and store the required things in self."""
        self.sessionRequirements = sessionRequirements
        # create a game with the given number of hands
        try:
            numberOfHandsToPlay = int(self.sessionRequirements.find("game").attrib["hands"])
        except KeyError:
            numberOfHandsToPlay = init.numberOfHandsToPlay
        self.game = Game(numberOfHandsToPlay)
        # create a table with the given number of seats
        try:
            numberOfSeatsAtTable = int(self.sessionRequirements.find("table").attrib["seats"])
        except KeyError:
            numberOfSeatsAtTable = init.numberOfSeatsAtTable
        self.table = Table(numberOfSeatsAtTable)
        # read or create a set of players
        self.setOfPlayers = set()
        try:
            for player in self.sessionRequirements.find("players"):
                # if it finds a player, check whether player's name and brain, hand, handType, seat is defined
                try:
                    playerName = player.attrib["name"]
                except KeyError:
                    playerName = random.sample(init.setOfPlayerNames, 1)[0]
                try:
                    forcedToPlay = bool(player.attrib["forcedToPlay"])
                except KeyError:
                    forcedToPlay = init.forcedToPlay
                try:
                    playerBrain = player.attrib["brain"]
                except KeyError:
                    playerBrain = dictionaryOfBrains[init.playerBrain](forcedToPlay)
                try:
                    hand = player.attrib["hand"]
                except KeyError:
                    hand = ""
                try:
                    handType = player.attrib["handType"]
                except KeyError:
                    handType = ""
                try:
                    seat = int(player.attrib["seat"])
                except KeyError:
                    seat = None
                self.setOfPlayers.add(Player(playerName, playerBrain, requiredCards=hand, requiredHandType=handType, requiredSeat=seat))
        except:
            # if no set of players is specified, take the default set of players
            for playerName in init.setOfPlayerNames:
                self.setOfPlayers.add(Player(playerName, dictionaryOfBrains[init.playerBrain]()))

####################
## ACTUAL PROGRAM ##
####################

if __name__ == "__main__":
    # create a deck of cards
    deckOfCards = Deck()
    # create a dictionary of brains
    dictionaryOfBrains = dict(inspect.getmembers(brain, predicate=inspect.isclass))
    if init.shuffleOnly:
        # shuffle the deck
        deckOfCards.casinoShuffle()
        deckOfCards.store()
        deckOfCards.readFromFile()
    elif init.requiredHands:
        # parse the requirements.xml ("requirements.xml" is stored in init.requiredHands)
        tree = ElementTree.parse(init.requiredHands)
        try:
            for session in tree.getroot():
                requirements = Requirements(session)
                # create the dealer for the session as required:
                dealer = Dealer(deckOfCards, requirements.game, requirements.table, requirements.setOfPlayers)
                # run the session
                messenger.transmit(m.aNewRunStarts)
                dealer.playGame()
        except KeyError:
            # update the name of requirements.xml in the message:
            m.couldNotParseRequirements.whatToTransmit[1] = init.requiredHands
            # transmit a message that you could not parse requirements.xml
            messenger.transmit(m.couldNotParseRequirements)
    else:
        # create a set of players interested in a game of poker at a particular table
        setOfPlayers = set()
        
        # create players
        for name in init.setOfPlayerNames:
            setOfPlayers.add(Player(name, brain.allIn()))
        
        # define the number of hands to be played
        numberOfHands = 20000
        
        # create game
        game = Game(numberOfHands)
        
        # define the number of seats at the poker table
        numberOfSeats = 9
        
        # create a table
        table = Table(numberOfSeats)
        
        # create a dealer and give him the deck of cards.
        dealer = Dealer(deckOfCards, game, table, setOfPlayers)
        
        # run the game
        messenger.transmit(m.aNewRunStarts)
        dealer.playGame()
