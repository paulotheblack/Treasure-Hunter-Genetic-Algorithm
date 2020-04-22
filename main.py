from helper import *


# prvych 2 zoberiem, a presuniem ich do novej generacii (elitisti)
# prvych 70 skrizim (hybridi) s urcitou pravedpodobnostou (30%)
# prvych 70 zmutujem (mutanti) s pravdepodobnostou (1:70, teda priemerne jeden mutant na generaciu) a potom tu pravdepodobnost mierne zvysujem
# 28 jedincov nahodne vygenerujem

# "Tournament  selection scheme  has been  used between  two individuals and uniform crossover is applied
# on two individuals with probability of 0.8. Mutation is applied on a gene of an
# individual with  probability of 1/number of  variables. Generational
# without elitism replacement scheme is used and population  size  is determined  as  100. "

# hunters.sort(key=lambda hunters: hunters[2], reverse=True)


def main():
    print('Treasure Hunter v1.1')
    board, start_position, treasures_total = generate_board()
    board_info = [board, start_position, treasures_total]
    # print(board)

    year = 0
    gen = get_randoms(100, board_info)
    gen = sorted(gen, reverse=True)

    while True:
        elite = get_elite(gen)
        hybrids = get_hybrids(60, gen, board_info) # mutacia vznika az potomkovy
        mutants = get_mutants(hybrids, board_info)
        randoms = get_randoms(30, board_info)

        gen.clear()
        gen = elite[:] + hybrids[:] + mutants[:] + randoms[:]
        gen = sorted(gen, reverse=True)

        year += 1
        if year % 1000 == 0:
            print('Year: ' + str(year))
            print('Population: ' + str(len(gen)))
            test_print(gen[:10])
            # choice = input('continue?(y/n): ')
            # if choice == 'y':
            #     year = 0


if __name__ == '__main__':
    main()
