from enum import Enum
import random


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


MALE_NAME_BANK = ["Adam", "Alex", "Andrew", "Anthony", "Ben", "Blake", "Brian", "Caleb", "Carl", "Charles",
                  "Chris", "Cody", "Colin", "Daniel", "David", "Derek", "Dylan", "Elijah", "Eric", "Ethan",
                  "Evan", "Frank", "Gabe", "Garrett", "George", "Greg", "Henry", "Isaac", "Jack", "Jacob",
                  "James", "Jason", "Jeff", "Jeremy", "John", "Jordan", "Joseph", "Josh", "Kyle", "Liam",
                  "Lucas", "Mark", "Matt", "Michael", "Nathan", "Nick", "Noah", "Owen", "Patrick", "Ryan",
                  "Samuel", "Thomas", "Tyler", "Zach"]
FEMALE_NAME_BANK = ["Abigail", "Alice", "Amanda", "Amy", "Andrea", "Anna", "Ashley", "Beth", "Brianna", "Brooke",
                    "Caitlin", "Camilla", "Caroline", "Cassandra", "Charlotte", "Chloe", "Christina", "Claire", "Daisy",
                    "Danielle",
                    "Diana", "Elizabeth", "Emily", "Emma", "Erica", "Evelyn", "Faith", "Fiona", "Gabrielle", "Grace",
                    "Hannah", "Isabella", "Ivy", "Jacqueline", "Jane", "Jessica", "Julia", "Kaitlyn", "Katherine",
                    "Laura",
                    "Lauren", "Leah", "Lily", "Madison", "Maria", "Megan", "Natalie", "Nicole", "Olivia", "Rebecca",
                    "Samantha", "Sarah", "Sophia", "Victoria"]
SURNAME_NAME_BANK = ["Adler", "Ashford", "Blackwood", "Carrington", "Crestwell", "Darkmoor", "Davenport", "Eldridge",
                     "Fairchild", "Fenwick",
                     "Gladstone", "Greenwood", "Hargrove", "Hawthorne", "Holloway", "Kensington", "Lancaster",
                     "Lockwood", "Montgomery", "Nightingale",
                     "Norwood", "Pendleton", "Ravenshaw", "Redfern", "Sinclair", "Sterling", "Thorne", "Underwood",
                     "Vance", "Whitmore",
                     "Winchester"]


def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]


class TaskAssignment:
    def __init__(self, task_type, sub_info):
        self.task_type = task_type
        self.sub_info = sub_info


class Relationship:
    def __init__(self, respect=100, enjoyment=100, esteem=100, cooperativity=100):
        self.respect = respect  # How much respect one has for the other
        self.enjoyment = enjoyment  # How much one enjoys being around the other
        self.esteem = esteem  # How capable one thinks the other is
        self.cooperativity = cooperativity  # How valuable to the team one thinks the other is

    def update(self, aspects_delta):
        self.respect = max(0, min(1000, self.respect + aspects_delta[0]))
        self.enjoyment = max(0, min(1000, self.enjoyment + aspects_delta[1]))
        self.esteem = max(0, min(1000, self.esteem + aspects_delta[2]))
        self.cooperativity = max(0, min(1000, self.cooperativity + aspects_delta[3]))


class RelationshipModifier:
    def __init__(self, base_mod, randomization):
        self.base_mod = base_mod
        self.randomization = randomization

    def resolve(self, relationship):
        active_modification = [m + random.choice(range(a, b + 1)) for m, (a, b) in
                               zip(self.base_mod, self.randomization)]
        relationship.update(active_modification)


class InteractionAttributeObserverInfluence:
    def __init__(self, on_initiator, on_target):
        self.on_initiator = on_initiator
        self.on_target = on_target


talk_init_mod = RelationshipModifier((10, 0, 0, 10), ((-20, 20), (-15, 15), (-10, 10), (-10, 10)))
talk_target_mod = RelationshipModifier((10, 0, 0, 10), ((-20, 20), (-15, 15), (-10, 10), (-10, 10)))

