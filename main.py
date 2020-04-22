from helper import *


def world(plt):
    board, start_position, treasures_total = generate_board()
    board_info = [board, start_position, treasures_total]

    typ = input('Tournament == 0, Roulette == 1: => ')

    year = 0
    _years = []
    population_fitness = []

    generation = get_randoms(Const.POPULATION_Q, board_info)
    generation = search_board(generation)
    generation.sort(reverse=True)

    while True:
        if get_result(generation, year) == 0:
            if plt == 'y' and year >= 100:
                fitness_plot(population_fitness, _years)
            return

        elites = get_elite(generation, board_info)

        children = get_children(typ, generation, board_info)

        mutants = get_mutants(children, board_info)
        randoms = get_randoms(Const.RANDOM_Q, board_info)

        generation.clear()

        generation = elites[:] + children[:] + mutants[:] + randoms[:]
        generation = search_board(generation)
        generation.sort(reverse=True)

        year += 1

        if year % 100 == 0:
            _years.append(year)
            # [:Const.POPULATION_Q - Const.RANDOM_Q]
            gen_fitness = generation_fitness(generation)
            population_fitness.append(gen_fitness)

        if year % 10000 == 0:
            if input('10 000 years passed. Quit? (y/n) ') == 'y':
                return


def main():
    Const.print_settings()
    x = 0
    while x < 1:
        plt = input('\nDo you want to see plot of fitness function? (y/n) ')

        world(plt)
        if input('\nDo you want to be the God one more time? (y/n) ') == 'y':
            x = 0
        else:
            print('Goodbye!')
            sys.exit(0)


if __name__ == '__main__':
    main()
