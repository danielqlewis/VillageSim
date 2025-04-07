from program_enums import FoodCollectionMethod


class SimulationParams:
    # Start Conditions parameters
    STARTING_POPULATION = 12
    STARTING_WATER = 25
    STARTING_FOOD = 35

    # End Conditions parameters
    MAX_POPULATION = 250
    MAX_DAYS = 300

    # Reproduction parameters
    BASE_REPRODUCTION_CHANCE = 50
    REPRODUCTION_BONUS_CUTOFF = 20

    # Resource collection parameters
    COLLECTION_BASE_SUCCESS = {FoodCollectionMethod.GATHER: 75,
                               FoodCollectionMethod.HUNT: 30,
                               FoodCollectionMethod.FISH: 50,
                               FoodCollectionMethod.TRAP: 55}
    COLLECTION_BASE_AMOUNT = {FoodCollectionMethod.GATHER: 12,
                              FoodCollectionMethod.HUNT: 42,
                              FoodCollectionMethod.FISH: 22,
                              FoodCollectionMethod.TRAP: 16}
