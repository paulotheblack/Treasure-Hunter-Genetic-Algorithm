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
    def __init__(self, memory, board, start_position, treasures_total):
        self.memory = memory
        self.board = copy.deepcopy(board)  # copy gameboard -> to be able to grab the treasure
        self.position = start_position
        self.treasures_total = treasures_total
        self.treasures_found = 0
        self.route = []
        self.fitness = 0

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
                        return self.winner()
                else:  # --<Out of Index>--
                    self.fitness = self.get_fitness()
                    return self

        self.fitness = self.get_fitness()
        return self  # --<Terminated after 500>--

    def mov(self, address):
        _instruction, _address = parse_cell(self.memory[address])
        direction = _address & 0b000011

        # UP
        if direction == 0:
            self.route.append('U')
            if self.position[0] != 0:
                self.position[0] -= 1
            else:
                return 666  # --<Move Out of Index>--

        # DOWN
        if direction == 1:
            self.route.append('D')
            if self.position[0] != len(self.board) - 1:
                self.position[0] += 1
            else:
                return 666

        # LEFT
        if direction == 2:
            self.route.append('L')
            if self.position[1] != 0:
                self.position[1] -= 1
            else:
                return 666

        # RIGHT
        if direction == 3:
            self.route.append('R')
            if self.position[1] != len(self.board[1]) - 1:
                self.position[1] += 1
            else:
                return 666

        # Check for treasure
        if self.board[(self.position[0], self.position[1])] == 1:
            # mark tile as already found treasure
            self.board[(self.position[0], self.position[1])] = 5
            self.treasures_found += 1

        return 0  # Successful move

    def get_fitness(self):
        return 1 + self.treasures_found - len(self.route) / 1000

    # move
    # def paulo_fitness(self):
    #     bounty = self.treasures_found / self.treasures_total
    #     if len(self.route) != 0:
    #         return (bounty / len(self.route)) * 100
    #     return 0

    def winner(self):
        print('Hello I am the winner')
        print('I found ' + str(self.treasures_found) + ' treasures' +
              ' in ' + str(len(self.route)) + ' steps')
        print('My journey: ' + str(self.route))
        print('My iQ: ' + str(self.fitness))
        print(self.board)
        sys.exit('Job done.')
