import utils
from simfolk_resources import SimfolkResource
from simfolk_social import SimfolkSocial, ALLINTERACTIONS, SocialInteraction, Mate


class Simfolk:
    def __init__(self, name, gender, birthday, postnominal=0):
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.postnomial = postnominal
        self.age = 0
        self.resources = SimfolkResource()
        self.social = SimfolkSocial()

    def step_reset(self):
        self.resources.assigned_task = None
        self.social.social_interaction_count = 0

    def get_water_cost(self, daynum):
        if self.age < 17:
            if (self.birthday + daynum) % 2 == 0:
                return 1
            else:
                return 0
        else:
            if self.resources.assigned_task is None:
                return 1
            else:
                return 2

    def get_food_cost(self):
        if self.age < 17:
            return 1
        else:
            if self.resources.assigned_task is None:
                return 2
            else:
                return 3

    def propose_interaction(self, available_simfolk):
        partner_choice_weights = self.social.get_desired_partner_weights(available_simfolk)
        target_partner = utils.weighted_choice(available_simfolk, partner_choice_weights)
        activity_choice_weights = self.social.get_interaction_type_weights(target_partner)
        proposed_activity = utils.weighted_choice(ALLINTERACTIONS, activity_choice_weights)
        if proposed_activity == Mate and target_partner.age < 17:
            return None
        return SocialInteraction(proposed_activity, self, target_partner)
