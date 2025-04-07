import random


def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]


def jitter_tuple(t):
    return tuple(x + random.choice([-1, 0, 1]) if x != 0 else 0 for x in t)
