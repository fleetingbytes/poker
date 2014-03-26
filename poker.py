#!/usr/bin/python
# -*- coding: UTF_8 -*-

from enum import Enum
import random

# TODO:
# seat the players at the table etc.
# Nagi's avatar on github
# Testing password management

# Requirements
# Comparison table for pocket cards strength. (for 2-9 players)
# Query: e.g. got 3 cards of one color after flop. What's the probability of a flush., Got three of a kind, how probably can someone has a full house.
# Play of 2-9 players. Each player will get a "brain" (poker strategy algorithm).
# Be able to randomly generate players

# Card names:
# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
class CardValue(Enum):
    ace = 13
    king = 12
    queen = 11
    jack = 10
    ten = 9
    nine = 8
    eight = 7
    seven = 6
    six = 5
    five = 4
    four = 3
    trey = 2
    deuce = 1

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
    def shuffl(self, method):
        pass
    def shuffle(self, shufflingSequence):
        # shufflingSequence is a list of shuffling methods, e.g. [wash, riffle, riffle, box, riffle, cut]
        for method in shufflingSequence:
            self.shuffl(self.cards)
    def deal(self, player):
        player.giveCard(self.cards.pop())

class Player():
    def __init__(self, playerName, brain):
        self.name = playerName
        self.brain = brain
        self.cards = set()
    def giveCard(self, card):
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
    def __init__(self):
        pass
    def whoIsTheButton(listOfPlayers):
        pass
    def playAHand(self):
        print("**** A NEW HAND STARTS ****")
        print("* Shuffle the cards.")
        print("* Determine who is the button.")
        print("* Place blinds.")
        print("* Deal cards to the players.")
        print("* Pre-flop bet, move money to the pot.")
        print("* Burn one card and uncover the flop.")
        print("* Flop bet, move money to the pot.")
        print("* Burn one card and uncover the turn.")
        print("* Turn bet, move money to the pot.")
        print("* Burn one card and uncover the river.")
        print("* River bet, move money to the pot.")
        print("* Optional showdown.")
        print("* Determine who is the winner.")
        print("* Transfer the pot to the winner.")
        print("* Collect the cards to the deck.")

class Game():
    """All steps of a game (series of Hands) are run by this class"""
    def __init__(self, setOfPlayers, numberOfSeats, numberOfHands):
        # number of players potentially involved in this game
        self.setOfPlayers = setOfPlayers
        # dictionary of seats at the poker table (later used for mapping Players to seat numbers)
        self.seats = dict(map(lambda x: (x + 1, None), range(len(setOfPlayers))))
        self.numberOfHands = numberOfHands
    def mapPlayersToSeats(self):
        # later, we can have a comples players seating function here, for now, we'll just seat them in the order in which they are pulled out of the set
        # we will want this function to check how many empty seats are there before a Hand is played. That many players may join the game for the next hand.
        for (player, seatNumber) in zip(self.setOfPlayers, self.seats.keys()):
            self.seats[seatNumber] = player
    def playHands(self):
        for n in range(self.numberOfHands):
            print("* Checking for empty seats at the table and seating players who want to play.")
            # create a hand
            hand = Hand()
            # play the hand
            hand.playAHand()


####################
## ACTUAL PROGRAM ##
####################

# create a deck of cards
deckOfCards = Deck()

# create players
Bob = Player("Bob", "all")
Bob.giveCard(d.H8)
Bob.giveCard(d.C8)
Bob.pocketPair()
Bob.suitedCards()
Quinn = Player("Quinn", "all")
Quinn.giveCard(d.HT)
Quinn.giveCard(d.HJ)
Quinn.pocketPair()
Quinn.suitedCards()

# create a set of players
setOfPlayers = set([Bob, Quinn])

# define the number of seats at the poker table
numberOfSeats = 9

# define the number of hands to be played
numberOfHands = 4

# create game
game = Game(setOfPlayers, numberOfSeats, numberOfHands)

# run the game
game.playHands()