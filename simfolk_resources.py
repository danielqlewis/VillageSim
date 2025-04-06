import random
from program_enums import FoodCollectionMethod


class TaskAssignment:
    def __init__(self, task_type, sub_info):
        self.task_type = task_type
        self.sub_info = sub_info


class SimfolkResource:
    def __init__(self):
        self.meal_skipped = False
        self.assigned_task = None

        self.collection_aptitudes = {
            FoodCollectionMethod.GATHER: random.choice([x for x in range(1, 25)]),
            FoodCollectionMethod.HUNT: random.choice([x for x in range(1, 25)]),
            FoodCollectionMethod.FISH: random.choice([x for x in range(1, 25)]),
            FoodCollectionMethod.TRAP: random.choice([x for x in range(1, 25)])
        }


    def get_collection_preferences(self):
        ordered_keys = list(FoodCollectionMethod)
        values = [self.collection_aptitudes.get(key, 0) for key in ordered_keys]
        total = sum(values)
        if total == 0:
            return [1 / len(values)] * len(values)  # fallback to equal distribution
        return [v / total for v in values]

    def level_up_aptitude(self, apt):
        if self.collection_aptitudes[apt] < 100:
            self.collection_aptitudes[apt] += 1

    @staticmethod
    def gather_water():
        return 24 + random.choice([x for x in range(-4, 5)])

    def gather_food(self, collection_method):
        base_success_dict = {FoodCollectionMethod.GATHER: 75,
                             FoodCollectionMethod.HUNT: 30,
                             FoodCollectionMethod.FISH: 50,
                             FoodCollectionMethod.TRAP: 55
                             }
        base_amount_dict = {FoodCollectionMethod.GATHER: 12,
                            FoodCollectionMethod.HUNT: 42,
                            FoodCollectionMethod.FISH: 22,
                            FoodCollectionMethod.TRAP: 16
                            }
        base_success_rate = base_success_dict[collection_method]
        active_success_rate = (base_success_rate + self.collection_aptitudes[collection_method]) / 2
        success_roll = random.choice([x for x in range(1, 101)])
        if success_roll <= active_success_rate:
            level_up_roll = random.choice([True, False])
            if level_up_roll:
                self.level_up_aptitude(collection_method)
            return base_amount_dict[collection_method] + (self.collection_aptitudes[collection_method] // 10)
        else:
            return 0