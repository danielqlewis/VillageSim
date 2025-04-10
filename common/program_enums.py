from enum import Enum


class TaskType(Enum):
    WATER_COLLECT = 0
    FOOD_COLLECT = 1


class FoodCollectionMethod(Enum):
    GATHER = 0
    HUNT = 1
    FISH = 2
    TRAP = 3


class FolkGender(Enum):
    MALE = 0
    FEMALE = 1


class InteractionAttributes(Enum):
    COOPERATIVE = 0
    COMMUNICATIVE = 1
    FUN = 2
    INTIMATE = 3
    COMBATIVE = 4
    SKILL = 5
    RECREATION = 6


class DeathCause(Enum):
    AGE = 0
    THIRST = 1
    HUNGER = 2


class InteractionType(Enum):
    TALK = 0
    SHARE_FOOD = 1
    GAME = 2
    SPORT = 3
    MAKE_ART = 4
    WRESTLE = 5
    DEBATE = 6
    ARGUE = 7
    FIGHT = 8
    LOUNGE = 9
    CUDDLE = 10
    MATE = 11