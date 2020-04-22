import copy
import sys

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


def parse_cell(cell):
    instruction = cell >> 6
    address = cell & 0b001111
    return instruction, address


class Assembler:
    def __init__(self, memory, board):
        self.memory = memory
        self.board = copy.deepcopy(board[0])  # copy gameboard -> to be able to grab the treasure
        self.position = copy.deepcopy(board[1])
        self.treasures_total = board[2]
        self.treasures_found = 0
        self.route = []
        self.fitness = 0
        self.stderr = 'None'
        self.orig_memory = copy.deepcopy(memory)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def run(self):
        program_counter = 0

        for clock in range(500):
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
                    if self.treasures_found == self.treasures_total:  # --<Found all treasures>--
                        self.fitness = self.get_fitness()
                        self.stderr = 'Found all treasures'
                        return self

                else:  # --<Out of Index>--
                    self.fitness = self.get_fitness()
                    self.stderr = 'Out of Index'
                    return self

        self.fitness = self.get_fitness()
        self.stderr = '500 Iterations'
        return self  # --<Terminated after 500>--

    def mov(self, address):
        _instruction, _address = parse_cell(self.memory[address])
        direction = _address & 0b000011

        # UP
        if direction == 0:
            if self.position[0] != 0:
                self.position[0] -= 1
                self.route.append('U')
            else:
                return 666  # --<Move Out of Index>--

        # DOWN
        if direction == 1:
            if self.position[0] != len(self.board) - 1:
                self.position[0] += 1
                self.route.append('D')
            else:
                return 666

        # LEFT
        if direction == 2:
            if self.position[1] != 0:
                self.position[1] -= 1
                self.route.append('L')
            else:
                return 666

        # RIGHT
        if direction == 3:
            if self.position[1] != len(self.board[1]) - 1:
                self.position[1] += 1
                self.route.append('R')
            else:
                return 666

        # Check for treasure
        if self.board[(self.position[0], self.position[1])] == 1:
            # mark tile as already found treasure
            self.board[(self.position[0], self.position[1])] = 5
            self.treasures_found += 1
            return 0

        # visualize movement, do not overwrite found treasure with another step on tile
        if self.board[(self.position[0], self.position[1])] != 5:
            self.board[(self.position[0], self.position[1])] = 3
        return 0  # Successful move

    def get_fitness(self):
        return 1 + self.treasures_found - len(self.route) / 1000
