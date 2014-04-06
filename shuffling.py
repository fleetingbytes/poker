#!/usr/bin/python
# -*- coding: UTF_8 -*-

# until I find out how to generate realistic riffles, I have created a setOfMixes which contains
# some riffle patterns sampled from my own shuffling

import itertools

class Mix():
    def __init__(self, upper, lower, lowerStarts):
        # When riffling the cards, the deck is divided in two more or less equal halves.
        # Then one drops cards from the two halves, ideally one by one, zipping the two halves together.
        # The upper half is a list of single-digit numbers, keeping record of how many cards from this half are dropped in each zip step.
        self.upper = list(map(lambda x: int(x), list(str(upper))))
        #self.upper.reverse()
        # and the lower half (analogous to the upper)
        self.lower = list(map(lambda x: int(x), list(str(lower))))
        #self.lower.reverse()
        # one of the halves starts
        self.lowerStarts = lowerStarts
        self.halves = dict(zip([True, False], [self.lower, self.upper]))
    def __iter__(self):
        # we must know which half comes first and which comes second
        if self.lowerStarts:
            first = True
        else:
            first = False
        second = not first
        # zip the two halves together
        zippedHalves = list()
        for one, two in zip(self.halves[first], self.halves[second]):
            zippedHalves.extend([one, two])
        # sometimes one half is longer than the other
        lowerHalfLen = len(self.halves[True])
        upperHalfLen = len(self.halves[False])
        if lowerHalfLen != upperHalfLen:
            # in this case we must additionally append the last element of the longer half
            zippedHalves.append(self.halves[lowerHalfLen > upperHalfLen][-1])
        # create list of tuples (n, bool) where n is the number of cards to be dropped
        # and bool designates the lower (True) or upper (False) half.
        cycle = itertools.cycle([first, second])
        listOfTuples = list()
        for n in zippedHalves:
            listOfTuples.append((n, next(cycle)))
        return iter(listOfTuples)

listOfPatterns = [Mix(231122122131211212, 1211121111111112111, True),
                  Mix(262121131211122, 232211221121121, True),
                  Mix(3221122111124321, 21111111111122213, True), 
                  Mix(11111211211113134, 2522121112112111, False), 
                  Mix(3112212111112222, 31211111111122116, True), 
                  Mix(2131322112112141, 2111122212221121, True), 
                  Mix(11132121211222127, 3111111111112112, False), 
                  Mix(1121111112112142121, 3131111111111121112, True), 
                  Mix(3111111112111226, 2112112212221222, True), 
                  Mix(41111211111121216, 2113112212111221, False)
                  ]

if __name__ == "__main__":
    pass