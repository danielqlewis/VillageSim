import random
import utils
from simfolk_base import Simfolk
from name_generator import generate_name
from enums import FolkGender, TaskType, TaskAssignment, FoodCollectionMethod


# Define name banks (or import from a separate file)
MALE_NAME_BANK = ["James", "John", "Robert", "Michael", "William"]  # Expand as needed
FEMALE_NAME_BANK = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth"]  # Expand as needed
SURNAME_NAME_BANK = ["Smith", "Johnson", "Williams", "Jones", "Brown"]  # Expand as needed


class Village:
    def __init__(self, params):
        self.population = []
        self.food_store = params.STARTING_FOOD
        self.water_store = params.STARTING_WATER
        self.params = params

    def add_simfolk(self, simfolk):
        for existing_sf in self.population:
            simfolk.social.create_relationship(existing_sf)
            existing_sf.social.create_relationship(simfolk)
        self.population.append(simfolk)

    def remove_simfolk(self, simfolk):
        if simfolk in self.population:
            self.population.remove(simfolk)

    def generate_new_simfolk(self, day, parents, age=0):
        child_gender = random.choice([FolkGender.MALE, FolkGender.FEMALE])
        child_name, child_postnomial = generate_name(self.population, child_gender, parents)
        child_simfolk = Simfolk(child_name, child_gender, day % 7, child_postnomial)
        if age != 0:
            child_simfolk.age = age
        self.add_simfolk(child_simfolk)

    def auto_assign_tasks(self):
        workforce = [sf for sf in self.population if sf.age > 16]
        population = len(self.population)

        # A) Assign people to collect water based on how much is available
        if population == 0 or len(workforce) == 0:
            return  # nothing to do

        water_threshold = 4 * population

        if self.water_store >= water_threshold:
            num_for_water = 0
        elif self.water_store == 0:
            num_for_water = max(1, population // 10)
        else:
            # Linearly interpolate
            fraction = 1 - (self.water_store / water_threshold)
            num_for_water = max(1, round(fraction * (population / 10)))

        num_for_water = min(len(workforce), num_for_water)

        water_workers = random.sample(workforce, num_for_water)
        for worker in water_workers:
            worker.resources.assigned_task = TaskAssignment(TaskType.WATER_COLLECT, None)

        # B) Assign remaining workers to collect food
        remaining_workers = [sf for sf in workforce if sf not in water_workers]

        if remaining_workers:
            food_threshold = 5 * population

            if self.food_store >= food_threshold:
                num_for_food = 0
            elif self.food_store == 0:
                num_for_food = max(1, population)
            else:
                # Linearly interpolate
                fraction = 1 - (self.food_store / food_threshold)
                num_for_food = max(1, round(fraction * population))

            number_to_assign = max(1, min(len(remaining_workers), num_for_food))

            food_workers = random.sample(remaining_workers, number_to_assign)

            for worker in food_workers:
                method_preferences = worker.resources.get_collection_preferences()
                method = utils.weighted_choice(list(FoodCollectionMethod), method_preferences)
                worker.resources.assigned_task = TaskAssignment(TaskType.FOOD_COLLECT, method)


    def handle_social_interactions(self):
        # Process all social interactions for the day
        pass

    def collect_resources(self):
        # Gather resources based on assignments
        pass

    def consume_resources(self):
        # Use food and water
        pass

    def handle_population_events(self):
        # Births, deaths, etc.
        pass