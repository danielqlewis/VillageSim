import random
from program_enums import InteractionType, InteractionAttributes


class RelationshipModifier:
    def __init__(self, base_mod, randomization):
        self.base_mod = base_mod
        self.randomization = randomization

    def resolve(self, relationship):
        active_modification = [m + random.choice(range(a, b + 1)) for m, (a, b) in
                               zip(self.base_mod, self.randomization)]
        relationship.update(active_modification)
        return active_modification


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


class InteractionDefinition:
    def __init__(self, interaction_type, effect_on_init, effect_on_target, relationship_threshold,
                 interaction_attributes):
        self.interaction_type = interaction_type
        self.effect_on_init = effect_on_init
        self.effect_on_target = effect_on_target
        self.relationship_threshold = relationship_threshold
        self.interaction_attributes = interaction_attributes


INTERACTION_DEFINITIONS = {
    InteractionType.TALK: InteractionDefinition(
        InteractionType.TALK,
        talk_init_mod,
        talk_target_mod,
        talk_threshold,
        talk_attribute_list
    ),
    InteractionType.SHARE_FOOD: InteractionDefinition(
        InteractionType.SHARE_FOOD,
        share_food_init_mod,
        share_food_target_mod,
        share_food_threshold,
        share_food_attribute_list
    ),
    InteractionType.GAME: InteractionDefinition(
        InteractionType.GAME,
        game_init_mod,
        game_target_mod,
        game_threshold,
        game_attribute_list
    ),
    InteractionType.SPORT: InteractionDefinition(
        InteractionType.SPORT,
        sport_init_mod,
        sport_target_mod,
        sport_threshold,
        sport_attribute_list
    ),
    InteractionType.MAKE_ART: InteractionDefinition(
        InteractionType.MAKE_ART,
        make_art_init_mod,
        make_art_target_mod,
        make_art_threshold,
        make_art_attribute_list
    ),
    InteractionType.WRESTLE: InteractionDefinition(
        InteractionType.WRESTLE,
        wrestle_init_mod,
        wrestle_target_mod,
        wrestle_threshold,
        wrestle_attribute_list
    ),
    InteractionType.DEBATE: InteractionDefinition(
        InteractionType.DEBATE,
        debate_init_mod,
        debate_target_mod,
        debate_threshold,
        debate_attribute_list
    ),
    InteractionType.ARGUE: InteractionDefinition(
        InteractionType.ARGUE,
        argue_init_mod,
        argue_target_mod,
        argue_threshold,
        argue_attribute_list
    ),
    InteractionType.FIGHT: InteractionDefinition(
        InteractionType.FIGHT,
        fight_init_mod,
        fight_target_mod,
        fight_threshold,
        fight_attribute_list
    ),
    InteractionType.LOUNGE: InteractionDefinition(
        InteractionType.LOUNGE,
        lounge_init_mod,
        lounge_target_mod,
        lounge_threshold,
        lounge_attribute_list
    ),
    InteractionType.CUDDLE: InteractionDefinition(
        InteractionType.CUDDLE,
        cuddle_init_mod,
        cuddle_target_mod,
        cuddle_threshold,
        cuddle_attribute_list
    ),
    InteractionType.MATE: InteractionDefinition(
        InteractionType.MATE,
        mate_init_mod,
        mate_target_mod,
        mate_threshold,
        mate_attribute_list
    )
}


def get_all_interaction_definitions():
    return list(INTERACTION_DEFINITIONS.values())
