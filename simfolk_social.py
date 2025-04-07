import utils
import social_interaction_config
from program_enums import InteractionAttributes, InteractionType


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


class SocialInteraction:
    def __init__(self, interaction_info, initiator, target):
        self.interaction_info = interaction_info
        self.initiator = initiator
        self.target = target

    def resolve(self):
        self.interaction_info.effect_on_init.resolve(self.initiator.social.relationships[self.target])
        self.interaction_info.effect_on_target.resolve(self.target.social.relationships[self.initiator])


class SimfolkSocial:
    def __init__(self):
        self.relationships = {}
        self.social_interaction_count = 0

    def create_relationship(self, other_simfolk):
        self.relationships[other_simfolk] = Relationship()

    def _standard_proposal_check(self, interaction, threshold):
        relationship = self.relationships[interaction.initiator]
        if relationship.respect < threshold[0]:
            return False
        elif relationship.enjoyment < threshold[1]:
            return False
        elif relationship.esteem < threshold[2]:
            return False
        elif relationship.cooperativity < threshold[3]:
            return False
        return True

    def consider_proposal(self, interaction, procreation_favored=False):
        if interaction.interaction_info.interaction_type == InteractionType.MATE and interaction.initiator < 17:
            return False

        threshold = interaction.interaction_info.relationship_threshold

        if interaction.interaction_info.interaction_type == InteractionType.MATE and procreation_favored:
            threshold = [50, 100, 0, 0]

        return self._standard_proposal_check(interaction, threshold)


    def get_proposal_details(self, available_simfolk, reproduction_favored, gender, age):
        partner_choice_weights = self.get_desired_partner_weights(available_simfolk)
        target_partner = utils.weighted_choice(available_simfolk, partner_choice_weights)
        if target_partner.gender != gender and target_partner.age > 16 and age > 16:
            procreation_favored = reproduction_favored
        else:
            procreation_favored = False
        activity_choice_weights = self.get_interaction_type_weights(target_partner, procreation_favored)
        proposed_activity = utils.weighted_choice(social_interaction_config.get_all_interaction_definitions(), activity_choice_weights)
        return proposed_activity, target_partner

    def get_desired_partner_weights(self, available_simfolk):
        # If there's no one available, return empty list
        if not available_simfolk:
            return []

        weights = []
        for partner in available_simfolk:
            if partner not in self.relationships:
                self.create_relationship(partner)

            # Use the enjoyment value as the weight
            weights.append(self.relationships[partner].enjoyment)

        # If all weights are zero, use equal weights
        if sum(weights) == 0:
            return [1 / len(available_simfolk)] * len(available_simfolk)

        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]

    @staticmethod
    def _get_attributes_factor(interaction):
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

        return total_factor

    @staticmethod
    def _scale_attribute_contribution(interaction, total_factor):
        max_attribute_contribution = 30
        if interaction.interaction_attributes:
            attribute_contribution = max_attribute_contribution * (
                    total_factor / len(interaction.interaction_attributes))
        else:
            attribute_contribution = 0
        return attribute_contribution

    def _get_threshold_penalty(self, partner, interaction):
        relationship = self.relationships[partner]

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

        return threshold_deficit

    def get_interaction_type_weights(self, partner, procreation_favored=False):
        weights = []
        for interaction in social_interaction_config.get_all_interaction_definitions():
            base_weight = 10
            raw_attribute_factor = self._get_attributes_factor(interaction)
            attribute_contribution = self._scale_attribute_contribution(interaction, raw_attribute_factor)
            weight = base_weight + attribute_contribution
            threshold_deficit = self._get_threshold_penalty(partner, interaction)
            weight = max(1, weight - threshold_deficit)
            if procreation_favored and interaction.interaction_type == InteractionType.MATE:
                weight *= 3
            weights.append(weight)

        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]
