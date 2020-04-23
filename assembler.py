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


# Predstavuje entitu jedneho hladaca pokladov
# Kazdy hladac ma svoj vlastny stroj
class Assembler:
    def __init__(self, memory, board):
        self.memory = memory  # pamat jedinca
        self.board = copy.deepcopy(board[0])  # kopia hracej dosky
        self.position = copy.deepcopy(board[1])  # kopia startovacej pozicie
        self.treasures_total = board[2]  # celkovy pocet pokladov
        self.treasures_found = 0
        self.route = []  # cesta akou sa hladac pohyboval po hracej doske
        self.fitness = 0
        self.stderr = 'None'  # sposob ukoncenia
        self.orig_memory = copy.deepcopy(memory)  # nezmenena pamat jedinca, vyuzivana pri krizeni

    # sposob sortovania: podla fitness
    def __lt__(self, other):
        return self.fitness < other.fitness

    # Hladacov program
    def run(self):
        program_counter = 0

        for clock in range(500):
            # zistenie instrukcie a adresy/hodnoty z aktualnej bunky pamate
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

    # funckia "vypisu" / pohybu na hracej doske
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
                return 666  # --<Move Out of Index>--

        # LEFT
        if direction == 2:
            if self.position[1] != 0:
                self.position[1] -= 1
                self.route.append('L')
            else:
                return 666  # --<Move Out of Index>--

        # RIGHT
        if direction == 3:
            if self.position[1] != len(self.board[1]) - 1:
                self.position[1] += 1
                self.route.append('R')
            else:
                return 666  # --<Move Out of Index>--

        # Check for treasure
        if self.board[(self.position[0], self.position[1])] == 1:
            # Oznacenie policka ako najdeneho pokladu
            # zabranuje repetivnosti
            self.board[(self.position[0], self.position[1])] = 5
            self.treasures_found += 1
            return 0

        # Vizualizacie pohybu na hracej doske
        if self.board[(self.position[0], self.position[1])] != 5:
            # Oznacenie policka ako navstiveneho
            self.board[(self.position[0], self.position[1])] = 3
        return 0  # Successful move

    # Vypocet fitness funkcie
    def get_fitness(self):
        return 1 + self.treasures_found - len(self.route) / 1000
