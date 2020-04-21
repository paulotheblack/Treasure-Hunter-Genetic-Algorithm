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
    def __init__(self, memory, board, start_position, treasures_total):
        self.memory = memory # generate_memory() # TODO refactor according to assigment
        self.board = copy.deepcopy(board)  # copy gameboard -> to be able to grab the treasure
        self.position = start_position
        self.treasures_total = treasures_total
        self.treasures_found = 0
        self.route = []
        self.last_move = 'None'


    # return:
    # @type of exit: <-> skus sa pohrat s hodnotami pri sortingu
    #     0 -> all treasures found
    #     1 -> 500 iterations done
    #     2 -> out of index
    # @treasures_found -> cim viac tym lepsie
    # @route -> mnozstvo krokov
    # IK: sort by Treasures found + Moves made
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
                    self.route.append(self.last_move)

                    # --<Found all treasures>--
                    if self.treasures_found == self.treasures_total:
                        return 0, self.treasures_found, self.route, self.kap_fitness()
                else:  # --<Out of Index>--
                    return 2, self.treasures_found, self.route, self.kap_fitness()

        # --<Terminated after 500>--
        return 1, self.treasures_found, self.route, self.kap_fitness()

    def mov(self, address):
        direction = address & 0b000011

        # UP
        if direction == 0:
            if self.position[0] == 0:
                return 666  # --<Move Out of Index>--
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
            # mark tile as already found treasure
            self.board[(self.position[0], self.position[1])] = 5
            self.treasures_found += 1
        return 0

    def paulo_fitness(self):
        bounty = self.treasures_found / self.treasures_total
        if len(self.route) != 0:
            return (bounty / len(self.route))*100
        return 0

    # move
    def kap_fitness(self):
        return (1 + self.treasures_found - len(self.route)/1000)
