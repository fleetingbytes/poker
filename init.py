#!/usr/bin/python
# -*- coding: UTF_8 -*-

# This will serve as a global configuration file

import sys, random

# If we don't want any messages, this will be the target file (like a /dev/null)
class Nowhere():
    def write(self, message):
        pass

nowhere = Nowhere()

# Verbose reporing of internal stuff
verbose = False 

# Define possible targets where messages can be typed out
msgTarget = {"screen":sys.stdout, "logfile":nowhere}

# Keep track of whether logging is enabled or disabled
log = None

# dictionary of various counters (later to be replaced by some objects for long-term statistics)
counter = dict(zip(["hand", "game"], [0, 0]))

# In messages, the default chunk of text which is randomized in the list whatToTransmit on position 0
defaultRandomizationPoition = 0

# Distribution parameters for boxing cards
boxQ1mu = 0.25846153846153846
boxQ1sigma = 0.049527080306645516
boxQ1Limit = 7
boxQ2mu = 0.3716556144862442
boxQ2sigma = 0.06414962470578507
boxQ2Limit = 6
boxQ3mu = 0.5734107387239231
boxQ3sigma = 0.11075727789906971
boxQ3Limit = 7

if __name__ == "__main__":
    for x in range(50):
        cards = 52
        box1 = round(cards*random.gauss(boxQ1mu, boxQ1sigma))
        cards = cards - box1
        box2 = round(cards*random.gauss(boxQ2mu, boxQ2sigma))
        cards = cards - box2
        box3 = round(cards*random.gauss(boxQ3mu, boxQ3sigma))
        box4 = cards - box3
        print(box1, box2, box3, box4, sum([box1, box2, box3, box4]))