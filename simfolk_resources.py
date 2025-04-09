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
        self.collection_aptitudes = {method: random.randint(1, 24) for method in FoodCollectionMethod}


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
        return 24 + random.randint(-4, 4)

    def gather_food(self, collection_method, params):
        active_aptitude = self.collection_aptitudes[collection_method]
        base_success_rate = params.COLLECTION_BASE_SUCCESS[collection_method]
        active_success_rate = (base_success_rate + active_aptitude) / 2

        if random.randint(1, 100) <= active_success_rate:
            level_up_roll = random.choice([True, False])
            if level_up_roll:
                self.level_up_aptitude(collection_method)
            return params.COLLECTION_BASE_AMOUNT[collection_method] + (active_aptitude // 10), level_up_roll
        else:
            return 0, False