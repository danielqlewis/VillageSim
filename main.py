from simulation_core import PrimarySimulator

if __name__ == "__main__":
    simulator = PrimarySimulator()
    simulator.run_simulation()
    print(f"Simulation ended after {simulator.current_day} days")
    print(f"Final population: {len(simulator.village.population)}")