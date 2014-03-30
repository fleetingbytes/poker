#!/usr/bin/python
# -*- coding: UTF_8 -*-

# This module will take care about typing out all kinds of messages during the whole run of the program.
# Messages are objects, instances of Message().
# When creating a message object, you'll define its string (and its possible wordings, just for variety)
# and also define the places where you want this message to be typed out, 
# e.g. certain messages you'll only want to read in the log file, certain messages you'll want to read only on the screen while the 
# program is running, certain messages you'll want to appear in both places.

# The Messenger() is there to manage the reporting in a more global way, e.g. disabling it totally (for automated long runs of the program)

import init, random, time

class Message():
    def __init__(self, whatToTransmit, listOfPossibleWordings, separatorOfMsgChunks, transmitOnlyIfVerboseWanted, whereToTransmitThisTo, playerName="PLAYERNAME", positionInWhatToTransmitWhichShouldBeRandomized=0):
        # whatToTransmit is a list of message chunks, some of which will have placeholders or be picked from a list of possible wordings (see self.transmit())
        self.whatToTransmit = whatToTransmit
        self.listOfPossibleWordings = listOfPossibleWordings
        self.separatorOfMsgChunks = separatorOfMsgChunks
        # Some messages will be transmitted "everytime", some will only be transmitted if "verbose" is enabled.
        # whenToTransmitThis keeps track of this for each message.
        self.transmitOnlyIfVerboseWanted = transmitOnlyIfVerboseWanted
        # Some messages will be transmitted (printed) only in the log file, some will only be printed on the screen, 
        # some will be printed on both of them.
        # whereToTransmitThisTo keeps track of this for each message.
        # whereToTransmitThisTo is a set
        self.whereToTransmitThisTo = whereToTransmitThisTo
        self.playerName = playerName
        self.positionInWhatToTransmitWhichShouldBeRandomized = positionInWhatToTransmitWhichShouldBeRandomized
    def updatePlayerName(self, player):
        """Needed to replace the PLAYERNAME placeholder with a player's name."""
        self.playerName = player.name
    def transmit(self, positionInWhatToTransmitWhichShouldBeRandomized):
        # whatToTransmit is a list of message chunks, some of which will have placeholders or be picked from a list of possible wordings (see self.transmit())
        # pick a random wording from the listOfPossibleWordings
        self.whatToTransmit[positionInWhatToTransmitWhichShouldBeRandomized] = random.choice(self.listOfPossibleWordings)
        # Sometimes the player's name will be used in the message. This will ensure that its placeholder will be replaced by the player's name.
        textOfTheMessage = self.separatorOfMsgChunks.join(self.whatToTransmit).replace("PLAYERNAME", self.playerName).replace("TIMESTAMP", time.strftime("%Y-%m-%d-%a %H:%M:%S"))
        # Before the message is typed out, we need to see whether it's appropriate to type it at all:
        #                                verbose wanted         verbose not wanted
        #                                (init.verbose = True)  (init.verbose = False)
        # this message is vebrose:       typeout                don't typeout
        # this message is a regular one: typeout                typeout
        # Typeout a message only if it's wanted:
        if not (self.transmitOnlyIfVerboseWanted and not init.verbose):
            # Transmit this message to every tarted in the list of targets
            for target in self.whereToTransmitThisTo:
                print(textOfTheMessage, file=target)

class Messenger():
    def __init__(self):
        pass
    def transmit(self, message, positionInWhatToTransmitWhichShouldBeRandomized=0):
        message.transmit(positionInWhatToTransmitWhichShouldBeRandomized)
    def disableAllMessages():
        """This is a shortcut for disabling all messages. Instead of letting each message be typed to init.Nowhere() (/dev/null),
        we abort typing the message here at this very beginning by redefining the function self.transmit()"""
        # make a new function transmit which does nothing
        def transmit(self, nothing=None):
            pass
        # replace the old one with this new one
        self.transmit = transmit

# Shortcuts to make creation of messages more readable:
everywhere = init.msgTarget.values() # message will be typed on screen and in the log file
logOnly = [init.msgTarget["logfile"]] # message will be typed only into the log file
screenOnly = [init.msgTarget["screen"]] # message will be typed only into the log file
onlyIfVerbose = True # message will be typed only if verbose messages are wanted.
everytime = False # message will be typed everytime (as long as messages are enabled at all)


# Create messages which will be used throughout the course of the program

