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


# ------------------------------------------ #
def get_randoms(quantity, board_info):
    randoms = []
    for i in range(quantity):
        hunter = Assembler(generate_memory(), board_info[0], board_info[1], board_info[2]).run()
        randoms.append(hunter)
    return randoms


def memory_cross(x, y):
    child_memory = []
    _x = x[:32]
    for cell in _x:
        child_memory.append(cell)
    _y = y[32:]
    for cell in _y:
        child_memory.append(cell)
    return child_memory


def get_hybrids(quantity, parents, board_info):
    x = 0  # index of first
    y = 1  # index of second
    hybrids = []
    while x <= quantity:
        if random.uniform(0, 1) <= 0.3:
            child_memory = memory_cross(parents[x].memory, parents[y].memory)
            # RUN AND SEARCH BOARD
            child = Assembler(child_memory, board_info[0], board_info[1], board_info[2]).run()
            hybrids.append(child)
        else:
            hybrids.append(parents[x])
            hybrids.append(parents[y])
        x += 2
        y += 2

    return hybrids


def get_elite(parents):
    return parents[:2]


def get_mutants(parents, board_info):
    mutation = []
    for hunter in parents:
        if random.uniform(0, 1) >= 0.7:
            enchanted_memory = copy.deepcopy(hunter.memory)
            enchanted_memory[random.randint(0, 63)] += 1

            mutant = Assembler(enchanted_memory, board_info[0], board_info[1], board_info[2]).run()
            mutation.append(mutant)
    return mutation


def test_print(generation): # generation = list(hunters)
    print('# -------------------------------- #')
    for hunter in generation:
        print('Treas: ' + str(hunter.treasures_found)
              + ' Steps: ' + str(len(hunter.route))
              + ' IQ: ' + str(hunter.fitness))
