from enum import Enum
import random


class TaskType(Enum):
    WATER_COLLECT = 0
    FOOD_COLLECT = 1


class FoodCollectionMethod(Enum):
    GATHER = 0
    HUNT = 2
    FISH = 3
    TRAP = 4


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


class InteractionType:
    def __init__(self, effect_on_init, effect_on_target):
        self.effect_on_init = effect_on_init
        self.effect_on_target = effect_on_target


Talk = InteractionType(talk_init_mod, talk_target_mod)
Share_Food = InteractionType(share_food_init_mod, share_food_target_mod)
Game = InteractionType(game_init_mod, game_target_mod)
Sport = InteractionType(sport_init_mod, sport_target_mod)
Make_Art = InteractionType(make_art_init_mod, make_art_target_mod)
Wrestle = InteractionType(wrestle_init_mod, wrestle_target_mod)
Debate = InteractionType(debate_init_mod, debate_target_mod)
Argue = InteractionType(argue_init_mod, argue_target_mod)
Fight = InteractionType(fight_init_mod, fight_target_mod)
Lounge = InteractionType(lounge_init_mod, lounge_target_mod)
Cuddle = InteractionType(cuddle_init_mod, cuddle_target_mod)
Mate = InteractionType(mate_init_mod, mate_target_mod)

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
    def __init__(self, name):
        self.name = name
        self.relationships = {}

        self.collection_aptitudes = {
            FoodCollectionMethod.GATHER: random.choice([x for x in range(1, 100)]),
            FoodCollectionMethod.HUNT: random.choice([x for x in range(1, 100)]),
            FoodCollectionMethod.FISH: random.choice([x for x in range(1, 100)]),
            FoodCollectionMethod.TRAP: random.choice([x for x in range(1, 100)])
        }

        self.assigned_task = None

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

        # Base weights for all interactions
        base_weight = 10

        for interaction in ALLINTERACTIONS:
            weight = base_weight

            # Example: adjust weights based on relationship values
            if interaction in [Talk, Debate]:
                weight += relationship.respect / 50  # More respect → more talk/debate

            if interaction in [Game, Sport, Cuddle, Mate]:
                weight += relationship.enjoyment / 50  # More enjoyment → more fun/intimate stuff

            if interaction in [Argue, Fight]:
                # Inverse relationship - less enjoyment means more fighting
                weight += (500 - relationship.enjoyment) / 100

            if interaction in [Make_Art, Wrestle]:
                weight += relationship.esteem / 50  # More esteem → more skill activities

            # Ensure no negative weights
            weight = max(1, weight)
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

    @staticmethod
    def gather_water():
        return 12

    def gather_food(self, collection_method):
        base_success_dict = {FoodCollectionMethod.GATHER: 60,
                             FoodCollectionMethod.HUNT: 20,
                             FoodCollectionMethod.FISH: 40,
                             FoodCollectionMethod.TRAP: 45
                             }
        base_amount_dict = {FoodCollectionMethod.GATHER: 3,
                            FoodCollectionMethod.HUNT: 12,
                            FoodCollectionMethod.FISH: 5,
                            FoodCollectionMethod.TRAP: 6
                            }
        base_success_rate = base_success_dict[collection_method]
        active_success_rate = (base_success_rate + self.collection_aptitudes[collection_method]) / 2
        success_roll = random.choice([x for x in range(1, 101)])
        if success_roll <= active_success_rate:
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
        self.simfolk.append(simfolk)

        for existing_sf in self.simfolk:
            simfolk.relationships[existing_sf] = Relationship()
            existing_sf.relationships[simfolk] = Relationship()

    def _resolve_social_interactions(self):
        available_simfolk = [sf for sf in self.simfolk if sf.assigned_task is None]

        if len(available_simfolk) > 1:
            proposed_interactions = []
            for sf in available_simfolk:
                proposal = sf.propose_interaction([s for s in available_simfolk if s != sf])
                if proposal:
                    proposed_interactions.append(proposal)

            for interaction in proposed_interactions:
                interaction.resolve()

    def _assign_resource_collection_tasks(self):
        raw_number_to_assign = len(self.simfolk) // 3 + (random.choice([1, 2, 3]) * random.choice([-1, 1]))
        number_to_assign = max(1, min(len(self.simfolk), raw_number_to_assign))
        simfolk_to_asign = random.sample(self.simfolk, number_to_assign)
        for target_simfolk in simfolk_to_asign:
            new_task_type = weighted_choice([TaskType.FOOD_COLLECT, TaskType.WATER_COLLECT], [.75, .25])
            if new_task_type == TaskType.FOOD_COLLECT:
                new_task_method = random.choice(
                    [FoodCollectionMethod.GATHER, FoodCollectionMethod.HUNT, FoodCollectionMethod.FISH,
                     FoodCollectionMethod.TRAP])
            else:
                new_task_method = None
            new_task = TaskAssignment(new_task_type, new_task_method)
            target_simfolk.assigned_task = new_task

    def _resolve_reource_collection(self):
        for sf in self.simfolk:
            if sf.assigned_task is not None:
                if sf.assigned_task.task_type == TaskType.WATER_COLLECT:
                    self.water_store += sf.gather_water()
                elif sf.assigned_task.task_type == TaskType.FOOD_COLLECT:
                    self.food_store += sf.gather_food(sf.assigned_task.sub_info)
                sf.assigned_task = None

    def _pay_upkeep_cost(self):
        for _ in self.simfolk:
            self.water_store -= 1
            self.food_store -= 2
            if self.water_store == 0 or self.food_store <= 0:
                return False
        return True

    def advance_day(self):
        self.day += 1
        self._assign_resource_collection_tasks()
        self._resolve_social_interactions()
        self._resolve_reource_collection()
        survival = self._pay_upkeep_cost()

        return survival


def main():
    villager_0 = Simfolk("John")
    villager_1 = Simfolk("Sara")
    villager_2 = Simfolk("Ben")
    villager_3 = Simfolk("Mary")
    community = Village()
    community.add_simfolk(villager_0)
    community.add_simfolk(villager_1)
    community.add_simfolk(villager_2)
    community.add_simfolk(villager_3)
    running = True

    while running:
        running = community.advance_day()


main()
