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
    def __init__(self, whatToTransmit, listOfPossibleWordings, separatorOfMsgChunks, transmitOnlyIfVerboseWanted, whereToTransmitThisTo, playerName="DefaultName"):
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
    def transmit(self, positionInWhatToTransmitWhichShouldBeRandomized=0):
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
    def transmit(self, message):
        message.transmit()
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

messenger = Messenger()
