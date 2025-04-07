import utils
from simfolk_resources import SimfolkResource
from simfolk_social import SimfolkSocial, SocialInteraction
from program_enums import InteractionType


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

    def propose_interaction(self, available_simfolk, reproduction_favored):
        proposed_activity, target_partner = self.social.get_proposal_details(available_simfolk, reproduction_favored, self.gender, self.age)

        if proposed_activity.interaction_type == InteractionType.MATE and target_partner.age < 17:
            return None

        return SocialInteraction(proposed_activity, self, target_partner)
