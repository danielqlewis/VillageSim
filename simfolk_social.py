class SimfolkSocial:
    def __init__(self):
        self.relationships = {}
        self.social_interaction_count = 0

    def get_relationship(self, other_simfolk):
        # Get or create relationship
        pass

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