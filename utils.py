import random


def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]