aNewRunStarts = Message(["TO BE REPLACED BY A NEWLINE", "____", "TIMESTAMP", "Program starts"], 
                        [""], "\n", everytime, everywhere)
aNewHandStarts = Message(["Starting hand number ", "NUMBER", "."],
                         ["Starting hand number "], "", everytime, everywhere)

shufflingCardsPLACEHOLDER = Message(["Shuffling cards."],
                                    ["Shuffling cards.",
                                     "Cards are being shuffled.",
                                     "It's about time to shuffle the cards again.",
                                     "Let's shuffle the cards."], " ", everytime, everywhere)

whoIsTheButtonPLACEHOLDER = Message(["Determining who is on the button."],
                                    ["Determining who is on the button."], " ", everytime, everywhere)

placeBlindsPLACEHOLDER = Message(["Placing blinds."],
                                 ["Placing blinds."], " ", everytime, everywhere)

dealCardsToPlayersPLACEHOLDER = Message(["Deal cards to the players."],
                                        ["Deal cards to the players."], " ", everytime, everywhere)

preFlopBetPLACEHOLDER = Message(["Pre-flop bet, move money to the pot."],
                                ["Pre-flop bet, move money to the pot."], " ", everytime, everywhere)

uncoverFlopPLACEHOLDER = Message(["Burn one card and uncover the flop."],
                                 ["Burn one card and uncover the flop."], " ", everytime, everywhere)

flopBetPLACEHOLDER = Message(["Flop bet, move money to the pot."],
                             ["Flop bet, move money to the pot."], " ", everytime, everywhere)

uncoverTurnPLACEHOLDER = Message(["Burn one card and uncover the turn."],
                                 ["Burn one card and uncover the turn."], " ", everytime, everywhere)

turnBetPLACEHOLDER = Message(["Turn bet, move money to the pot."],
                             ["Turn bet, move money to the pot."], " ", everytime, everywhere)

uncoverRiverPLACEHOLDER = Message(["Burn one card and uncover the river."],
                                  ["Burn one card and uncover the river."], " ", everytime, everywhere)

riverBetPLACEHOLDER = Message(["River bet, move money to the pot."],
                              ["River bet, move money to the pot."], " ", everytime, everywhere)

showdownPLACEHOLDER = Message(["Optional showdown."],
                              ["Optional showdown."], " ", everytime, everywhere)

whoIsTheWinnerPLACEHOLDER = Message(["Determine who is the winner."],
                                    ["Determine who is the winner."], " ", everytime, everywhere)

transferPotToWinnerPLACEHOLDER = Message(["Transfer the pot to the winner."],
                                         ["Transfer the pot to the winner."], " ", everytime, everywhere)

collectCardsToDeckPLACEHOLDER = Message(["Collect the cards to the deck."],
                                        ["Collect the cards to the deck."], " ", everytime, everywhere)

xPlayersWantToJoinAGame = Message(["NUMBER", "players want to join a game."],
                                  ["players want to join a game."], " ", everytime, everywhere)

playerTakesSeatNumberX = Message(["PLAYERNAME takes seat number ", "SEATNUMBER", "."],
                                 ["PLAYERNAME takes seat number "], "", everytime, everywhere)

playerLeavesSeatNumberX = Message(["PLAYERNAME has vacated seat number ", "SEATNUMBER", "."],
                                  ["PLAYERNAME has vacated seat number "], "", everytime, everywhere)

playingGameNumberX = Message(["Playing game number ", "GAMENUMBER", "."],
                             ["Playing game number "], "", everytime, everywhere)

endingGameNumberX = Message(["Game number ", "GAMENUMBER", " is over and all players have left the table."],
                            ["Game number "], "", everytime, everywhere)

checkPlayersJoinGame = Message(["Checking whether any players want to join the game."], 
                               ["Checking whether any players want to join the game."], " ", everytime, everywhere)

xPlayersPlayAHand = Message(["NUMBER", "players play a hand."],
                            ["players play a hand."], " ", everytime, everywhere)

checkPlayersLeaveGame = Message(["Checking whether any players want to leave the game."], 
                                ["Checking whether any players want to leave the game."], " ", everytime, everywhere)

lastPlayerHasLeft = Message(["Last remaining player (PLAYERNAME) has left the table."],
                            ["Last remaining player (PLAYERNAME) has left the table."], " ", everytime, everywhere)

messenger = Messenger()
