from core.simulation_core import PrimarySimulator
from reporting.record_formatter import SimulationFormatter
from enum import Enum


class DetailLevel(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


def interactive_simulation(detail_level=DetailLevel.MEDIUM):
    simulator = PrimarySimulator()
    running = True

    print("=== Village Simulation Started ===")
    print(f"Initial population: {len(simulator.village.population)}")

    while running:
        # Advance one day
        simulator.advance_day()

        # Get the current day report
        current_day = simulator.current_day
        day_report = simulator.simulation_recorder.full_report.simulated_days[-1]

        # Format and display the day's events
        if detail_level == DetailLevel.MEDIUM:
            formatted_day = SimulationFormatter.format_medium_detail(day_report)
        elif detail_level == DetailLevel.HIGH:
            formatted_day = SimulationFormatter.format_heavy_detail(day_report)
        else:
            formatted_day = SimulationFormatter.format_light_detail(day_report)
        print(formatted_day)

        # Check if simulation should end automatically
        if (current_day > simulator.village.params.MAX_DAYS or
                len(simulator.village.population) > simulator.village.params.MAX_POPULATION or
                not simulator.village.population):
            print("\nSimulation has reached an end condition.")
            running = False
            continue

        # Ask user if they want to continue
        choice = input("\nContinue to next day? (y/n): ").lower()
        if choice != 'y' and choice != 'yes':
            running = False

    # Display final summary
    print("\n=== Simulation Summary ===")
    print(f"Simulation ended after {simulator.current_day} days")
    print(f"Final population: {len(simulator.village.population)}")