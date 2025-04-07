import random
from program_enums import InteractionAttributes


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
    def __init__(self, flag, effect_on_init, effect_on_target, relationship_threshold, interaction_attributes):
        self.flag = flag
        self.effect_on_init = effect_on_init
        self.effect_on_target = effect_on_target
        self.relationship_threshold = relationship_threshold
        self.interaction_attributes = interaction_attributes


Talk = InteractionType("talk", talk_init_mod, talk_target_mod, talk_threshold, talk_attribute_list)
Share_Food = InteractionType("share food", share_food_init_mod, share_food_target_mod, share_food_threshold,
                             share_food_attribute_list)
Game = InteractionType("game", game_init_mod, game_target_mod, game_threshold, game_attribute_list)
Sport = InteractionType("sport", sport_init_mod, sport_target_mod, sport_threshold, sport_attribute_list)
Make_Art = InteractionType("make art", make_art_init_mod, make_art_target_mod, make_art_threshold, make_art_attribute_list)
Wrestle = InteractionType("wrestle", wrestle_init_mod, wrestle_target_mod, wrestle_threshold, wrestle_attribute_list)
Debate = InteractionType("debate", debate_init_mod, debate_target_mod, debate_threshold, debate_attribute_list)
Argue = InteractionType("argue", argue_init_mod, argue_target_mod, argue_threshold, argue_attribute_list)
Fight = InteractionType("fight", fight_init_mod, fight_target_mod, fight_threshold, fight_attribute_list)
Lounge = InteractionType("lounge", lounge_init_mod, lounge_target_mod, lounge_threshold, lounge_attribute_list)
Cuddle = InteractionType("cuddle", cuddle_init_mod, cuddle_target_mod, cuddle_threshold, cuddle_attribute_list)
Mate = InteractionType("mate", mate_init_mod, mate_target_mod, mate_threshold, mate_attribute_list)

ALLINTERACTIONS = [Talk, Share_Food, Game, Sport, Make_Art, Wrestle, Debate, Argue, Fight, Lounge, Cuddle, Mate]


class SocialInteraction:
    def __init__(self, interaction_type, initiator, target):
        self.interaction_type = interaction_type
        self.initiator = initiator
        self.target = target

    def resolve(self):
        self.interaction_type.effect_on_init.resolve(self.initiator.social.relationships[self.target])
        self.interaction_type.effect_on_target.resolve(self.target.social.relationships[self.initiator])


class SimfolkSocial:
    def __init__(self):
        self.relationships = {}
        self.social_interaction_count = 0

    def create_relationship(self, other_simfolk):
        self.relationships[other_simfolk] = Relationship()

    def consider_proposal(self, interaction, procreation_favored=False):

        other = interaction.initiator

        if interaction.interaction_type == Mate and other.age < 17:
            return False

        if interaction.interaction_type == Mate and procreation_favored:
            threshold = [50, 100, 0, 0]
        else:
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

    def get_proposal_details(self, available_simfolk, reproduction_favored):
        partner_choice_weights = self.get_desired_partner_weights(available_simfolk)
        target_partner = utils.weighted_choice(available_simfolk, partner_choice_weights)
        if target_partner.gender != self.gender and target_partner.age > 16 and self.age > 16:
            procreation_favored = reproduction_favored
        else:
            procreation_favored = False
        activity_choice_weights = self.get_interaction_type_weights(target_partner, procreation_favored)
        proposed_activity = utils.weighted_choice(ALLINTERACTIONS, activity_choice_weights)
        return proposed_activity, target_partner

    def get_desired_partner_weights(self, available_simfolk):
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

    def get_interaction_type_weights(self, partner, procreation_favored=False):
        weights = []

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


            if procreation_favored and interaction == Mate:
                weight *= 3

            weight = max(1, weight - threshold_deficit)
            weights.append(weight)

        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]