share_food_init_mod = RelationshipModifier((0, 20, 0, 0), ((0, 0), (-5, 5), (0, 0), (-5, 10)))
share_food_target_mod = RelationshipModifier((0, 20, 10, 10), ((0, 0), (-5, 5), (0, 0), (-5, 10)))

game_init_mod = RelationshipModifier((10, 25, 0, 0), ((-5, 5), (-20, 10), (0, 15), (0, 10)))
game_target_mod = RelationshipModifier((0, 25, 0, -10), ((-5, 5), (-20, 10), (0, 15), (0, 10)))

sport_init_mod = RelationshipModifier((20, 10, 10, 10), ((-10, 10), (-10, 10), (-10, 10), (-10, 10)))
sport_target_mod = RelationshipModifier((20, 10, 10, 0), ((-10, 10), (-10, 10), (-10, 10), (-10, 10)))

make_art_init_mod = RelationshipModifier((0, 20, 20, 0), ((0, 0), (0, 0), (-20, 5), (0, 20)))
make_art_target_mod = RelationshipModifier((10, 20, 10, 0), ((0, 0), (0, 0), (-20, 5), (0, 20)))

wrestle_init_mod = RelationshipModifier((10, 0, 25, 0), ((-10, 10), (-20, 10), (-10, 10), (-10, 5)))
wrestle_target_mod = RelationshipModifier((15, 0, 25, -5), ((-10, 10), (-20, 10), (-10, 10), (-10, 5)))

debate_init_mod = RelationshipModifier((10, 10, 10, 10), ((0, 0), (-5, 10), (0, 0), (-10, 10)))
debate_target_mod = RelationshipModifier((20, 0, 10, 10), ((0, 0), (-5, 10), (0, 0), (-10, 10)))

argue_init_mod = RelationshipModifier((5, -15, 10, -10), ((-20, 5), (-10, 5), (-10, 0), (-10, 5)))
argue_target_mod = RelationshipModifier((-10, -10, 10, -10), ((-20, 5), (-10, 5), (-10, 0), (-10, 5)))

fight_init_mod = RelationshipModifier((-15, -20, 5, -15), ((-5, 15), (-10, 10), (-10, 5), (-15, -5)))
fight_target_mod = RelationshipModifier((-10, -25, 5, -25), ((-5, 15), (-10, 10), (-10, 5), (-15, -5)))

lounge_init_mod = RelationshipModifier((0, 10, -10, 0), ((0, 10), (0, 10), (-5, 5), (-10, 0)))
lounge_target_mod = RelationshipModifier((-10, 10, -10, -10), ((0, 10), (0, 10), (-5, 5), (-10, 0)))

cuddle_init_mod = RelationshipModifier((5, 20, 0, 10), ((-5, 15), (-5, 20), (-5, 5), (-10, 10)))
cuddle_target_mod = RelationshipModifier((0, 25, 0, 10), ((-5, 15), (-5, 20), (-5, 5), (-10, 10)))

mate_init_mod = RelationshipModifier((5, 25, -5, 15), ((0, 10), (0, 20), (-5, 5), (-5, 5)))
mate_target_mod = RelationshipModifier((0, 30, -5, 15), ((0, 10), (0, 20), (-5, 5), (-5, 5)))

talk_threshold = [0, 0, 0, 0]
share_food_threshold = [0, 100, 0, 0]
game_threshold = [0, 150, 0, 100]
sport_threshold = [100, 150, 0, 0]
make_art_threshold = [0, 150, 150, 0]
wrestle_threshold = [200, 100, 100, 0]
debate_threshold = [300, 0, 300, 0]
argue_threshold = [100, 0, 0, 0]
fight_threshold = [0, 0, 100, 0]
lounge_threshold = [0, 300, 0, 0]
cuddle_threshold = [200, 350, 0, 0]
mate_threshold = [300, 450, 0, 0]

