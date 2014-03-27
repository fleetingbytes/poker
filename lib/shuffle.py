import random #temp

# Fisher–Yates shuffle algorythm
# no true randomness yet

def shuffle(list):

    for i in reversed(range(1, len(list)-1)):
        j = random.randint(0, i)
        list[i], list[j] = list[j], list[i]
    return list

if __name__ == "__main__":
    pass
