"""
Michal Paulovic
FIIT STU 2020
UI Z-3b
url: http://www2.fiit.stuba.sk/~kapustik/poklad.html
"""
import numpy as np
import random


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
    return board, treasures_no, start_position


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


# get instruction, value
# TODO check if correct
def parse_cell(cell):
    instruction = cell >> 6
    address = cell & 0b001111
    return instruction, address

