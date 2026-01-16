"""Main game orchestrator."""
from __future__ import annotations

from .config import (
    AVAILABLE_RELIGIONS,
    GAME_DAYS,
    SATANIC_VICTORY_THRESHOLD,
    DAYS,
)
from .enums import LocationType, Religion
from .events import EventManager
from .logic import (
    apply_hunger,
    is_day_over,
    record_conversion,
    set_random_weather,
    try_money_donation,
    apply_sunday_offering,
    purchase_item,
    can_afford,
    apply_friendly_church_buff,
    apply_hostile_church_debuff,
    is_church_friendly,
    is_church_hostile,
    apply_library_hunger,
    get_neighborhood_tip,
    reveal_npc_resistance,
    get_all_npcs_in_neighborhood,
)
from .models import GameState, NPC
from .ui import ConsoleUI
from .conversation import ConversationEngine, ConversationState
from .memory import MemoryManager
from .narrative import NarrativeEngine, NarrativeContext


class Game:
    """Main game orchestrator - ties together UI, state, and logic."""

    def __init__(self, ui: ConsoleUI) -> None:
        self.ui = ui
        self.state = GameState.create_new_game()
        self.events = EventManager()
        self.conversation = ConversationEngine()
        self.memory = MemoryManager()
        self.narrative = NarrativeEngine(self.memory)

    def run(self) -> None:
        """Run the main game loop."""
        self.ui.display_welcome()
        self._choose_religion()

        for _ in range(GAME_DAYS):
            self._run_day()
            self.state.reset_for_new_day()
            self.state.advance_day()

        self._end_game()

    def _get_narrative_context(self) -> NarrativeContext:
        """Build current narrative context from game state."""
        from .memory import EventType
        neighborhood_name = ""
        reputation = 0
        if self.state.current_neighborhood:
            neighborhood_name = self.state.current_neighborhood.name
            reputation = self.state.reputation.get_reputation(neighborhood_name)

        return NarrativeContext(
            day=self.state.day_of_week,
            weather=self.state.weather.value,
            hunger=self.state.hunger,
            money=self.state.money,
            total_score=self.state.score,
            satanic_score=self.state.satanic_score,
            current_neighborhood=neighborhood_name,
            rejection_streak=self.memory.get_streak(EventType.REJECTION),
            conversion_streak=self.memory.get_streak(EventType.CONVERSION),
            reputation_in_area=reputation,
        )

    def _choose_religion(self) -> None:
        """Let the player choose their religion."""
        options = [r.value for r in AVAILABLE_RELIGIONS]
        choice = self.ui.display_menu("Choose your religion:", options)
        self.state.religion = AVAILABLE_RELIGIONS[choice - 1]
        self.ui.display_choice_confirmation("religion", self.state.religion.value)

    def _run_day(self) -> None:
        """Run a single day of gameplay."""
        set_random_weather(self.state)
        day_name = DAYS[self.state.day_of_week]

        # Start tracking day in memory
        self.memory.start_day(
            self.state.day_of_week,
            day_name,
            self.state.weather.value
        )

        self.ui.display_new_day(day_name, self.state.weather.value)

        # Weather narrative
        weather_narrative = self.narrative.get_weather_narrative(
            self.state.weather.value,
            self.state.day_of_week
        )
        self.ui.display_weather_narrative(weather_narrative)

        # Money situation narrative
        context = self._get_narrative_context()
        money_narrative = self.narrative.get_money_narrative(self.state.money, context)
        if money_narrative:
            self.ui.display_narrative_moment(money_narrative)

        # Sunday offering
        if self.state.is_sunday():
            amount = apply_sunday_offering(self.state)
            self.ui.display_sunday_offering(amount)

        self._choose_neighborhood_and_location()
        self._main_loop()

        # End day and show journal
        ended_hungry = self.state.hunger >= 100
        summary = self.memory.end_day(ended_hungry)
        journal_entry = self.narrative.generate_journal_entry(summary)
        self.ui.display_journal_entry(journal_entry)

    def _choose_neighborhood_and_location(self) -> None:
        """Let the player choose a neighborhood and location."""
        # Choose neighborhood
        print("Choose your neighborhood:\n")
        self.ui.display_neighborhoods(self.state.neighborhoods)
        choice = self.ui._get_valid_input(
            "Enter the number of your choice: ", 1, len(self.state.neighborhoods)
        )
        self.state.current_neighborhood = self.state.neighborhoods[choice - 1]
        self.ui.display_choice_confirmation(
            "neighborhood", self.state.current_neighborhood.name
        )

        # Check for return narrative (have we been here before?)
        neighborhood_name = self.state.current_neighborhood.name
        reputation = self.state.reputation.get_reputation(neighborhood_name)
        return_narrative = self.narrative.get_neighborhood_return_narrative(
            neighborhood_name, reputation
        )
        self.ui.display_neighborhood_return(return_narrative)

        # Choose location
        self._choose_location()

    def _choose_location(self) -> None:
        """Choose a location within the current neighborhood."""
        assert self.state.current_neighborhood is not None
        print("Choose your location:\n")
        self.ui.display_locations(self.state.current_neighborhood.locations)
        choice = self.ui._get_valid_input(
            "Enter the number of your choice: ",
            1,
            len(self.state.current_neighborhood.locations),
        )
        self.state.chosen_location = self.state.current_neighborhood.locations[choice - 1]
        self.ui.display_choice_confirmation(
            "location", self.state.chosen_location.name
        )

    def _main_loop(self) -> None:
        """Main gameplay loop for the day."""
        while not is_day_over(self.state):
            assert self.state.chosen_location is not None
            self.ui.clear_screen()

            location = self.state.chosen_location
            self.ui.display_location_header(location)

            # Handle different location types
            if location.location_type == LocationType.STORE:
                self._handle_store()
            elif location.location_type == LocationType.CHURCH:
                self._handle_church()
            elif location.location_type == LocationType.LIBRARY:
                self._handle_library()
            else:
                self._handle_house()

            if is_day_over(self.state):
                self.ui.display_too_hungry()

    def _handle_house(self) -> None:
        """Handle a house location (standard preaching)."""
        assert self.state.chosen_location is not None
        assert self.state.current_neighborhood is not None
        location = self.state.chosen_location
        neighborhood_name = self.state.current_neighborhood.name

        # Handle empty locations
        if not location.npcs:
            self.ui.display_empty_location()
            self.ui.prompt_continue()
            self._prompt_next_action()
            return

        self.ui.display_location_npcs(location.npcs)
        print("\nChoose a person to approach or enter 0 to move on.")

        choice = self.ui._get_valid_input("Enter your choice: ", 0, len(location.npcs))

        if choice == 0:
            self.ui.display_moving_on()
            self._prompt_next_action()
            return

        npc_id = choice - 1
        npc = location.npcs[npc_id]

        if npc.converted:
            self.ui.display_already_converted()
            return

        # Get narrative context and show internal thought before approaching
        context = self._get_narrative_context()
        approach_thought = self.narrative.get_approach_thought(context, npc)
        self.ui.display_internal_thought(approach_thought)

        # Check for callbacks to previous encounters
        callback = self.narrative.get_encounter_callback(npc, neighborhood_name)
        self.ui.display_encounter_callback(callback)

        # Check if NPC will even open the door (reputation system)
        if not self.state.reputation.will_open_door(neighborhood_name):
            self.ui.display_no_answer(npc.name)
            # Record no-answer in memory
            self.memory.record_no_answer(self.state.day_of_week, neighborhood_name)
            # Show thought about being unwelcome
            no_answer_thought = self.narrative.get_no_answer_thought(context)
            self.ui.display_internal_thought(no_answer_thought)
            apply_hunger(self.state)
            self.ui.display_hunger(self.state.hunger)
            return

        # Run the new conversation system
        self._run_conversation(npc, npc_id)

        apply_hunger(self.state)
        self.state.use_pamphlet_charge()  # Use pamphlet charge if active
        self.ui.display_hunger(self.state.hunger)

        if not is_day_over(self.state):
            if self.ui.prompt_continue_or_dashboard():
                self.ui.display_dashboard(self.state)

    def _handle_store(self) -> None:
        """Handle a store location."""
        assert self.state.chosen_location is not None
        location = self.state.chosen_location

        self.ui.display_store_welcome(location.name)

        while True:
            self.ui.display_store_inventory(location.inventory, self.state.money)
            choice = self.ui._get_valid_input("Enter your choice: ", 0, len(location.inventory))

            if choice == 0:
                self.ui.display_store_thanks()
                self._prompt_next_action()
                return

            item = location.inventory[choice - 1]
            if can_afford(self.state, item.price):
                purchase_item(self.state, item.price)
                item.effect(self.state)
                self.ui.display_purchase_success(item.name)
            else:
                self.ui.display_cannot_afford()

    def _handle_church(self) -> None:
        """Handle a church location."""
        assert self.state.chosen_location is not None
        assert self.state.current_neighborhood is not None
        location = self.state.chosen_location
        neighborhood_name = self.state.current_neighborhood.name

        if is_church_friendly(location, self.state.religion):
            self.ui.display_friendly_church(location.name)
            apply_friendly_church_buff(self.state)
            self.ui.display_church_buff()
            # Record friendly church in memory
            self.memory.record_friendly_church(
                self.state.day_of_week, neighborhood_name, location.name
            )

            # Can preach in friendly church
            if location.npcs:
                if self.ui.prompt_yes_no("Would you like to preach to the congregation?"):
                    self._handle_house()  # Reuse house logic for preaching
                    return

        elif is_church_hostile(location, self.state.religion):
            self.ui.display_hostile_church(location.name)
            apply_hostile_church_debuff(self.state)
            self.ui.display_church_debuff()
            self.ui.display_hunger(self.state.hunger)
            # Reputation hit for getting chased out
            self.state.reputation.on_hostile_church(neighborhood_name)
            # Record hostile church in memory
            self.memory.record_hostile_church(
                self.state.day_of_week, neighborhood_name, location.name
            )
        else:
            # Non-denominational - neutral
            self.ui.display_message(f"\n{location.name} welcomes all faiths.")
            if location.npcs and self.ui.prompt_yes_no("Would you like to preach here?"):
                self._handle_house()
                return

        self.ui.prompt_continue()
        self._prompt_next_action()

    def _handle_library(self) -> None:
        """Handle a library location."""
        assert self.state.chosen_location is not None
        assert self.state.current_neighborhood is not None
        location = self.state.chosen_location

        self.ui.display_library_welcome(location.name)

        while True:
            choice = self.ui.display_library_menu()

            if choice == 0:
                self._prompt_next_action()
                return

            elif choice == 1:
                # Research neighborhood
                apply_library_hunger(self.state)
                tip = get_neighborhood_tip(self.state.current_neighborhood)
                self.ui.display_library_tip(tip)
                self.ui.display_hunger(self.state.hunger)

            elif choice == 2:
                # Read newspaper (lore)
                self.ui.display_library_lore()

            elif choice == 3:
                # Look up specific person
                npcs = get_all_npcs_in_neighborhood(self.state.current_neighborhood)
                if not npcs:
                    self.ui.display_library_no_people()
                else:
                    npc_choice = self.ui.display_npc_list_for_lookup(npcs)
                    if npc_choice > 0:
                        apply_library_hunger(self.state)
                        _, npc = npcs[npc_choice - 1]
                        reveal_npc_resistance(npc)
                        self.ui.display_library_npc_info(npc.name, npc.resistant)
                        self.ui.display_hunger(self.state.hunger)
                        # Record in memory if they're resistant
                        if npc.resistant:
                            self.memory.record_resistant_revealed(
                                self.state.day_of_week,
                                self.state.current_neighborhood.name,
                                npc.name
                            )

            if is_day_over(self.state):
                return

    def _prompt_next_action(self) -> None:
        """Prompt player for next action after leaving a location."""
        if is_day_over(self.state):
            return

        print("\nWhat would you like to do?")
        print("1. Choose a new location in this neighborhood")
        print("2. Go to a different neighborhood")
        choice = self.ui._get_valid_input("Enter your choice: ", 1, 2)

        if choice == 1:
            self._choose_location()
        else:
            self._choose_neighborhood_and_location()

    def _run_conversation(self, npc: NPC, npc_id: int) -> None:
        """Run the full conversation system with an NPC."""
        assert self.state.current_neighborhood is not None
        neighborhood_name = self.state.current_neighborhood.name

        # Get reputation bonus
        rep_bonus = self.state.reputation.get_reputation_bonus(neighborhood_name)

        # Override mood based on reputation
        original_mood = npc.mood
        npc.mood = self.state.reputation.get_starting_mood(neighborhood_name)

        # Start conversation
        conv_state = ConversationState.start(
            npc,
            reputation_bonus=rep_bonus,
            pamphlet_tags=self.state.active_pamphlet_tags,
        )

        # Display conversation start
        mood_hint = self.ui.display_npc_mood_hint(conv_state.mood)
        self.ui.display_conversation_start(npc.name, mood_hint)

        # Show opening response
        opening_response = self.conversation.get_opening_response(conv_state)
        self.ui.display_npc_response(opening_response, conv_state.interest >= 0)

        # Player chooses opener
        openers = self.conversation.get_openers()
        opener_choice = self.ui.display_opener_choices(openers)
        opener = openers[opener_choice - 1]

        # Track tags used during conversation for memory
        used_tags: list[str] = list(opener.get("tags", []))
        was_aggressive = "hellfire" in used_tags or "pushy" in used_tags

        # Apply opener and get result
        result = self.conversation.apply_opener(conv_state, opener["id"])
        interest_desc = self.conversation.get_interest_description(conv_state.interest)
        self.ui.display_interest_bar(conv_state.interest, interest_desc)

        # Main conversation loop
        current_objection = None
        while not result.conversation_ended:
            # Get next objection from NPC
            current_objection = self.conversation.get_next_objection(conv_state)
            self.ui.display_objection(current_objection["text"])

            # Get available responses
            responses = self.conversation.get_available_responses(conv_state, current_objection["id"])
            response_choice = self.ui.display_response_choices(responses)
            response = responses[response_choice - 1]

            # Track response tags
            response_tags = response.get("tags", [])
            used_tags.extend(response_tags)
            if "hellfire" in response_tags or "pushy" in response_tags:
                was_aggressive = True

            # Apply response
            result = self.conversation.apply_response(conv_state, response["id"], current_objection["id"])

            # Show NPC response
            self.ui.display_npc_response(result.npc_response, result.is_positive)
            interest_desc = self.conversation.get_interest_description(result.new_interest)
            self.ui.display_interest_bar(result.new_interest, interest_desc)

        # Handle conversation end
        self.ui.display_conversion_result(result.converted, result.rejected, result.polite_exit)

        # Update reputation based on outcome
        old_rep = self.state.reputation.get_reputation(neighborhood_name)
        if result.converted:
            self._handle_conversion_success(npc_id, neighborhood_name, npc, used_tags)
        elif result.rejected:
            self._handle_rejection(neighborhood_name, npc, was_aggressive)
        elif result.polite_exit:
            self.state.reputation.on_polite_exit(neighborhood_name)
            self.memory.record_polite_exit(self.state.day_of_week, neighborhood_name, npc.name)
        else:
            # Ran out of patience - treat as rejection
            self.state.reputation.on_rejection(neighborhood_name)
            self.memory.record_rejection(
                self.state.day_of_week, neighborhood_name, npc.name, npc.personality
            )

        new_rep = self.state.reputation.get_reputation(neighborhood_name)
        self.ui.display_reputation_change(neighborhood_name, old_rep, new_rep)

        # Restore original mood for NPC
        npc.mood = original_mood

    def _handle_conversion_success(self, npc_id: int, neighborhood_name: str, npc: NPC,
                                    approach_tags: list[str]) -> None:
        """Handle successful conversion."""
        record_conversion(self.state, npc_id)
        self.state.reputation.on_conversion(neighborhood_name)

        # Record in memory
        self.memory.record_conversion(
            day=self.state.day_of_week,
            neighborhood=neighborhood_name,
            npc_name=npc.name,
            npc_personality=npc.personality,
            approach_tags=approach_tags,
        )

        # Show post-conversion thought
        context = self._get_narrative_context()
        thought = self.narrative.get_post_conversion_thought(context, npc)
        self.ui.display_internal_thought(thought)

        # Check for money donation
        donation = try_money_donation(self.state)
        if donation:
            self.ui.display_money_donation(donation)
            self.memory.record_donation(self.state.day_of_week, donation)

        self.events.trigger_success_events(self.state, self.ui)

    def _handle_rejection(self, neighborhood_name: str, npc: NPC,
                          was_aggressive: bool = False) -> None:
        """Handle when NPC rejects player."""
        self.state.reputation.on_rejection(neighborhood_name)

        # Record in memory
        self.memory.record_rejection(
            day=self.state.day_of_week,
            neighborhood=neighborhood_name,
            npc_name=npc.name,
            npc_personality=npc.personality,
            was_aggressive=was_aggressive,
        )

        # Show post-rejection thought
        context = self._get_narrative_context()
        thought = self.narrative.get_post_rejection_thought(context, npc, was_aggressive)
        self.ui.display_internal_thought(thought)

        self.events.trigger_bad_response(self.state, self.ui)

    def _end_game(self) -> None:
        """Handle end of game."""
        self.ui.display_end_game(self.state.score)

        # Generate and display final reflection
        patterns = self.memory.get_recurring_patterns()
        reflection = self.narrative.generate_ending_reflection(self.state, patterns)
        self.ui.display_ending_reflection(reflection)

        if self.state.satanic_score >= SATANIC_VICTORY_THRESHOLD:
            self._become_supernatural()

    def _become_supernatural(self) -> None:
        """Handle the supernatural ending."""
        choice = self.ui.prompt_vampire_or_werewolf()
        if choice == 'v':
            self.ui.display_vampire_ending()
        else:
            self.ui.display_werewolf_ending()
