from simfolk_resources import SimfolkResource
from simfolk_social import SimfolkSocial


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