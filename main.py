from helper import *


def world(plt):
    board, start_position, treasures_total = generate_board()
    board_info = [board, start_position, treasures_total]

    # Vyber sposobu ziskania rodicov pre krizenie
    typ = input('Tournament: 0, Roulette: 1: => ')

    year = 0
    _years = []
    population_fitness = []

    # Generovanie 1.generacie hladacov pokladov
    generation = get_randoms(Const.POPULATION_Q, board_info)
    # Kazdy hladac zbehne svoj virtualny stroj
    generation = search_board(generation)
    # Zoradenie podla fitness funkcie
    generation.sort(reverse=True)

    while True:
        # Zistenie, ci niektory z hladacov nasiel vsetky poklady
        if get_result(generation, year) == 0:
            # PLOTTING
            if plt == 'y' and year >= 100:
                fitness_plot(population_fitness, _years)
            return

        # Elitarizmus, najlepsich presuniem do novej generacie
        # pocet: ${Const.ELITE_Q}
        elites = get_elite(generation, board_info)

        # Krizenie podla zvoleneho typu (Turnaj/Ruleta)
        # pocet: ${Const.TOURNAMENT_Q} || ${Const.ROULETTE_Q}
        children = get_children(typ, generation, board_info)

        # Mutacia jedinca (len z krizencov 'children')
        # pravdepodobnost: ${Const.MUTATION_PROB}
        mutants = get_mutants(children, board_info)

        # Nova krv pre dalsiu generaciu
        # pocet: ${Const.RANDOM_Q}
        randoms = get_randoms(Const.RANDOM_Q, board_info)

        # Vymazanie povodnej generacie (neuspesnej)
        generation.clear()

        # Vytvorenie, spustenie a zoradenie novej generacie
        generation = elites[:] + children[:] + mutants[:] + randoms[:]
        generation = search_board(generation)
        generation.sort(reverse=True)

        year += 1

        # Plotting, not used by default.
        if year % 50 == 0:
            _years.append(year)
            gen_fitness = generation_fitness(generation)
            population_fitness.append(gen_fitness)

        if year % 10000 == 0:
            if input('10 000 years passed. Quit? (y/n) ') == 'y':
                return


def main():
    Const.print_settings()
    x = 0
    while x < 1:
        # Plotting of fitness function (requires matplotlib installed, or to be run in Pycharm IDE).
        # default is 'n'
        # plt = 'n'
        plt = input('\nDo you want to see plot of fitness function? (y/n) ')

        world(plt)
        if input('\nDo you want to be the God one more time? (y/n) ') == 'y':
            x = 0
        else:
            print('Goodbye!')
            exit(0)


if __name__ == '__main__':
    main()