talk_attribute_list = [InteractionAttributes.COMMUNICATIVE]
share_food_attribute_list = [InteractionAttributes.COOPERATIVE]
game_attribute_list = [InteractionAttributes.COOPERATIVE, InteractionAttributes.FUN, InteractionAttributes.RECREATION]
sport_attribute_list = [InteractionAttributes.FUN, InteractionAttributes.SKILL, InteractionAttributes.RECREATION]
make_art_attribute_list = [InteractionAttributes.COOPERATIVE, InteractionAttributes.FUN, InteractionAttributes.INTIMATE]
wrestle_attribute_list = [InteractionAttributes.COMBATIVE, InteractionAttributes.SKILL,
                          InteractionAttributes.RECREATION]
debate_attribute_list = [InteractionAttributes.COMMUNICATIVE, InteractionAttributes.SKILL,
                         InteractionAttributes.RECREATION]
argue_attribute_list = [InteractionAttributes.COMMUNICATIVE, InteractionAttributes.COMBATIVE]
fight_attribute_list = [InteractionAttributes.COMBATIVE, InteractionAttributes.SKILL]
lounge_attribute_list = [InteractionAttributes.COOPERATIVE, InteractionAttributes.FUN]
cuddle_attribute_list = [InteractionAttributes.COOPERATIVE, InteractionAttributes.FUN, InteractionAttributes.INTIMATE]
mate_attribute_list = [InteractionAttributes.FUN, InteractionAttributes.INTIMATE, InteractionAttributes.RECREATION]

cooperative_observer_influence = InteractionAttributeObserverInfluence((2, 0, 0, 2), (1, 0, 0, 3))
communicative_observer_influence = InteractionAttributeObserverInfluence((1, 0, 0, 3), (1, 2, 0, 0))
fun_observer_influence = InteractionAttributeObserverInfluence((0, 3, -1, 0), (0, 3, 0, 1))
intimate_observer_influence = InteractionAttributeObserverInfluence((0, 1, -2, 2), (0, 0, -1, 1))
combative_observer_influence = InteractionAttributeObserverInfluence((2, -2, 0, -2), (2, 0, 1, -2))
skill_observer_influence = InteractionAttributeObserverInfluence((2, 0, 3, 0), (2, 0, 2, 1))
recreation_observer_influence = InteractionAttributeObserverInfluence((0, 2, -3, 2), (0, 3, -2, 2))

InteractionAttributeToInfluenceDict = {InteractionAttributes.COOPERATIVE: cooperative_observer_influence,
                                       InteractionAttributes.COMMUNICATIVE: communicative_observer_influence,
                                       InteractionAttributes.FUN: fun_observer_influence,
                                       InteractionAttributes.INTIMATE: intimate_observer_influence,
                                       InteractionAttributes.COMBATIVE: combative_observer_influence,
                                       InteractionAttributes.SKILL: skill_observer_influence,
                                       InteractionAttributes.RECREATION: recreation_observer_influence}


class InteractionType:
    def __init__(self, effect_on_init, effect_on_target, relationship_threshold, interaction_attributes):
        self.effect_on_init = effect_on_init
        self.effect_on_target = effect_on_target
        self.relationship_threshold = relationship_threshold
        self.interaction_attributes = interaction_attributes


Talk = InteractionType(talk_init_mod, talk_target_mod, talk_threshold, talk_attribute_list)
Share_Food = InteractionType(share_food_init_mod, share_food_target_mod, share_food_threshold,
                             share_food_attribute_list)
Game = InteractionType(game_init_mod, game_target_mod, game_threshold, game_attribute_list)
Sport = InteractionType(sport_init_mod, sport_target_mod, sport_threshold, sport_attribute_list)
Make_Art = InteractionType(make_art_init_mod, make_art_target_mod, make_art_threshold, make_art_attribute_list)
Wrestle = InteractionType(wrestle_init_mod, wrestle_target_mod, wrestle_threshold, wrestle_attribute_list)
Debate = InteractionType(debate_init_mod, debate_target_mod, debate_threshold, debate_attribute_list)
Argue = InteractionType(argue_init_mod, argue_target_mod, argue_threshold, argue_attribute_list)
Fight = InteractionType(fight_init_mod, fight_target_mod, fight_threshold, fight_attribute_list)
Lounge = InteractionType(lounge_init_mod, lounge_target_mod, lounge_threshold, lounge_attribute_list)
Cuddle = InteractionType(cuddle_init_mod, cuddle_target_mod, cuddle_threshold, cuddle_attribute_list)
Mate = InteractionType(mate_init_mod, mate_target_mod, mate_threshold, mate_attribute_list)

