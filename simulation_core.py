from village import Village
from simulation_params import SimulationParams


class PrimarySimulator:
    def __init__(self):
        self.village = Village(SimulationParams)
        self.current_day = 0

    def _advance_day(self):
        # Main simulation loop
        self.current_day += 1
        self.village.auto_assign_tasks()
        self.village.handle_social_interactions()
        self.village.collect_resources()
        self.village.consume_resources()
        self.village.handle_population_events()

    def run_simulation(self):
        running = True
        while running:
            self._advance_day()

            if self.current_day > SimulationParams.MAX_DAYS:
                running = False

            if len(self.village.population) > SimulationParams.MAX_POPULATION:
                running = False
