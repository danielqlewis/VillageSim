# record_formatter.py


from program_enums import TaskType, FoodCollectionMethod, InteractionType, DeathCause


class SimulationFormatter:
    """Formatter for simulation reports with different levels of detail."""

    @staticmethod
    def format_light_detail(day_report):
        """Format a day report with light detail level."""
        output = [
            f"=== DAY {day_report.day_number} ===",
            f"Population: {day_report.final_population}",
            f"Food stored: {day_report.initial_resources.food_stored}",
            f"Water stored: {day_report.initial_resources.water_stored}",
        ]
        return "\n".join(output)

    @staticmethod
    def format_resource_collection_primary(collection_result):
        """Format a resource collection event with primary details only."""
        collector = collection_result.primary.collector
        task_type = collection_result.primary.task_type

        if task_type == TaskType.WATER_COLLECT:
            action = "collected water"
            resource_text = f"{collection_result.primary.amount_collected} units of water"
        else:  # FOOD_COLLECT
            method = collection_result.primary.collection_method
            method_names = {
                FoodCollectionMethod.GATHER: "gathering",
                FoodCollectionMethod.HUNT: "hunting",
                FoodCollectionMethod.FISH: "fishing",
                FoodCollectionMethod.TRAP: "trapping"
            }
            method_text = method_names.get(method, "collecting food")

            if collection_result.primary.success:
                action = f"successfully collected food by {method_text}"
                resource_text = f"{collection_result.primary.amount_collected} units of food"
            else:
                action = f"failed to collect food by {method_text}"
                resource_text = "0 units of food"

        return f"{collector} {action} ({resource_text})"

    @staticmethod
    def format_social_interaction_primary(interaction_result):
        """Format a social interaction event with primary details including attitude changes."""
        initiator = interaction_result.primary.initiator
        target = interaction_result.primary.target
        interaction_type = interaction_result.primary.interaction_type
        accepted = interaction_result.primary.acceptance

        # Map interaction types to human-readable actions
        interaction_verbs = {
            InteractionType.TALK: "talk with",
            InteractionType.SHARE_FOOD: "share food with",
            InteractionType.GAME: "play a game with",
            InteractionType.SPORT: "play sports with",
            InteractionType.MAKE_ART: "make art with",
            InteractionType.WRESTLE: "wrestle with",
            InteractionType.DEBATE: "debate with",
            InteractionType.ARGUE: "argue with",
            InteractionType.FIGHT: "fight with",
            InteractionType.LOUNGE: "lounge with",
            InteractionType.CUDDLE: "cuddle with",
            InteractionType.MATE: "mate with"
        }

        action = interaction_verbs.get(interaction_type, "interact with")

        # Format relationship changes
        attitude_names = ["respect", "enjoyment", "esteem", "cooperativity"]

        initiator_changes = interaction_result.primary.initiator_attitude_change
        target_changes = interaction_result.primary.target_attitude_change

        # Create readable format for attitude changes
        init_changes_text = []
        for i, change in enumerate(initiator_changes):
            if change != 0:
                sign = "+" if change > 0 else ""
                init_changes_text.append(f"{attitude_names[i]}: {sign}{change}")

        target_changes_text = []
        for i, change in enumerate(target_changes):
            if change != 0:
                sign = "+" if change > 0 else ""
                target_changes_text.append(f"{attitude_names[i]}: {sign}{change}")

        # Build the output
        if accepted:
            result = f"{initiator} attempted to {action} {target} and was accepted"
        else:
            result = f"{initiator} attempted to {action} {target} but was rejected"

        # Add attitude changes if there are any non-zero changes
        attitude_info = []
        if any(c != 0 for c in initiator_changes):
            init_text = ", ".join(init_changes_text)
            attitude_info.append(f"\n     {initiator}'s feelings changed ({init_text})")

        if any(c != 0 for c in target_changes):
            target_text = ", ".join(target_changes_text)
            attitude_info.append(f"\n     {target}'s feelings changed ({target_text})")

        if attitude_info:
            result += " " + " ".join(attitude_info)

        return result

    @staticmethod
    def format_birth_event(birth_record):
        """Format a birth event."""
        return f"A child named {birth_record.child_name} was born to {birth_record.parent_0} and {birth_record.parent_1}"

    @staticmethod
    def format_death_event(death_record):
        """Format a death event."""
        cause_descriptions = {
            DeathCause.AGE: "old age",
            DeathCause.THIRST: "dehydration",
            DeathCause.HUNGER: "starvation"
        }
        cause = cause_descriptions.get(death_record.cause_of_death, "unknown causes")
        return f"{death_record.dead_simfolk} died at age {death_record.final_age} from {cause}"

    @staticmethod
    def format_medium_detail(day_report):
        """Format a day report with medium detail level."""
        # Start with the light detail info
        output = [
            f"=== DAY {day_report.day_number} ===",
            f"Population: {day_report.final_population}",
            f"Food stored: {day_report.initial_resources.food_stored}",
            f"Water stored: {day_report.initial_resources.water_stored}",
            f"Food consumed today: {day_report.consumption.total_food_consumed}",
            f"Water consumed today: {day_report.consumption.total_water_consumed}",
        ]

        # If this is day 1, list out all simfolk and their food collection aptitudes
        if day_report.day_number == 1:
            # Find all unique simfolk from various events
            all_simfolk = set()

            for collection in day_report.collection_outcomes:
                all_simfolk.add(collection.primary.collector)

            for interaction in day_report.interaction_outcomes:
                all_simfolk.add(interaction.primary.initiator)
                all_simfolk.add(interaction.primary.target)

            # Add births and aging simfolk
            for birth in day_report.community_events.births:
                all_simfolk.add(birth.parent_0)
                all_simfolk.add(birth.parent_1)
                all_simfolk.add(birth.child)

            for aging in day_report.community_events.aging_simfolk:
                all_simfolk.add(aging.aging_simfolk)

            # Sort by name for consistent output
            all_simfolk = sorted(all_simfolk, key=lambda sf: str(sf))

            if all_simfolk:
                output.append("\nVillage Population:")
                for simfolk in all_simfolk:
                    # Get food collection aptitudes
                    aptitudes = simfolk.resources.collection_aptitudes
                    aptitude_strings = []

                    for method, value in aptitudes.items():
                        method_name = method.name.lower().capitalize()
                        aptitude_strings.append(f"{method_name}: {value}")

                    aptitude_text = ", ".join(aptitude_strings)
                    output.append(
                        f"- {simfolk} (Age: {simfolk.age}, Gender: {simfolk.gender.name}, Aptitudes: {aptitude_text})")

        # Add resource collection events
        if day_report.collection_outcomes:
            output.append("\nResource Collection:")
            for collection in day_report.collection_outcomes:
                output.append(f"- {SimulationFormatter.format_resource_collection_primary(collection)}")

        # Add social interaction events - failed ones first, then successful ones
        if day_report.interaction_outcomes:
            # Separate failed and successful interactions
            failed_interactions = [interaction for interaction in day_report.interaction_outcomes
                                   if not interaction.primary.acceptance]
            successful_interactions = [interaction for interaction in day_report.interaction_outcomes
                                       if interaction.primary.acceptance]

            if failed_interactions or successful_interactions:
                output.append("\nSocial Interactions:")

            if failed_interactions:
                output.append("  Failed Interactions:")
                for interaction in failed_interactions:
                    output.append(f"  - {SimulationFormatter.format_social_interaction_primary(interaction)}")

            if successful_interactions:
                output.append("  Successful Interactions:")
                for interaction in successful_interactions:
                    output.append(f"  - {SimulationFormatter.format_social_interaction_primary(interaction)}")

        # Add notable aging events (when simfolk turn 4 or 17)
        if day_report.community_events.aging_simfolk:
            notable_aging = []
            for aging in day_report.community_events.aging_simfolk:
                if aging.new_age == 4 or aging.new_age == 17:
                    notable_aging.append(aging)

            if notable_aging:
                output.append("\nNotable Aging Events:")
                for aging in notable_aging:
                    if aging.new_age == 4:
                        output.append(f"- {aging.aging_simfolk} turned 4 and is now considered a child")
                    elif aging.new_age == 17:
                        output.append(f"- {aging.aging_simfolk} turned 17 and is now considered an adult")

        # Add births
        if day_report.community_events.births:
            output.append("\nBirths:")
            for birth in day_report.community_events.births:
                output.append(f"- {SimulationFormatter.format_birth_event(birth)}")

        # Add deaths
        if day_report.community_events.deaths:
            output.append("\nDeaths:")
            for death in day_report.community_events.deaths:
                output.append(f"- {SimulationFormatter.format_death_event(death)}")

        return "\n".join(output)

    @staticmethod
    def format_heavy_detail(day_report):
        """
        Format a day report with heavy detail level - shows all information.
        This is primarily for debugging and detailed analysis.
        """
        output = []

        # Basic day information
        output.append(f"==================== DAY {day_report.day_number} ====================")
        output.append(f"Population: {day_report.final_population}")

        # Resource information
        output.append("\n--- RESOURCES ---")
        output.append(f"Initial Food: {day_report.initial_resources.food_stored}")
        output.append(f"Initial Water: {day_report.initial_resources.water_stored}")

        # Consumption details
        output.append("\n--- CONSUMPTION ---")
        output.append(f"Total Food Consumed: {day_report.consumption.total_food_consumed}")
        output.append(f"Total Water Consumed: {day_report.consumption.total_water_consumed}")

        if day_report.consumption.simfolk_gone_hungry:
            output.append("\nSimfolk Gone Hungry:")
            for sf in day_report.consumption.simfolk_gone_hungry:
                output.append(f"  - {sf} (Age: {sf.age}, Gender: {sf.gender.name})")

        if day_report.consumption.simfolk_gone_thirsty:
            output.append("\nSimfolk Gone Thirsty:")
            for sf in day_report.consumption.simfolk_gone_thirsty:
                output.append(f"  - {sf} (Age: {sf.age}, Gender: {sf.gender.name})")

        # Resource Collection
        if day_report.collection_outcomes:
            output.append("\n--- RESOURCE COLLECTION EVENTS ---")
            for i, collection in enumerate(day_report.collection_outcomes):
                output.append(f"\nCollection Event #{i + 1}:")

                # Primary details
                primary = collection.primary
                output.append(f"  Collector: {primary.collector} (Age: {primary.collector.age})")
                output.append(f"  Task Type: {primary.task_type.name}")

                if primary.collection_method:
                    output.append(f"  Collection Method: {primary.collection_method.name}")
                    aptitude = primary.collector.resources.collection_aptitudes[primary.collection_method]
                    output.append(f"  Collector's Aptitude: {aptitude}")

                output.append(f"  Success: {primary.success}")
                output.append(f"  Amount Collected: {primary.amount_collected}")

                # Secondary details
                secondary = collection.secondary
                output.append(f"  Level Up: {secondary.level_up}")

                if secondary.influence_results:
                    output.append("  Observer Influences:")
                    for influence in secondary.influence_results:
                        output.append(f"    - {influence.observer} → {influence.target}: {influence.attitude_change}")

        # Social Interactions
        if day_report.interaction_outcomes:
            output.append("\n--- SOCIAL INTERACTION EVENTS ---")

            # Group by interaction type
            interaction_by_type = {}
            for interaction in day_report.interaction_outcomes:
                interaction_type = interaction.primary.interaction_type
                if interaction_type not in interaction_by_type:
                    interaction_by_type[interaction_type] = []
                interaction_by_type[interaction_type].append(interaction)

            for interaction_type, interactions in interaction_by_type.items():
                output.append(f"\n{interaction_type.name} Interactions ({len(interactions)}):")

                # Further group by success/failure
                successful = [i for i in interactions if i.primary.acceptance]
                failed = [i for i in interactions if not i.primary.acceptance]

                output.append(f"  Successful: {len(successful)}, Failed: {len(failed)}")

                # Detail each interaction
                for i, interaction in enumerate(interactions):
                    output.append(f"\n  {interaction_type.name} #{i + 1}:")

                    # Primary details
                    primary = interaction.primary
                    output.append(f"    Initiator: {primary.initiator} (Age: {primary.initiator.age})")
                    output.append(f"    Target: {primary.target} (Age: {primary.target.age})")
                    output.append(f"    Accepted: {primary.acceptance}")
                    output.append(f"    Initiator Attitude Change: {primary.initiator_attitude_change}")
                    output.append(f"    Target Attitude Change: {primary.target_attitude_change}")

                    # Secondary details
                    secondary = interaction.secondary
                    output.append(f"    Reproduction: {secondary.reproduction}")

                    if secondary.influence_results:
                        output.append("    Observer Influences:")
                        for influence in secondary.influence_results:
                            output.append(
                                f"      - {influence.observer} → {influence.target}: {influence.attitude_change}")

        # Community Events
        output.append("\n--- COMMUNITY EVENTS ---")

        # Births
        if day_report.community_events.births:
            output.append("\nBirths:")
            for birth in day_report.community_events.births:
                output.append(f"  - Child: {birth.child_name} ({birth.child_gender.name})")
                output.append(f"    Parents: {birth.parent_0} & {birth.parent_1}")
                output.append(f"    Birthday: Day {birth.child_birthday}")

        # Aging
        if day_report.community_events.aging_simfolk:
            output.append("\nAging:")
            for aging in day_report.community_events.aging_simfolk:
                output.append(f"  - {aging.aging_simfolk} turned {aging.new_age}")

                # Highlight significant age milestones
                if aging.new_age == 4:
                    output.append("    (Now considered a child)")
                elif aging.new_age == 17:
                    output.append("    (Now considered an adult)")
                elif aging.new_age >= 60:
                    risk = round((aging.new_age - 60) / 100, 4)
                    output.append(f"    (Death risk: {risk:.2%} per day)")

        # Deaths
        if day_report.community_events.deaths:
            output.append("\nDeaths:")
            for death in day_report.community_events.deaths:
                output.append(f"  - {death.dead_simfolk} died at age {death.final_age}")
                output.append(f"    Cause: {death.cause_of_death.name}")

        return "\n".join(output)


    @staticmethod
    def format_full_simulation_light(full_report):
        """Format the entire simulation report with light detail level."""
        formatted_days = []
        for day in full_report.simulated_days:
            formatted_days.append(SimulationFormatter.format_light_detail(day))

        return "\n\n".join(formatted_days)

    @staticmethod
    def format_full_simulation_medium(full_report):
        """Format the entire simulation report with medium detail level."""
        formatted_days = []
        for day in full_report.simulated_days:
            formatted_days.append(SimulationFormatter.format_medium_detail(day))

        return "\n\n".join(formatted_days)