ALLINTERACTIONS = [Talk, Share_Food, Game, Sport, Make_Art, Wrestle, Debate, Argue, Fight, Lounge, Cuddle, Mate]


class SocialInteraction:
    def __init__(self, interaction_type, initiator, target):
        self.interaction_type = interaction_type
        self.initiator = initiator
        self.target = target

    def resolve(self):
        self.interaction_type.effect_on_init.resolve(self.initiator.relationships[self.target])
        self.interaction_type.effect_on_target.resolve(self.target.relationships[self.initiator])


class Simfolk:
    def __init__(self, name, gender, birthday, postnominal=0):
        self.name = name
        self.relationships = {}
        self.gender = gender
        self.birthday = birthday
        self.age = 0
        self.postnomial = postnominal
        self.meal_skipped = False

        self.collection_aptitudes = {
            FoodCollectionMethod.GATHER: random.choice([x for x in range(1, 25)]),
            FoodCollectionMethod.HUNT: random.choice([x for x in range(1, 25)]),
            FoodCollectionMethod.FISH: random.choice([x for x in range(1, 25)]),
            FoodCollectionMethod.TRAP: random.choice([x for x in range(1, 25)])
        }

        self.assigned_task = None
        self.social_interaction_count = 0

    def get_collection_preferences(self):
        ordered_keys = list(FoodCollectionMethod)
        values = [self.collection_aptitudes.get(key, 0) for key in ordered_keys]
        total = sum(values)
        if total == 0:
            return [1 / len(values)] * len(values)  # fallback to equal distribution
        return [v / total for v in values]

    def consider_proposal(self, other, interaction):
        threshold = interaction.interaction_type.relationship_threshold
        relationship = self.relationships[other]
        if relationship.respect < threshold[0]:
            return False
        elif relationship.enjoyment < threshold[1]:
            return False
        elif relationship.esteem < threshold[2]:
            return False
        elif relationship.cooperativity < threshold[3]:
            return False
        return True

    def get_water_cost(self, daynum):
        if self.age < 17:
            if (self.birthday + daynum) % 2 == 0:
                return 1
            else:
                return 0
        else:
            if self.assigned_task is None:
                return 1
            else:
                return 2

    def get_food_cost(self):
        if self.age < 17:
            return 1
        else:
            if self.assigned_task is None:
                return 2
            else:
                return 3

    def _get_desired_partner_weights(self, available_simfolk):
        # If there's no one available, return empty list
        if not available_simfolk:
            return []

        weights = []
        for partner in available_simfolk:
            # Get the relationship or create a new one if it doesn't exist
            if partner not in self.relationships:
                self.relationships[partner] = Relationship()

            # Use the enjoyment value as the weight
            weights.append(self.relationships[partner].enjoyment)

        # If all weights are zero, use equal weights
        if sum(weights) == 0:
            return [1 / len(available_simfolk)] * len(available_simfolk)

        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]

    def _get_interaction_type_weights(self, partner):
        weights = []

        # Get or create relationship
        if partner not in self.relationships:
            self.relationships[partner] = Relationship()

        relationship = self.relationships[partner]

        # Maximum contribution from attributes (fixed regardless of attribute count)
        max_attribute_contribution = 30

        for interaction in ALLINTERACTIONS:
            # Start with base weight
            base_weight = 10
            total_factor = 0

            # Calculate proportional factors for each attribute
            for attribute in interaction.interaction_attributes:
                if attribute == InteractionAttributes.COMMUNICATIVE:
                    total_factor += relationship.respect / 500

                elif attribute == InteractionAttributes.FUN:
                    total_factor += relationship.enjoyment / 400

                elif attribute == InteractionAttributes.INTIMATE:
                    total_factor += (relationship.enjoyment - 200) / 300

                elif attribute == InteractionAttributes.COMBATIVE:
                    total_factor += (500 - relationship.enjoyment) / 1000

                elif attribute == InteractionAttributes.SKILL:
                    total_factor += relationship.esteem / 400

                elif attribute == InteractionAttributes.COOPERATIVE:
                    total_factor += relationship.cooperativity / 500

                elif attribute == InteractionAttributes.RECREATION:
                    total_factor += relationship.enjoyment / 600

            # Scale to fixed maximum contribution
            if interaction.interaction_attributes:
                attribute_contribution = max_attribute_contribution * (
                            total_factor / len(interaction.interaction_attributes))
            else:
                attribute_contribution = 0

            weight = base_weight + attribute_contribution

            # Add threshold penalty
            threshold = interaction.relationship_threshold
            threshold_deficit = 0

            if relationship.respect < threshold[0]:
                threshold_deficit += (threshold[0] - relationship.respect) / 50

            if relationship.enjoyment < threshold[1]:
                threshold_deficit += (threshold[1] - relationship.enjoyment) / 50

            if relationship.esteem < threshold[2]:
                threshold_deficit += (threshold[2] - relationship.esteem) / 50

            if relationship.cooperativity < threshold[3]:
                threshold_deficit += (threshold[3] - relationship.cooperativity) / 50

            weight = max(1, weight - threshold_deficit)
            weights.append(weight)

        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]

    def propose_interaction(self, available_simfolk):
        partner_choice_weights = self._get_desired_partner_weights(available_simfolk)
        target_partner = weighted_choice(available_simfolk, partner_choice_weights)
        activity_choice_weights = self._get_interaction_type_weights(target_partner)
        proposed_activity = weighted_choice(ALLINTERACTIONS, activity_choice_weights)
        return SocialInteraction(proposed_activity, self, target_partner)

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


