from dataclasses import dataclass
from typing import Optional, List, Tuple
from entities.simfolk_base import Simfolk
from common.program_enums import InteractionType, TaskType, FoodCollectionMethod, FolkGender, DeathCause


class SimulationReporter:
    def __init__(self):
        self.current_day_report = None
        self.current_event = None
        self.full_report = FullSimulationReport(simulated_days=[])
        self.current_day = -1

    def start_new_day(self, day_number, initial_water, initial_food):
        self.current_day = day_number
        initial_resources = ResourceStoreReport(water_stored=initial_water, food_stored=initial_food)

        self.current_day_report = SimulationDayReport(
            day_number=day_number,
            initial_resources=initial_resources,
            collection_outcomes=[],
            interaction_outcomes=[],
            relationships_status=[],
            consumption=ConsumptionReport(
                total_food_consumed=0,
                total_water_consumed=0,
                simfolk_gone_thirsty=[],
                simfolk_gone_hungry=[]
            ),
            community_events=LifeEventsReport(
                day_number=day_number,
                births=[],
                aging_simfolk=[],
                deaths=[]
            ),
            final_population=0
        )

    def establish_social_interaction(self, interaction, accepted):
        interaction_primary_record = SocialInteractionResultPrimary(
            initiator=interaction.initiator,
            target=interaction.target,
            interaction_type=interaction.interaction_info.interaction_type,
            acceptance=accepted,
            initiator_attitude_change=(0, 0, 0, 0),
            target_attitude_change=(0, 0, 0, 0)

        )
        interaction_secondary_record = SocialInteractionResultSecondary(
            reproduction=False,
            influence_results=[]
        )
        self.current_event = SocialInteractionResultFull(
            day_number=self.current_day,
            primary=interaction_primary_record,
            secondary=interaction_secondary_record
        )

    def update_participants_attitude_change(self, changes):
        self.current_event.primary.initiator_attitude_change = changes[0]
        self.current_event.primary.target_attitude_change = changes[1]

    def update_reproduction_flag(self, new_value):
        self.current_event.secondary.reproduction = new_value

    def add_observer_influence(self, observer, target, change):
        new_observer_event = EventInfluence(observer, target, change)
        self.current_event.secondary.influence_results.append(new_observer_event)

    def register_social_interaction(self):
        self.current_day_report.interaction_outcomes.append(self.current_event)
        self.current_event = None

    def record_resource_collection(self, collector, task_type, method, success, amount, level_up, influences):
        collection_primary_record = ResourceCollectionResultPrimary(
            collector=collector,
            task_type=task_type,
            collection_method=method,
            success=success,
            amount_collected=amount
        )
        processed_influences = [EventInfluence(observer=influence[0], target=collector, attitude_change=influence[1])
                                for influence in influences]
        collection_secondary_record = ResourceCollectionResultSecondary(
            level_up=level_up,
            influence_results=processed_influences
        )
        full_record = ResourceCollectionResultFull(
            day_number=self.current_day,
            primary=collection_primary_record,
            secondary=collection_secondary_record
        )
        self.current_day_report.collection_outcomes.append(full_record)

    def record_opinion(self, simfolk, target):
        opinion = simfolk.social.relationships[target]
        opinion_record = OpinionReport(simfolk, target, opinion)
        self.current_day_report.relationships_status.append(opinion_record)



    def record_all_relationships(self, population):
        for simfolk in population:
            for sf in population:
                self.record_opinion(simfolk, sf)

    def record_birth(self, parent_0, parent_1, child):
        new_record = BirthRecord(
            parent_0=parent_0,
            parent_1=parent_1,
            child=child,
            child_gender=child.gender,
            child_birthday=child.birthday,
            child_name=child.name
        )
        if self.current_day_report:
            self.current_day_report.community_events.births.append(new_record)

    def record_death(self, simfolk, age, cause):
        new_record = DeathRecord(
            dead_simfolk=simfolk,
            final_age=age,
            cause_of_death=cause
        )
        self.current_day_report.community_events.deaths.append(new_record)

    def record_aging(self, simfolk, new_age):
        new_record = FolkAgingRecord(
            aging_simfolk=simfolk,
            new_age=new_age
        )
        self.current_day_report.community_events.aging_simfolk.append(new_record)

    def update_water_consumption(self, amount, thirsty_simfolk):
        self.current_day_report.consumption.total_water_consumed += amount
        if thirsty_simfolk:
            self.current_day_report.consumption.simfolk_gone_thirsty.append(thirsty_simfolk)

    def update_food_consumption(self, amount, hungry_simfolk):
        self.current_day_report.consumption.total_food_consumed += amount
        if hungry_simfolk:
            self.current_day_report.consumption.simfolk_gone_hungry.append(hungry_simfolk)

    def end_day(self, pop_size):
        if self.current_day_report:
            self.current_day_report.final_population = pop_size
            self.full_report.simulated_days.append(self.current_day_report)
            self.current_day_report = None


@dataclass
class BirthRecord:
    parent_0: Optional[Simfolk]
    parent_1: Optional[Simfolk]
    child: Simfolk
    child_gender: FolkGender
    child_birthday: int
    child_name: str


@dataclass
class FolkAgingRecord:
    aging_simfolk: Simfolk
    new_age: int


@dataclass
class DeathRecord:
    dead_simfolk: Simfolk
    final_age: int
    cause_of_death: DeathCause


@dataclass
class LifeEventsReport:
    day_number: int
    births: List[BirthRecord]
    aging_simfolk: List[FolkAgingRecord]
    deaths: List[DeathRecord]


@dataclass
class EventInfluence:
    observer: Simfolk
    target: Simfolk
    attitude_change: Tuple[int, int, int, int]


@dataclass
class SocialInteractionResultSecondary:
    influence_results: List[EventInfluence]
    reproduction: bool


@dataclass
class SocialInteractionResultPrimary:
    initiator: Simfolk
    target: Simfolk
    interaction_type: InteractionType
    acceptance: bool
    initiator_attitude_change: Tuple[int, int, int, int]
    target_attitude_change: Tuple[int, int, int, int]


@dataclass
class SocialInteractionResultFull:
    day_number: int
    primary: SocialInteractionResultPrimary
    secondary: SocialInteractionResultSecondary


@dataclass
class ResourceCollectionResultSecondary:
    level_up: bool
    influence_results: List[EventInfluence]


@dataclass
class ResourceCollectionResultPrimary:
    collector: Simfolk
    task_type: TaskType
    collection_method: Optional[FoodCollectionMethod]
    success: bool
    amount_collected: int


@dataclass
class ResourceCollectionResultFull:
    day_number: int
    primary: ResourceCollectionResultPrimary
    secondary: ResourceCollectionResultSecondary


@dataclass
class ResourceStoreReport:
    water_stored: int
    food_stored: int


@dataclass
class ConsumptionReport:
    total_food_consumed: int
    total_water_consumed: int
    simfolk_gone_thirsty: List[Simfolk]
    simfolk_gone_hungry: List[Simfolk]

@dataclass
class OpinionReport:
    opinion_holder: Simfolk
    opinion_subject: Simfolk
    opinion_vector: Tuple[int, int, int, int]

@dataclass
class SimulationDayReport:
    day_number: int
    initial_resources: ResourceStoreReport
    collection_outcomes: List[ResourceCollectionResultFull]
    interaction_outcomes: List[SocialInteractionResultFull]
    relationships_status: List[OpinionReport]
    community_events: LifeEventsReport
    consumption: ConsumptionReport
    final_population: int


@dataclass
class FullSimulationReport:
    simulated_days: List[SimulationDayReport]
