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
import sys


# get config of board, generate board
# return board, treasures_indexes, start_position
# TODO implement '#' to stop reading => comment config file
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
# return array or int (depends of @par arr)
def convert(arr):
    if len(arr) != 1:
        digit_arr = []
        for char in arr:
            if char.isdigit():
                _char = int(char)
                digit_arr.append(_char)
        return digit_arr
    else:  # TODO check if correct (may return string)
        return int(arr[0])


# get position of desired element
def get_position(array, element):
    _position = np.where(array == element)
    position = list(zip(_position[0], _position[1]))

    if len(position) == 1:
        return position[0]
    return position


# ------------------------------------------ #
# random 64-memory cells (0, 255)
def generate_memory():
    memory = []
    for i in range(64):
        cell = random.randint(0b00000000, 0b11111111)
        memory.append(cell)
    return memory


# board_info = [board, start_position, treasures_total]
# Assembler(memory, board, start_position, treasures_total)
# ------------------------------------------ #
def get_randoms(quantity, board):
    randoms = []
    for i in range(quantity):
        hunter = Assembler(generate_memory(), board)
        randoms.append(hunter)
    return randoms



def search_board(generation):
    for hunter in generation:
        hunter.run()
    return sorted(generation, reverse=True)


def get_result(generation, year):
    for hunter in generation:
        if hunter.stderr == 'Found all treasures':
            winner(hunter, year)
            return 0
            #     sys.exit('Job done')  # continue? --> N
            # else: return 1  # continue --> Y


def memory_cross(parents):
    child_memory = []
    x_chrom = parents[0].orig_memory[:32]
    for cell in x_chrom:
        child_memory.append(cell)

    y_chrom = parents[1].orig_memory[32:]
    for cell in y_chrom:
        child_memory.append(cell)
    return child_memory


def tournament(generation):
    parents = []
    # get 2 random parents
    for i in range(2):
        _parents = random.choices(generation, k=2)
        _parents.sort(reverse=True)
        parents.append(_parents[0])
    return parents


def roulette(generation):
    return random.choices(generation, weights=[hunter.fitness for hunter in generation], k=2)


def get_children(typ, generation, board):
    if typ == 0:
        return get_children_tournament(Const.TOURNAMENT_Q, generation, board)
    else: return get_children_roulette(Const.ROULETTE_Q, generation, board)


def get_children_tournament(quantity, generation, board):
    children = []
    for i in range(quantity):
        parents = tournament(generation)
        child_memory = memory_cross(parents)
        child = Assembler(child_memory, board)
        children.append(child)
    return children


def get_children_roulette(quantity, generation, board):
    children = []
    for i in range(quantity):
        parents = roulette(generation)
        child_memory = memory_cross(parents)
        child = Assembler(child_memory, board)
        children.append(child)
    return children


def get_elite(parents, board):
    elits = []
    _elits = parents[:Const.ELITE_Q]
    for hunter in _elits:
        elite_hunter = Assembler(hunter.orig_memory, board)
        elits.append(elite_hunter)
    return elits


# zmen kazdu druhu bunku v memory!!!
def get_mutants(parents, board):
    mutation = []
    for hunter in parents:
        if random.uniform(0, 1) <= Const.MUTATION_PROB:
            mutate_index = random.randint(0, 63)
            enchanted_memory = copy.deepcopy(hunter.memory)
            enchanted_memory[mutate_index] += 1
            mutant = Assembler(enchanted_memory, board)
            mutation.append(mutant)
    return mutation


# ------------------------------------------ #
def generation_fitness(generation):
    fitness = 0

    for hunter in generation:
        fitness += hunter.fitness
    return fitness/len(generation)


def fitness_plot(population_fitness, years):
    plot.plot(years, population_fitness)
    plot.xlabel('year')
    plot.ylabel('fitness')
    plot.show()


def test_print(generation):
    print('# -------------------------------- #')
    for hunter in generation:
        print('Treasures: ' + str(hunter.treasures_found) +
              ' Steps: ' + str(len(hunter.route)) +
              ' IQ: ' + str(hunter.fitness))


def winner(hunter, year):
    print('\nHello I am the winner')
    print('I found ' + str(hunter.treasures_found) + ' treasures' +
          ' in ' + str(len(hunter.route)) + ' steps')
    print('My journey: ' + str(hunter.route))
    print('My iQ: ' + str(hunter.fitness))
    print('Year: ' + str(year))
    print(hunter.board)
    # if input('continue?(y/n) ') == 'y':
    #     return 1
    # else: return 0
