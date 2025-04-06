import random
import utils
from simfolk_base import Simfolk
from name_generator import generate_name
from program_enums import FolkGender, TaskType, TaskAssignment, FoodCollectionMethod


class Village:
    def __init__(self, params):
        self.population = []
        self.food_store = params.STARTING_FOOD
        self.water_store = params.STARTING_WATER
        self.params = params
        self.pending_births = []

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

    def night_reset(self):
        self.pending_births = []
        for sf in self.population:
            sf.step_reset()

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

    def _resolve_reproduction(self, parents):
        roll = random.choice([x for x in range(100)])
        if roll < self.params.BASE_REPRODUCTION_CHANCE:
            if parents[0].gender != parents[1].gender:
                self.pending_births.append(parents)

    def handle_social_interactions(self):
        available_simfolk = [sf for sf in self.population if sf.resources.assigned_task is None]
        interacted_pairs = set()

        if len(available_simfolk) > 1:
            proposed_interactions = []
            for sf in available_simfolk:
                proposal = sf.social.propose_interaction([s for s in available_simfolk if s != sf])
                if proposal:
                    proposed_interactions.append(proposal)

            for interaction in proposed_interactions:
                if interaction.initiator.social_interaction_count >= 3:
                    pass
                elif interaction.target.social_interaction_count >= 3:
                    pass
                elif (interaction.initiator, interaction.target) in interacted_pairs:
                    pass
                else:
                    interaction_success = interaction.target.consider_proposal(interaction.initiator, interaction)
                    if interaction_success:
                        interaction.initiator.social_interaction_count += 1
                        interaction.target.social_interaction_count += 1
                        interacted_pairs.add((interaction.initiator, interaction.target))
                        interacted_pairs.add((interaction.target, interaction.initiator))
                        interaction.resolve()
                        if interaction.interaction_type is Mate:
                            self._resolve_reproduction([interaction.initiator, interaction.target])

                    for observer in [sf for sf in available_simfolk if sf != interaction.initiator and sf != interaction.target]:
                        relationship_with_initiator = observer.relationships[interaction.initiator]
                        relationship_with_target = observer.relationships[interaction.target]
                        if interaction_success:
                            initiator_influence_list = []
                            target_influence_list = []
                            for interaction_attribute in interaction.interaction_type.interaction_attributes:
                                local_influence = InteractionAttributeToInfluenceDict[interaction_attribute]
                                initiator_influence_list.append(local_influence.on_initiator)
                                target_influence_list.append(local_influence.on_target)
                            influence_towards_initiator = tuple(sum(x) for x in zip(*initiator_influence_list))
                            influence_towards_target = tuple(sum(x) for x in zip(*target_influence_list))
                        else:
                            influence_towards_initiator = (0, 2, -2, 0)
                            influence_towards_target = (2, 0, 0, -2)

                        influence_towards_initiator = tuple(x + random.choice([-1, 0, 1]) if x != 0 else 0 for x in influence_towards_initiator)
                        influence_towards_target = tuple(x + random.choice([-1, 0, 1]) if x != 0 else 0 for x in influence_towards_target)

                        relationship_with_initiator.update(influence_towards_initiator)
                        relationship_with_target.update(influence_towards_target)

    def collect_resources(self):
        for sf in self.population:
            if sf.resources.assigned_task is not None:
                if sf.resources.assigned_task.task_type == TaskType.WATER_COLLECT:
                    self.water_store += sf.resources.gather_water()
                elif sf.resources.assigned_task.task_type == TaskType.FOOD_COLLECT:
                    collection_result = sf.resources.gather_food(sf.resources.assigned_task.sub_info)
                    self.food_store += collection_result
                    modifier_magnitude = 1 + (sf.resources.collection_aptitudes[sf.resources.assigned_task.sub_info] // 18)
                    if collection_result == 0:
                        relationship_mod = (0, 0, -modifier_magnitude, 0)
                    else:
                        relationship_mod = (0, 0, modifier_magnitude, 0)
                    for bystander in [s for s in self.population if s != sf]:
                        bystander.social.relationships[sf].update(relationship_mod)

    def pay_upkeep(self, day):
        for sf in self.population:
            water_cost = sf.get_water_cost(day)
            if water_cost > self.water_store:
                thirst_flip = random.choice([True, False])
                if not thirst_flip:
                    self.remove_simfolk(sf)
            self.water_store = max(self.water_store - water_cost, 0)

            food_cost = sf.get_food_cost()
            if food_cost > self.food_store:
                if sf.resources.meal_skipped:
                    starve_roll = utils.weighted_choice([True, False], [.25, .75])
                    if not starve_roll:
                        self.remove_simfolk(sf)
                else:
                    sf.resources.meal_skipped = True
            else:
                sf.resources.meal_skipped = False
            self.food_store = max(self.food_store - food_cost, 0)

    def _handle_births(self, day):
        for parents in self.pending_births:
            self.generate_new_simfolk(day, parents)

    def _handle_aging(self, day):
        for sf in list(self.population):
            if day % 7 == sf.birthday:
                sf.age += 1
            death_chance = max(0, (sf.age - 60) / 100)  # Starts at age 60, increases by 1% per year
            if random.random() < death_chance:
                self.remove_simfolk(sf)


    def handle_population_events(self, day):
        self._handle_births(day)
        self._handle_aging(day)