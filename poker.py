#!/usr/bin/python
# -*- coding: UTF_8 -*-

# How to debug this:
# set path to Python27
# run cmd in winpdb dir, then start winpdb by "python winpdb.py"
# set path to Python34
# run a new instance of cmd from the dir of poker.py
# type "python <winpdb dir>rpdb2.py -pahoj -d poker.py" (password is "ahoj"
# type 'python "y:\sven\My Dropbox\Dropbox\python\winpdb\rpdb2.py" -pahoj -d poker.py'
# we need the following keypress routine in order to attach the script to the winpdb debugger (workaround for a bug in rpdb2.py)

import msvcrt
#msvcrt.getch()

import random
import init
import brain
import messenger as m
from enum import Enum
from lib import rndint # needed for true random shuffle of the deck of cards
from optparse import OptionParser

# Shortcuts and aliases:
messenger = m.messenger

# OptionParser will parse command line argumenty
parser = OptionParser(usage="%prog", version="%prog 0.0.2", prog="Poker Pie")
parser.add_option("-v", "--verbose",dest="verbose", default=True, action="store_true", help="Report internal stuff")
parser.add_option("-n", "--nolog", dest="log", default=True, action="store_false", help="Don't log")
(options,args) = parser.parse_args()

init.verbose = options.verbose
init.log = options.log

# If logging is enabled, create the necessary files:
if init.log:
    # general log file
    logfile = open("log.txt", mode="a", encoding="UTF_8")
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
    spades = 4
    hearts = 3
    diamonds = 2
    clubs = 1

cardColors = dict(zip((CardColor.spades, CardColor.hearts, CardColor.diamonds, CardColor.clubs), ("S", "H", "D", "C")))

# Pocket cards:
# AKs = A and K of the same color (s = suited)

class Card():
    def __init__(self, value, color):
        self.value = value
        self.color = color
    def __call__(self, parameter="short"):
        if parameter == "short":
            return cardNames[self.value] + cardColors[self.color]
        if parameter == "text":
            return self.value.name + " of " + self.color.name

class Deck:
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
            Δ = 0
        else:
            µ = 35.5 # [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
            Δ = 16
        σ = 2.2
        cardsTaken = 0
        while (cardsTaken < (15 + Δ)) or (cardsTaken > (24 + Δ)):
            cardsTaken = random.gauss(µ, σ)
        cardsTaken = int(round(cardsTaken, 0))
        self.cards = self.cards[cardsTaken:] + self.cards[:cardsTaken]
    def shuffl(self, method):
        pass
    def shuffle(self, shufflingSequence):
        # shufflingSequence is a list of shuffling methods, e.g. [wash, riffle, riffle, box, riffle, cut]
        for method in shufflingSequence:
            self.shuffl(self.cards)
    def randomOrgShuffle(self):
        # Seed Random Generator with true Random Value ans shuffle list
        # random.seed(rndint.get(0, len(self.cards), 1).pop())
        # random.shuffle(self.cards)
        # rndint.get function reference: https://code.google.com/p/pyrndorg/source/browse/trunk/rndint.py?r=2
        pass
    def pop(self):
        return self.cards.pop()

