from helper import generate_memory, parse_cell
import copy

"""
------- # ------------ #
 cell   | inst | value |
------- # ------------ #
    Instruction set    #
---------------------- #
  Increment 00 XXXXXX  |
  Decrement 01 XXXXXX  |
  Jump      10 XXXXXX  |
  Print     11 XXXXXX  |
---------------------- #
"""


class Assembler:
    def __init__(self, board, start_position, treasures_total):
        self.memory = generate_memory()
        self.last_move = 'None'
        self.route = []
        self.treasures_found = 0
        self.board = copy.deepcopy(board)  # game board
        self.position = start_position
        self.treasures_total = treasures_total


    # return:
    # @type of exit: <-> skus sa pohrat s hodnotami pri sortingu
    #     0 -> all treasures found
    #     1 -> 500 iterations done
    #     2 -> out of index
    # @treasures_found -> cim viac tym lepsie
    # @route -> ?
    def run(self):
        program_counter = 0

        for steps in range(500):
            instruction, address = parse_cell(self.memory[program_counter])

            if instruction == 0:  # INC
                self.memory[address] += 1
                program_counter += 1
            if instruction == 1:  # DEC
                self.memory[address] -= 1
                program_counter += 1
            if instruction == 2:  # JMP
                program_counter = address
            if instruction == 3:  # MOV
                if self.mov(address) != 666:
                    program_counter = address + 1
                    self.route.append(self.last_move)

                    # Check if all treasures have been found
                    if self.treasures_found == self.treasures_total:
                        return 0, self.treasures_found, self.route
                else:  # --<Out of Index>--
                    return 2, self.treasures_found, self.route

        # --<Terminated after 500>--
        return 1, self.treasures_found, self.route

    def mov(self, address):
        direction = address & 0b000011

        # UP
        if direction == 0:
            if self.position[0] == 0:
                return 666
            self.position[0] -= 1
            self.last_move = 'U'  # TEST

        # DOWN
        if direction == 1:
            if self.position[0] == len(self.board) - 1:
                return 666
            self.position[0] += 1
            self.last_move = 'D'  # TEST

        # LEFT
        if direction == 2:
            if self.position[1] == 0:
                return 666
            self.position[1] -= 1
            self.last_move = 'L'  # TEST

        # RIGHT
        if direction == 3:
            if self.position[1] == (len(self.board[1]) - 1):
                return 666
            self.position[1] += 1
            self.last_move = 'R'  # TEST

        # Check for treasure
        if self.board[(self.position[0], self.position[1])] == 1:
            # osetri, ze repetetivnost
            # deepcopy boardu ==> prepisovat hodnotu
            self.board[(self.position[0], self.position[1])] = 5
            self.treasures_found += 1
        return 0
