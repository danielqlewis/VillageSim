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
        return 18

    def gather_food(self, collection_method):
        base_success_dict = {FoodCollectionMethod.GATHER: 60,
                             FoodCollectionMethod.HUNT: 20,
                             FoodCollectionMethod.FISH: 40,
                             FoodCollectionMethod.TRAP: 45
                             }
        base_amount_dict = {FoodCollectionMethod.GATHER: 8,
                            FoodCollectionMethod.HUNT: 32,
                            FoodCollectionMethod.FISH: 16,
                            FoodCollectionMethod.TRAP: 12
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