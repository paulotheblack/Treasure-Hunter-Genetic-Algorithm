import random, copy


def tester():
    mem = []
    for i in range(3):
        cell = random.randint(0b00000000, 0b11111111)
        mem.append(cell)

    for i in mem:
        print(i)

    ench = mem[:]

    ench[random.randint(0, 2)] += 1

    print('-----')

    for i in ench:
        print(i)


if __name__ == '__main__':
    tester()


# turnaj - vyber dvoch nahodnych a zober toho s lepsou fitness
# zober dvoch a výber lepsiu fitness
# skriz tych dvoch
# elitarstvo - posli top jedincov bez zmeny