#!/usr/bin/python
# -*- coding: UTF_8 -*-

# This will serve as a global configuration file

import sys

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

if __name__ == "__main__":
    pass
