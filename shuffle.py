import random
from lib import rndint

# Fisher–Yates shuffle algorythm
# no true randomness yet

class RealRandom:
    max = 999
    min = 0
    size = 10000
    buffer = rndint.get(min, max, size)
    quote = False

    @staticmethod
    def getInt(rangemin = 0, rangemax = 999):
        if((len(RealRandom.buffer) == 0) and (RealRandom.quote == False)):
           RealRandom.buffer = rndint.get(RealRandom.min, RealRandom.max, RealRandom.size)

        if(RealRandom.buffer == None):
            RealRandom.quote = True

        if(RealRandom.quote):
            return random.randint(rangemin, rangemax)

        vaule = int(RealRandom.buffer.pop())

        if (rangemin != 0) and (rangemax != 999):
            return vaule
        else:
            fixedvalue = ((vaule - RealRandom.min) / (RealRandom.max - RealRandom.min)) * (rangemax - rangemin) + rangemin
            return int(fixedvalue)

    @staticmethod
    def shuffle(cards):

        for i in reversed(range(1, len(cards)-1)):
            j = RealRandom.getInt(0, i)
            cards[i], cards[j] = cards[j], cards[i]
        return cards

#if __name__ == "__main__":
#    pass
