class Const:
    POPULATION_Q = 100
    RANDOM_Q = int(POPULATION_Q/3)
    ELITE_Q = 0
    TOURNAMENT_Q = int(2 * POPULATION_Q / 3)
    ROULETTE_Q = int(2 * POPULATION_Q / 3)
    MUTATION_PROB = 0.05  # 0 > prob > 1

    @staticmethod
    def print_settings():
        print('# ----------------------------------- #' +
              '\n| Treasure Hunter: UI 3b xpaulovicm1  |' +
              '\n# ----------------------------------- #' +
              '\nBoard settings => ./input.conf' +
              '\nWorld settings => ./constants.py' +
              '\nPopulation size: ' + str(Const.POPULATION_Q) +
              '\nElites: ' + str(Const.ELITE_Q) +
              '\nChildren (tournament): ' + str(Const.TOURNAMENT_Q) +
              '\nChildren (roulette): ' + str(Const.ROULETTE_Q) +
              '\nNew blood: ' + str(Const.RANDOM_Q) +
              '\nMutation probability: ' + str(Const.MUTATION_PROB))