class Village:
    def __init__(self):
        self.simfolk = []
        self.day = 0
        self.water_store = 40
        self.food_store = 40

    def add_simfolk(self, simfolk):
        for existing_sf in self.simfolk:
            simfolk.relationships[existing_sf] = Relationship()
            existing_sf.relationships[simfolk] = Relationship()
        self.simfolk.append(simfolk)

    def _generate_new_name(self, gender, parents):
        current_name_pool = [x.name for x in self.simfolk]
        potential_name_pool = {FolkGender.MALE: MALE_NAME_BANK, FolkGender.FEMALE: FEMALE_NAME_BANK}[gender]
        for _ in range(100):
            new_name = random.choice(potential_name_pool) + " " + random.choice(SURNAME_NAME_BANK)
            if new_name not in current_name_pool:
                return new_name, 0

        if parents is not None:
            for parent in parents:
                if parent.gender == gender:
                    new_name = parent.name
                    new_postnomial = (parent.postnomial + 1) % 10
                    return new_name, new_postnomial

        if gender == FolkGender.MALE:
            return "John Doe", 0
        elif gender == FolkGender.FEMALE:
            return "Jane Doe", 0
        else:
            return "Zork the Destroyer", 0

    def generate_new_simfolk(self, parents, age=0):
        child_gender = random.choice([FolkGender.MALE, FolkGender.FEMALE])
        child_name, child_postnomial = self._generate_new_name(child_gender, parents)
        child_simfolk = Simfolk(child_name, child_gender, self.day % 7)
        if age != 0:
            child_simfolk.age = age
        self.add_simfolk(child_simfolk)

    def _resolve_reproduction(self, parents):
        roll = random.choice([x for x in range(100)])
        if parents[0].gender != parents[1].gender:
            self.generate_new_simfolk(parents)

    def _resolve_social_interactions(self):
        available_simfolk = [sf for sf in self.simfolk if sf.assigned_task is None]
        interacted_pairs = set()

        if len(available_simfolk) > 1:
            proposed_interactions = []
            for sf in available_simfolk:
                proposal = sf.propose_interaction([s for s in available_simfolk if s != sf])
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

    def _assign_resource_collection_tasks(self):
        workforce = [sf for sf in self.simfolk if sf.age > 16]
        population = len(self.simfolk)

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
            worker.assigned_task = TaskAssignment(TaskType.WATER_COLLECT, None)

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
                method_preferences = worker.get_collection_preferences()
                method = weighted_choice(list(FoodCollectionMethod), method_preferences)
                worker.assigned_task = TaskAssignment(TaskType.FOOD_COLLECT, method)

    def _resolve_reource_collection(self):
        for sf in self.simfolk:
            if sf.assigned_task is not None:
                if sf.assigned_task.task_type == TaskType.WATER_COLLECT:
                    self.water_store += sf.gather_water()
                elif sf.assigned_task.task_type == TaskType.FOOD_COLLECT:
                    collection_result = sf.gather_food(sf.assigned_task.sub_info)
                    self.food_store += collection_result
                    modifier_magnitude = 1 + (sf.collection_aptitudes[sf.assigned_task.sub_info] // 18)
                    if collection_result == 0:
                        relationship_mod = (0, 0, -modifier_magnitude, 0)
                    else:
                        relationship_mod = (0, 0, modifier_magnitude, 0)
                    for bystander in [s for s in self.simfolk if s != sf]:
                        bystander.relationships[sf].update(relationship_mod)


    def _pay_upkeep_cost(self):
        for sf in self.simfolk:
            water_cost = sf.get_water_cost(self.day)
            if water_cost > self.water_store:
                thirst_flip = random.choice([True, False])
                if not thirst_flip:
                    self.simfolk.remove(sf)
            self.water_store = max(self.water_store - water_cost, 0)

            food_cost = sf.get_food_cost()
            if food_cost > self.food_store:
                if sf.meal_skipped:
                    starve_roll = weighted_choice([True, False], [.25, .75])
                    if not starve_roll:
                        self.simfolk.remove(sf)
                else:
                    sf.meal_skipped = True
            else:
                sf.meal_skipped = False
            self.food_store = max(self.food_store - food_cost, 0)

    def _resolve_aging(self):
        for sf in list(self.simfolk):
            if self.day % 7 == sf.birthday:
                sf.age += 1
            death_chance = max(0, (sf.age - 60) / 100)  # Starts at age 60, increases by 1% per year
            if random.random() < death_chance:
                self.simfolk.remove(sf)

    def _reset_assigned_tasks(self):
        for sf in self.simfolk:
            sf.assigned_task = None
            sf.social_interaction_count = 0

    def advance_day(self):
        self.day += 1
        self._assign_resource_collection_tasks()
        self._resolve_social_interactions()
        self._resolve_reource_collection()
        self._pay_upkeep_cost()
        self._resolve_aging()
        self._reset_assigned_tasks()

        if self.simfolk == [] or len(self.simfolk) >= 1000:
            return False
        return True


def main():
    community = Village()
    for _ in range(50):
        community.generate_new_simfolk(parents=None, age=20)

    running = True
    max_days = 1000
    days_elapsed = 0
    pop_max = 0

    while running and days_elapsed < max_days:
        running = community.advance_day()
        days_elapsed += 1
        if days_elapsed % 100 == 0:
            print(f"days elapsed: {days_elapsed}")
            print(f"current population: {len(community.simfolk)}")
        if len(community.simfolk) > pop_max:
            pop_max = len(community.simfolk)

    # Determine end reason
    if not running and len(community.simfolk) == 0:
        print(f"Simulation ended after {days_elapsed} days due to EXTINCTION")
    elif not running and len(community.simfolk) >= 1000:
        print(f"Simulation ended after {days_elapsed} days due to OVERPOPULATION ({len(community.simfolk)} simfolk)")
    elif days_elapsed >= max_days:
        print(f"Simulation ended after reaching TIME LIMIT of {max_days} days")
        print(f"Final population: {len(community.simfolk)} simfolk")
    print(f"Maximum population: {pop_max}")

    return days_elapsed, len(community.simfolk), community


main()
