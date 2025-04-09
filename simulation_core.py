from village import Village
from simulation_params import SimulationParams
from sim_reports import SimulationReporter


class PrimarySimulator:
    def __init__(self):
        self.simulation_recorder = SimulationReporter()
        self.village = Village(SimulationParams, self.simulation_recorder)
        self.current_day = 0
        for _ in range(SimulationParams.STARTING_POPULATION):
            self.village.generate_new_simfolk(0, None, 20)

    def _advance_day(self):
        self.current_day += 1
        self.simulation_recorder.start_new_day(self.current_day, village.water_store, village.food_store)
        self.village.auto_assign_tasks()
        self.village.handle_social_interactions()
        self.village.collect_resources()
        self.village.handle_population_events(self.current_day)
        self.village.pay_upkeep(self.current_day)
        self.simulation_recorder.end_day()
        self.village.night_reset()

    def run_simulation(self):
        running = True
        while running:
            self._advance_day()

            if self.current_day > SimulationParams.MAX_DAYS:
                running = False

            if len(self.village.population) > SimulationParams.MAX_POPULATION:
                running = False

            if not self.village.population:
                running = False
