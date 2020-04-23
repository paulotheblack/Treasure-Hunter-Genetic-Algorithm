"""
Michal Paulovic
FIIT STU 2020
UI Z-3b
url: http://www2.fiit.stuba.sk/~kapustik/poklad.html
"""
import numpy as np
import random
import copy
from assembler import Assembler
from constants import Const
import matplotlib.pyplot as plot

# Vygenerovanie hracej dosky zo suboru ./input.conf
# struktura suboru:
# rozmer hracej dosky (m, n): 7 7
# startovanice pozicia (m, n): 6 3
# pocet pokladov: 4
# adresy pokladov (m, n): ...
def generate_board():
    config = open('input.conf', 'r')

    # get array size
    buffer = config.readline().split()
    arr_size = convert(buffer)
    # generate board
    board = np.zeros(arr_size)

    # get starting point
    buffer = config.readline().split()
    start_position = convert(buffer)
    # create start point == 9
    board[start_position[0], start_position[1]] = 9

    # get no. of treasures
    buffer = config.readline().split()
    treasures_no = convert(buffer)

    # get all treasure's coordinates
    treasures_indexes = []
    for element in range(treasures_no):
        buffer = config.readline().split()
        index = convert(buffer)
        treasures_indexes.append(index)
    # insert treasures
    for treasure in treasures_indexes:
        board[treasure[0], treasure[1]] = 1

    config.close()
    return board, start_position, treasures_no


# convert to 'int' if digit
def convert(arr):
    if len(arr) != 1:
        digit_arr = []
        for char in arr:
            if char.isdigit():
                _char = int(char)
                digit_arr.append(_char)
        return digit_arr
    else:
        return int(arr[0])


# get position of desired element
def get_position(array, element):
    _position = np.where(array == element)
    position = list(zip(_position[0], _position[1]))

    if len(position) == 1:
        return position[0]
    return position

# ----------------------------------------- #
#           Memory manipulation             #
# ----------------------------------------- #
# Vygenerovanie nahodnej pamate 64 buniek (0, 255)
def generate_memory():
    memory = []
    for i in range(64):
        cell = random.randint(0b00000000, 0b11111111)
        memory.append(cell)
    return memory

# Krizenie (nezmenych) pamati rodicov
def memory_cross(parents):
    child_memory = []
    x_chrom = parents[0].orig_memory[:32]
    for cell in x_chrom:
        child_memory.append(cell)

    y_chrom = parents[1].orig_memory[32:]
    for cell in y_chrom:
        child_memory.append(cell)
    return child_memory

# ----------------------------------------- #
#               Miscellaneous               #
# ----------------------------------------- #
# Vyber rodicov turnaj
def tournament(generation):
    parents = []
    for i in range(2):
        # Vyberie 2 nahodnych jedincov z celej generacie
        _parents = random.choices(generation, k=2)
        # Porovna fitness a ten "lepsi" sa stava rodicom
        _parents.sort(reverse=True)
        parents.append(_parents[0])
    return parents

# Vyber rodicov ruleta
def roulette(generation):
    # Z celej generacie vybera 2 nahodnych
    # (s pridanou vahou, cim vyssia fitness tym vacsia pravdepodobnost vyberu jedinca)
    return random.choices(generation, weights=[hunter.fitness for hunter in generation], k=2)

# Zbehnutie programu pre celu generaciu a zoradenie podla fitness
def search_board(generation):
    for hunter in generation:
        hunter.run()
    return sorted(generation, reverse=True)

# Overenie ci niektory hladac nasiel vsetky poklady
def get_result(generation, year):
    for hunter in generation:
        if hunter.stderr == 'Found all treasures':
            winner(hunter, year)
            return 0

def winner(hunter, year):
    print('\nHello I am the winner')
    print('Found ' + str(hunter.treasures_found) + ' treasures' +
          ' in ' + str(len(hunter.route)) + ' steps')
    print('My journey: ' + str(hunter.route))
    print('My fitness: ' + str(hunter.fitness))
    print('Year: ' + str(year))
    print(hunter.board)

# ----------------------------------------- #
#           Population management           #
# ----------------------------------------- #
# Ziskanie nahodnych jedincov
def get_randoms(quantity, board):
    randoms = []
    for i in range(quantity):
        hunter = Assembler(generate_memory(), board)
        randoms.append(hunter)
    return randoms

# pomocna funkcia pre krizenie
def get_children(typ, generation, board):
    if typ == 0:
        return get_children_tournament(Const.TOURNAMENT_Q, generation, board)
    else: return get_children_roulette(Const.ROULETTE_Q, generation, board)

# Krizenie Turnaj
def get_children_tournament(quantity, generation, board):
    children = []
    for i in range(quantity):
        parents = tournament(generation)
        child_memory = memory_cross(parents)
        child = Assembler(child_memory, board)
        children.append(child)
    return children

# Krizenie ruleta
def get_children_roulette(quantity, generation, board):
    children = []
    for i in range(quantity):
        parents = roulette(generation)
        child_memory = memory_cross(parents)
        child = Assembler(child_memory, board)
        children.append(child)
    return children

# Elitny jedincy
def get_elite(generation, board):
    elits = []
    _elits = generation[:Const.ELITE_Q]
    for hunter in _elits:
        elite_hunter = Assembler(hunter.orig_memory, board)
        elits.append(elite_hunter)
    return elits

# Mutacia pri krizemie
# Kazda druha bunka pamate je generovana nahodne (k povodnej pamati)
# povodny jedinec je vyradeny a do novej generacie je priradeny len mutant
def get_mutants(generation, board):
    mutation = []
    for hunter in generation:
        if random.uniform(0, 1) <= Const.MUTATION_PROB:
            enchanted_memory = copy.deepcopy(hunter.orig_memory)
            for i in range (64):
                if i % 2 == 0:
                    enchanted_memory[i] = random.randint(0b00000000, 0b11111111)
            generation.remove(hunter)
            mutant = Assembler(enchanted_memory, board)
            mutation.append(mutant)
    return mutation

# ----------------------------------------- #
#               Plotting misc.              #
#           by default turned off           #
#       becuase of matplotlib dependency    #
# ----------------------------------------- #
def generation_fitness(generation):
    fitness = 0
    for hunter in generation:
        fitness += hunter.fitness
    return fitness/len(generation)


def fitness_plot(population_fitness, years):
    try:
        plot.plot(years, population_fitness)
        plot.xlabel('year')
        plot.ylabel('fitness')
        plot.show()
    except ModuleNotFoundError as e:
        print(e)
        print('Not supported for plotting')