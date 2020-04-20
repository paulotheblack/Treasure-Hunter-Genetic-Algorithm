from helper import *
from assembler import *


def main():
    print('Treasure Hunter by Mike v0.1')
    board, treasures_total, start_position = generate_board()
    print(board)

    hunters = []

    for i in range(100):
        exit, treasures, route = Assembler(board, start_position, treasures_total).run()
        hunters.append([exit, treasures, len(route), Assembler])

    # TODO sort by 2 values
    # ---------------------------
    # sorted(list, key=lambda x: (x[0], -x[1]))
    # ----------------------------
    # import operator
    # list1 = sorted(csv1, key=operator.itemgetter(1, 2))
    hunters.sort(key = lambda hunters: hunters[1], reverse=True)

    for el in hunters:
        print(  'exit: ' +  str(el[0]) +
               ' treas: ' + str(el[1]) +
               ' moves: ' + str(el[2]))

if __name__ == '__main__':
    main()