class Player():
    def __init__(self, playerName, brain, wantsToJoinAGame=True, wantsToLeaveAGame=False):
        self.name = playerName
        self.brain = brain
        self.cards = set()
        self.wantsToJoinAGame = wantsToJoinAGame
        self.wantsToLeaveAGame = wantsToLeaveAGame
    def receiveCard(self, card):
            self.cards.add(card)
    def pocketCards(self):
        # this will print the player's cards ordered
        return sorted(self.cards, key = lambda card: (card.value.value, card.color.value), reverse = True)
    def typePocketCards(self, parameter="short"):
        for card in self.pocketCards():
            print(card(parameter))
    def pocketPair(self):
        return self.pocketCards()[0].value == self.pocketCards()[1].value
    def suitedCards(self):
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
    def invitePlayers(self):
        """This function maps players who want to join a game to a free seat at the table."""
        # from the set of all players we make a list of players who want to join a game.
        listOfPlayersToJoinAGame = list()
        for player in self.setOfPlayers:
            if player.wantsToJoinAGame:
                listOfPlayersToJoinAGame.append(player)
        # update the message about how many players want to join a game
        m.xPlayersWantToJoinAGame.whatToTransmit[0] = str(len(listOfPlayersToJoinAGame))
        # transmit the message
        messenger.transmit(m.xPlayersWantToJoinAGame, positionInWhatToTransmitWhichShouldBeRandomized=1)
        # since we want the players to be seated at the table randomly, we will shuffle this list
        random.shuffle(listOfPlayersToJoinAGame)
        # for each player taking a seat at the table we will put him into the table's seats dictionary
        # and transmit a message saying which player took which seat
        for (player, seatNumber) in zip(listOfPlayersToJoinAGame, self.table.setOfEmptySeats()):
            self.table.seats[seatNumber] = player
            # update the message about player taking a seat
            m.playerTakesSeatNumberX.updatePlayerName(player)
            # update the seatnumber in the message
            m.playerTakesSeatNumberX.whatToTransmit[1] = str(seatNumber)
            messenger.transmit(m.playerTakesSeatNumberX)
    def letPlayersGo(self):
        # Until players get more sophisticated brains, they decide randomly whether they want to leave the table or not.
        for seatNumber, player in self.table.seats.items():
            # We have to check whether a player is sitting at this seat
            if player is not None:
            # let the player decide whether he wants to leave the table
                player.brain.wantToLeaveTheTable = player.brain.tossACoin()
                if player.brain.wantToLeaveTheTable:
                    self.table.seats[seatNumber] = None
                    # update the message about player leaving the seat
                    m.playerLeavesSeatNumberX.updatePlayerName(player)
                    # update the seatnumber in the message
                    m.playerLeavesSeatNumberX.whatToTransmit[1] = str(seatNumber)
                    messenger.transmit(m.playerLeavesSeatNumberX)
    def dealCard(self, player):
        # later we should only use player.receiveCard(self.deck.pop())
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
                # later we should only use self.deck.cards.append(player.cards.pop())
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
        self.deck.cut()
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
        # update the game counter in the message
        m.endingGameNumberX.whatToTransmit[1] = str(init.counter["game"])
        messenger.transmit(m.endingGameNumberX)

class Table():
    """A table has a limited number of seats for the players and it holds the community cards, a.k.a. 'the board'.
It also inherently has a dealer who deals the cards to players and manages the pot."""
    def __init__(self, numberOfSeats):
        self.numberOfSeats = numberOfSeats
        # dictionary of seats at the poker table (later used for mapping Players to seat numbers)
        self.seats = dict(map(lambda x: (x + 1, None), range(numberOfSeats)))
    def setOfEmptySeats(self):
        """This will check how many empty seats are there.
It returns a list of seat numbers, e.g. [2, 3, 5, 8, 9]
(used when inviting players to the table, etc.)"""
        emptySeats = set()
        for seatNumber, player in self.seats.items():
            if player is None:
                emptySeats.add(seatNumber)
        return emptySeats # as a list of seat numbers, e.g. [2, 3, 5, 8, 9]
    def listOfPlayersAtTheTable(self):
        """This returns the list of players currently sitting at the table and playing"""
        listOfPlayersPlayingAtTheTable = list()
        for seatNumber, player in self.seats.items():
            if player is not None:
                listOfPlayersPlayingAtTheTable.append(player)
        return listOfPlayersPlayingAtTheTable
    def sortedListOfPlayers(self):
        # create a list of players sorted according to the seat number they have taken
        # search for a seat which is not empty, add the player sitting there to the list
        sortedListOfPlayers = list()
        for i in range(self.seats.values()):
            if self.seats[i] is not None:
                sortedListOfPlayers.append(seats[i])
        return sortedListOfPlayers

####################
## ACTUAL PROGRAM ##
####################

if __name__ == "__main__":
    # create a deck of cards
    deckOfCards = Deck()
    
    # create a set of players interested in a game of poker at a particular table
    setOfPlayers = set()
    
    # create players
    setOfPlayerNames = set(["Bob", "Quinn", "Jeff", "Lewis", "Sven", "John", "Mary", "Marc", "Gary", "Marlana", "Blanch", "Cathey", "Bruno", "Violeta", "Barton", "Fran", "Hubert", "Barbara", "Nydia", "Cinda", "Enid", "Dalton", "Shae", "Verda", "Tomas", "Terina", "Robin", "Pricilla", "Melba", "Suzan", "Johna", "Shawanda", "Rema", "Madeleine", "Sherilyn", "Lyndsay", "Sau", "Monserrate", "Denice", "Ramonita", "Kenyetta", "Cara", "Caryl", "Olga", "Rosenda", "Lorene", "Kellie", "Myrl", "Carleen", "Porter", "Laurine", "Lucila", "Felisha", "Candace", "Dagny", "Temple", "Lacey", "Estela", "Alexis"])
    for name in setOfPlayerNames:
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