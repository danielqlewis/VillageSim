import random
import utils
from simfolk_base import Simfolk
from name_generator import generate_name
from program_enums import FolkGender, TaskType, FoodCollectionMethod, DeathCause, InteractionType
from simfolk_resources import TaskAssignment
from simfolk_social import InteractionAttributeToInfluenceDict


class Village:
    def __init__(self, params):
        self.population = []
        self.food_store = params.STARTING_FOOD
        self.water_store = params.STARTING_WATER
        self.params = params
        self.pending_births = []
        self.pending_deaths = []
        self.interacted_pairs = set()
        self.food_limit_tracker = [0, 0, 0, 0]

    def add_food(self, amount, source):
        effective_ammount = min(amount, max(60 - amount, 0))
        self.food_store += effective_ammount
        self.food_limit_tracker[source.value] += effective_ammount

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
        self.pending_deaths = []
        self.interacted_pairs = set()
        self.food_limit_tracker = [0, 0, 0, 0]
        for sf in self.population:
            sf.step_reset()

    def _assign_water_workers(self, workforce, pop_size):
        if pop_size == 0 or len(workforce) == 0:
            return  # nothing to do

        water_threshold = 4 * pop_size

        if self.water_store >= water_threshold:
            num_for_water = 0
        elif self.water_store == 0:
            num_for_water = max(1, pop_size // 10)
        else:
            # Linearly interpolate
            fraction = 1 - (self.water_store / water_threshold)
            num_for_water = max(1, round(fraction * (pop_size / 10)))

        num_for_water = min(len(workforce), num_for_water)
        return random.sample(workforce, num_for_water)

    def _assign_food_workers(self, workforce, pop_size):
        food_threshold = 5 * pop_size

        if self.food_store >= food_threshold:
            num_for_food = 0
        elif self.food_store == 0:
            num_for_food = max(1, pop_size)
        else:
            # Linearly interpolate
            fraction = 1 - (self.food_store / food_threshold)
            num_for_food = max(1, round(fraction * pop_size))

        number_to_assign = max(1, min(len(workforce), num_for_food))

        return random.sample(workforce, number_to_assign)

    def auto_assign_tasks(self):
        workforce = [sf for sf in self.population if sf.age > 16]
        population_size = len(self.population)

        water_workers = self._assign_water_workers(workforce, population_size)
        for worker in water_workers:
            worker.resources.assigned_task = TaskAssignment(TaskType.WATER_COLLECT, None)

        remaining_workers = [sf for sf in workforce if sf not in water_workers]
        if remaining_workers:
            food_workers = self._assign_food_workers(remaining_workers, population_size)

            for worker in food_workers:
                method_preferences = worker.resources.get_collection_preferences()
                method = utils.weighted_choice(list(FoodCollectionMethod), method_preferences)
                worker.resources.assigned_task = TaskAssignment(TaskType.FOOD_COLLECT, method)

    def _resolve_reproduction(self, parents):
        roll = random.choice([x for x in range(100)])
        if roll < self.params.BASE_REPRODUCTION_CHANCE:
            if parents[0].gender != parents[1].gender:
                self.pending_births.append(parents)

    @staticmethod
    def _get_interaction_proposals(reproduction_favored, available_simfolk):
        proposed_interactions = []
        for sf in available_simfolk:
            proposal = sf.propose_interaction([s for s in available_simfolk if s != sf], reproduction_favored)
            if proposal:
                proposed_interactions.append(proposal)
        return proposed_interactions

    def _check_interaction_available(self, interaction):
        if interaction.initiator.social.social_interaction_count >= 3:
            return False
        elif interaction.target.social.social_interaction_count >= 3:
            return False
        elif (interaction.initiator, interaction.target) in self.interacted_pairs:
            return False
        return True

    def _resolve_interaction(self, interaction):
        interaction.initiator.social.social_interaction_count += 1
        interaction.target.social.social_interaction_count += 1
        self.interacted_pairs.add((interaction.initiator, interaction.target))
        self.interacted_pairs.add((interaction.target, interaction.initiator))
        interaction.resolve()
        if interaction.interaction_info.interaction_type is InteractionType.MATE:
            if interaction.initiator.age > 16 and interaction.target.age > 16:
                self._resolve_reproduction([interaction.initiator, interaction.target])

    @staticmethod
    def _get_influence(direction, interaction_attributes, interaction_success):
        if interaction_success:
            influence_list = []
            for interaction_attribute in interaction_attributes:
                local_influence = InteractionAttributeToInfluenceDict[interaction_attribute]
                if direction == "initiator":
                    influence_list.append(local_influence.on_initiator)
                elif direction == "target":
                    influence_list.append(local_influence.on_target)
            return tuple(sum(x) for x in zip(*influence_list))
        else:
            if direction == "initiator":
                return tuple((0, 2, -2, 0))
            elif direction == "target":
                return tuple((2, 0, 0, -2))

    def _resolve_observer_influence(self, interaction, observer, interaction_success):
        influence_towards_initiator = self._get_influence("initiator",
                                                          interaction.interaction_info.interaction_attributes,
                                                          interaction_success)
        influence_towards_target = self._get_influence("target", interaction.interaction_info.interaction_attributes,
                                                       interaction_success)

        influence_towards_initiator = utils.jitter_tuple(influence_towards_initiator)
        influence_towards_target = utils.jitter_tuple(influence_towards_target)

        relationship_with_initiator = observer.social.relationships[interaction.initiator]
        relationship_with_target = observer.social.relationships[interaction.target]

        relationship_with_initiator.update(influence_towards_initiator)
        relationship_with_target.update(influence_towards_target)

    def _handle_single_interaction(self, interaction, reproduction_favored, available_simfolk):
        if self._check_interaction_available(interaction):
            interaction_success = interaction.target.social.consider_proposal(interaction, reproduction_favored)
            if interaction_success:
                self._resolve_interaction(interaction)

            for observer in [sf for sf in available_simfolk if sf not in [interaction.initiator, interaction.target]]:
                self._resolve_observer_influence(interaction, observer, interaction_success)

    def handle_social_interactions(self):
        available_simfolk = [sf for sf in self.population if sf.resources.assigned_task is None and sf.age > 3]
        reproduction_favored = len(self.population) <= self.params.REPRODUCTION_BONUS_CUTOFF

        if len(available_simfolk) > 1:
            proposed_interactions = self._get_interaction_proposals(reproduction_favored, available_simfolk)

            for interaction in proposed_interactions:
                self._handle_single_interaction(interaction, reproduction_favored, available_simfolk)

    def _collect_water(self, simfolk):
        self.water_store += simfolk.resources.gather_water()

    def _collect_food(self, simfolk):
        collection_result = simfolk.resources.gather_food(simfolk.resources.assigned_task.sub_info)
        self.add_food(collection_result, simfolk.resources.assigned_task.sub_info)
        modifier_magnitude = 1 + (
                simfolk.resources.collection_aptitudes[simfolk.resources.assigned_task.sub_info] // 18)
        if collection_result == 0:
            relationship_mod = (0, 0, -modifier_magnitude // 3, 0)
        else:
            relationship_mod = (0, 0, modifier_magnitude, 0)
        for bystander in [sf for sf in self.population if sf != simfolk]:
            bystander.social.relationships[simfolk].update(relationship_mod)

    def collect_resources(self):
        working_population = [sf for sf in self.population if sf.resources.assigned_task is not None and sf.age > 3]
        for simfolk in working_population:
            if simfolk.resources.assigned_task.task_type == TaskType.WATER_COLLECT:
                self._collect_water(simfolk)
            elif simfolk.resources.assigned_task.task_type == TaskType.FOOD_COLLECT:
                self._collect_food(simfolk)

    def _pay_water_upkeep(self, day):
        for sf in self.population:
            water_cost = sf.get_water_cost(day)
            if water_cost > self.water_store:
                thirst_flip = random.choice([True, False])
                if not thirst_flip:
                    self.pending_deaths.append((sf, DeathCause.THIRST))
            self.water_store = max(self.water_store - water_cost, 0)

    def _pay_food_upkeep(self):
        for sf in self.population:
            food_cost = sf.get_food_cost()
            if food_cost > self.food_store:
                if sf.resources.meal_skipped:
                    starve_roll = utils.weighted_choice([True, False], [.25, .75])
                    if not starve_roll:
                        self.pending_deaths.append((sf, DeathCause.HUNGER))
                else:
                    sf.resources.meal_skipped = True
            else:
                sf.resources.meal_skipped = False
            self.food_store = max(self.food_store - food_cost, 0)

    def pay_upkeep(self, day):
        self._pay_water_upkeep(day)
        self._pay_food_upkeep()

    def _handle_births(self, day):
        for parents in self.pending_births:
            self.generate_new_simfolk(day, parents)

    def _handle_aging(self, day):
        for sf in list(self.population):
            if day % 7 == sf.birthday:
                sf.age += 1
            death_chance = max(0, (sf.age - 60) / 100)  # Starts at age 60, increases by 1% per year
            if random.random() < death_chance:
                self.pending_deaths.append((sf, DeathCause.AGE))

    def _handle_deaths(self):
        for death in self.pending_deaths:
            self.remove_simfolk(death[0])

    def handle_population_events(self, day):
        self._handle_births(day)
        self._handle_aging(day)
        self._handle_deaths()
