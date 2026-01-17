"""Console UI for the game - all input/output goes through here."""
from __future__ import annotations

import os
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState, Location, Neighborhood, NPC, InventoryItem, Town, Street
    from .enums import Religion, Strategy
    from .items import Item, Pamphlet
    from .conversation import ConversationState, ConversationResult

from .config import DAYS
from .dialogue import MOODS, PERSONALITIES


# Library lore - quirky 90s newspaper clippings
LIBRARY_LORE = [
    "LOCAL NEWS: Town council debates whether to allow rollerblading on Main Street sidewalks.",
    "CLASSIFIEDS: For sale - Beanie Babies collection. Serious investors only. $500 OBO.",
    "OPINION: 'The internet is just a fad' writes local businessman Harold Pemberton.",
    "SPORTS: Little League team wins regionals! Pizza party at Chuck E. Cheese Saturday.",
    "WEATHER: El Nino expected to bring unusual weather patterns this winter.",
    "LOCAL NEWS: New Blockbuster Video opening on Oak Street. Grand opening Saturday!",
    "COMMUNITY: Church potluck raises $127 for new hymnals. Mrs. Henderson's casserole wins 'Best Dish'.",
    "POLICE BLOTTER: Teens caught TP'ing Principal Morrison's house. Parents notified.",
    "EDITORIAL: 'Y2K is coming - are you prepared?' Tips for the new millennium inside.",
    "LIFESTYLE: Tamagotchi craze sweeps local elementary school. Teachers concerned.",
    "BUSINESS: Sears announces layoffs. 'We're confident catalog sales will recover.'",
    "REAL ESTATE: Beautiful 3BR ranch, $89,000. Great starter home!",
]


class ConsoleUI:
    """Handles all console input/output for the game."""

    def __init__(self) -> None:
        self._game_state: "GameState | None" = None

    def set_game_state(self, state: "GameState") -> None:
        """Set the game state reference for status display."""
        self._game_state = state

    def clear_screen(self) -> None:
        """Clear the console screen."""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_message(self, text: str) -> None:
        """Display a message to the player."""
        print(text)

    def display_welcome(self) -> None:
        """Display the welcome message and instructions."""
        print("=" * 50)
        print("       PREACHING THE TRUTH")
        print("=" * 50)
        print()
        print("       Dedicated to my sister, Monica Huertas")
        print("            By Rowan Valis & Claude")
        print()
        print("-" * 50)
        print()
        print("In this game, you play as a preacher for a chosen religion.")
        print("Your goal is to win as many souls as you can by going")
        print("door-to-door and preaching your faith.\n")
        print("Each day you will encounter various responses from people.")
        print("Your hunger increases as you preach. When it reaches 100,")
        print("the day ends and you must go home to rest.\n")
        print("CONTROLS:")
        print("  Press 'i' at any prompt to check your inventory/status")
        print("  Press '0' to go back/leave the current area\n")
        print("Now, let's begin by choosing your preacher...\n")

    def display_menu(self, title: str, options: list[str]) -> int:
        """Display a numbered menu and get user choice (1-indexed)."""
        if title:
            print(f"{title}\n")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        return self._get_valid_input("Enter the number of your choice: ", 1, len(options))

    def display_menu_with_zero(self, title: str, options: list[str], zero_option: str) -> int:
        """Display a numbered menu with a 0 option."""
        if title:
            print(f"{title}\n")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        print(zero_option)
        return self._get_valid_input("Enter the number of your choice: ", 0, len(options))

    def _get_valid_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """Get validated integer input from user within a range.

        If game state is set, pressing 'i' will show the status menu.
        """
        while True:
            try:
                raw = input(prompt)
                # Check for status shortcut
                if raw.lower() == 'i' and self._game_state is not None:
                    self.display_quick_status(self._game_state)
                    continue
                choice = int(raw)
                if min_val <= choice <= max_val:
                    return choice
                print(f"Invalid choice. Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                if raw.lower() == 'i':
                    print("(Status view not available yet)")
                else:
                    print("Invalid input. Please enter a number.")

    def prompt_yes_no(self, question: str) -> bool:
        """Ask a yes/no question and return True for yes."""
        response = input(f"{question} (y/n) ")
        return response.lower() == 'y'

    def prompt_continue(self) -> None:
        """Wait for the player to press Enter."""
        input("Press Enter to continue...")

    def prompt_continue_or_dashboard(self) -> bool:
        """Wait for player, return True if they want to see dashboard."""
        response = input("Press Enter to continue, or 'd' to view the dashboard.")
        return response.lower() == 'd'

    def prompt_vampire_or_werewolf(self) -> str:
        """Ask the player to choose vampire or werewolf."""
        while True:
            choice = input("You've won 10 souls to Satanism! Would you like to become a vampire or a werewolf? (v/w) ")
            if choice.lower() in ('v', 'w'):
                return choice.lower()
            print("Invalid input. Please enter 'v' for vampire or 'w' for werewolf.")

    def display_new_day(self, day_name: str, weather_value: str) -> None:
        """Announce a new day."""
        print(f"\n{'='*50}")
        print(f"A new day begins... It's {day_name}.")
        print(f"The weather is {weather_value}.")
        print(f"{'='*50}\n")

    def display_choice_confirmation(self, label: str, choice: str) -> None:
        """Confirm a player's choice."""
        print(f"You've chosen: {choice}\n")

    def display_towns(self, towns: list["Town"]) -> None:
        """Display town options with names."""
        for i, town in enumerate(towns, start=1):
            total_neighborhoods = len(town.neighborhoods)
            print(f"{i}. {town.name} ({total_neighborhoods} neighborhoods)")

    def display_neighborhoods(self, neighborhoods: list[Neighborhood]) -> None:
        """Display neighborhood options with names."""
        for i, neighborhood in enumerate(neighborhoods, start=1):
            total_streets = len(neighborhood.streets)
            print(f"{i}. {neighborhood.name} ({total_streets} streets)")

    def display_streets(self, streets: list["Street"]) -> None:
        """Display street options with names."""
        for i, street in enumerate(streets, start=1):
            total_locations = len(street.locations)
            print(f"{i}. {street.name} ({total_locations} locations)")

    def display_locations(self, locations: list[Location]) -> None:
        """Display location options with types and names."""
        from .enums import LocationType
        for i, location in enumerate(locations, start=1):
            type_icon = {
                LocationType.HOUSE: "[House]",
                LocationType.STORE: "[Store]",
                LocationType.CHURCH: "[Church]",
                LocationType.LIBRARY: "[Library]",
            }.get(location.location_type, "")
            print(f"{i}. {type_icon} {location.name}")

    def display_location_header(self, location: Location) -> None:
        """Display the current location header."""
        from .enums import LocationType, Religion
        print(f"\n--- {location.name} ---")
        # Show affiliation for churches, but hide Satanic (mysterious)
        if location.location_type == LocationType.CHURCH and location.affiliation:
            if location.affiliation != Religion.SATANIC:
                print(f"Affiliation: {location.affiliation.value}")
            else:
                print("Affiliation: Unknown")
        print()

    def display_location_npcs(self, npcs: list[NPC]) -> None:
        """Display NPCs at a location with names."""
        print(f"You see {len(npcs)} people here:\n")
        for i, npc in enumerate(npcs, start=1):
            status = "Converted" if npc.converted else "Not Converted"
            resistance_hint = ""
            if npc.revealed_resistant:
                resistance_hint = " [Resistant]" if npc.resistant else " [Receptive]"
            print(f"{i}. {npc.name}: {status}{resistance_hint}")

    def display_empty_location(self) -> None:
        """Show message for empty location."""
        print("This location appears to be empty. No one is home.\n")

    def display_already_converted(self) -> None:
        """Show message when NPC is already converted."""
        print("This person has already been converted.\n")

    def display_approaching(self, npc_name: str) -> None:
        """Show message when approaching an NPC."""
        print(f"Approaching {npc_name}...\n")

    def display_moving_on(self) -> None:
        """Show message when moving to next location."""
        print("Moving on to the next location...\n")

    def display_hunger(self, hunger: int) -> None:
        """Display current hunger level."""
        print(f"Your hunger level is now {hunger}.")

    def display_too_hungry(self) -> None:
        """Show message when day ends due to hunger."""
        print("You're too hungry to continue. Time to go home and rest.")

    def display_resistant(self, npc_name: str) -> None:
        """Show message when NPC is resistant."""
        print(f"{npc_name} is resistant to conversion.")

    def display_conversion_success(self, npc_name: str) -> None:
        """Show message on successful conversion."""
        print(f"{npc_name} is interested and converts!")

    def display_conversion_failure(self, npc_name: str) -> None:
        """Show message on failed conversion."""
        print(f"{npc_name} is not interested.")

    def display_intense_backlash(self) -> None:
        """Show message when intense preaching backfires."""
        print("Your intense approach put them off even more.")

    def display_food_donation(self) -> None:
        """Show message when receiving food."""
        print("The person donates some food to you!\n")

    def display_ate_food(self) -> None:
        """Show message after eating food."""
        print("You eat the food and feel less hungry.\n")

    def display_money_donation(self, amount: int) -> None:
        """Show message when receiving money."""
        print(f"The person donates ${amount} to your ministry!\n")

    def display_satanic_bible_thrown(self) -> None:
        """Show message when Satanic Bible is thrown."""
        print("The person throws a Satanic Bible at you!")

    def display_became_satanic(self) -> None:
        """Show message when player becomes Satanic."""
        print("You take the Satanic Bible and become a Satanic preacher!")

    def display_met_satanic_ally(self) -> None:
        """Show message when meeting another Satanic preacher."""
        print("You meet another Satanic preacher who joins your cause!")

    def display_end_game(self, score: int) -> None:
        """Display final score."""
        print(f"\n{'='*50}")
        print(f"Your ministry has ended. You've won {score} souls!")
        print(f"{'='*50}\n")

    def display_vampire_ending(self) -> None:
        """Display vampire ending."""
        print("You become a vampire and win the game!")

    def display_werewolf_ending(self) -> None:
        """Display werewolf ending."""
        print("You become a werewolf and win the game!")

    def display_sunday_offering(self, amount: int) -> None:
        """Display Sunday offering bonus."""
        print(f"\nIt's Sunday! You receive ${amount} from the Sunday offering.\n")

    # Store UI
    def display_store_welcome(self, store_name: str) -> None:
        """Display store welcome message."""
        print(f"\nWelcome to {store_name}!")
        print("What can I get for ya?\n")

    def display_store_inventory(self, items: list[Item], player_money: int) -> None:
        """Display store inventory."""
        print(f"Your money: ${player_money}\n")
        print("Available items:")
        for i, item in enumerate(items, start=1):
            affordable = "" if item.price <= player_money else " (can't afford)"
            print(f"{i}. {item.name} - ${item.price}{affordable}")
            print(f"   {item.description}")
        print("\n0. Leave store")

    def display_purchase_success(self, item_name: str) -> None:
        """Display successful purchase."""
        print(f"You bought {item_name}!")

    def display_purchase_to_inventory(self, item_name: str) -> None:
        """Display successful purchase added to inventory."""
        print(f"You bought {item_name} and put it in your bag. (Press 'i' to use)")

    def display_cannot_afford(self) -> None:
        """Display can't afford message."""
        print("You don't have enough money for that.")

    def display_store_thanks(self) -> None:
        """Display store goodbye."""
        print("Thanks, come again!\n")

    # Church UI
    def display_friendly_church(self, church_name: str) -> None:
        """Display friendly church message."""
        print(f"\nWelcome, fellow believer! The congregation of {church_name} greets you warmly.")
        print("Your presence strengthens our community's faith.\n")

    def display_hostile_church(self, church_name: str) -> None:
        """Display hostile church message."""
        print(f"\nYou are not welcome here at {church_name}!")
        print("The congregation asks you to leave immediately.")
        print("You're chased out, wasting precious energy.\n")

    def display_church_buff(self) -> None:
        """Display church buff notification."""
        print("Your spirits are lifted! Conversion rates in this area improved.\n")

    def display_church_debuff(self) -> None:
        """Display church debuff notification."""
        print("The hostile reception has shaken your confidence...\n")

    # Library UI
    def display_library_welcome(self, library_name: str) -> None:
        """Display library welcome."""
        print(f"\nWelcome to {library_name}.")
        print("The librarian looks up from her book and smiles.\n")

    def display_library_menu(self) -> int:
        """Display library options."""
        print("What would you like to do?\n")
        print("1. Research the neighborhood (learn about residents)")
        print("2. Read the local newspaper (flavor text)")
        print("3. Look up a specific person")
        print("0. Leave library")
        return self._get_valid_input("Enter your choice: ", 0, 3)

    def display_library_tip(self, tip: str) -> None:
        """Display a library research tip."""
        print(f"\nYou find some useful information:")
        print(f'"{tip}"\n')

    def display_library_lore(self) -> None:
        """Display random library lore."""
        lore = random.choice(LIBRARY_LORE)
        print(f"\nYou browse the local newspaper...")
        print(f'"{lore}"\n')

    def display_library_npc_info(self, npc_name: str, is_resistant: bool) -> None:
        """Display info about a specific NPC."""
        if is_resistant:
            print(f"\n{npc_name} is known to be set in their ways. Unlikely to convert.\n")
        else:
            print(f"\n{npc_name} seems open to new ideas. Might be receptive!\n")

    def display_library_no_people(self) -> None:
        """Display message when no people to look up."""
        print("\nYou haven't met anyone in this neighborhood yet.\n")

    def display_npc_list_for_lookup(self, npcs: list[tuple[str, NPC]]) -> int:
        """Display list of NPCs for lookup."""
        print("\nWho would you like to look up?\n")
        for i, (loc_name, npc) in enumerate(npcs, start=1):
            print(f"{i}. {npc.name} (from {loc_name})")
        print("0. Cancel")
        return self._get_valid_input("Enter your choice: ", 0, len(npcs))

    def display_quick_status(self, state: GameState) -> None:
        """Display status and inventory menu (accessible via 'i' key)."""
        while True:
            print("\n" + "=" * 35)
            print("     INVENTORY & STATUS")
            print("=" * 35)
            print(f"  Day: {DAYS[state.day_of_week]} | Hunger: {state.hunger}/100")
            print(f"  Money: ${state.money} | Souls: {state.score}")
            # Show location hierarchy
            location_parts = []
            if state.current_town:
                location_parts.append(state.current_town.name)
            if state.current_neighborhood:
                location_parts.append(state.current_neighborhood.name)
            if state.current_street:
                location_parts.append(state.current_street.name)
            if location_parts:
                print(f"  Location: {' > '.join(location_parts)}")
            if state.pamphlet_boost_remaining > 0:
                print(f"  Active pamphlet: {state.pamphlet_boost_remaining} uses left")
            if state.bible_bonus > 0:
                print(f"  Bible bonus: +{int(state.bible_bonus * 100)}%")
            if state.current_neighborhood:
                rep_desc = state.reputation.get_reputation_description(state.current_neighborhood.name)
                print(f"  Local reputation: {rep_desc}")
            print("-" * 35)

            # Show inventory
            if not state.inventory:
                print("  Your bag is empty.")
            else:
                # Group items by type
                food_items = [i for i in state.inventory if i.item_type == "food"]
                pamphlet_items = [i for i in state.inventory if i.item_type == "pamphlet"]

                if food_items:
                    print(f"  FOOD ({len(food_items)}):")
                    for idx, item in enumerate(food_items, 1):
                        print(f"    {idx}. {item.name} (-{item.hunger_restore} hunger)")

                if pamphlet_items:
                    offset = len(food_items)
                    print(f"  PAMPHLETS ({len(pamphlet_items)}):")
                    for idx, item in enumerate(pamphlet_items, offset + 1):
                        print(f"    {idx}. {item.name}")

            print("-" * 35)
            print("  Enter number to use item, or 0 to close")
            print("=" * 35)

            if not state.inventory:
                input("  Press Enter to close...")
                break

            try:
                choice = input("  > ")
                if choice == "0" or choice == "":
                    break
                choice_num = int(choice)
                if 1 <= choice_num <= len(state.inventory):
                    # Use the item
                    item = state.inventory[choice_num - 1]
                    self._use_inventory_item(state, item)
                    state.inventory.remove(item)
                else:
                    print("  Invalid choice.")
            except ValueError:
                if choice.lower() != 'i':  # Don't error on pressing i again
                    print("  Invalid input.")

    def _use_inventory_item(self, state: GameState, item: "InventoryItem") -> None:
        """Use an inventory item."""
        from .models import InventoryItem
        if item.item_type == "food":
            state.hunger = max(0, state.hunger - item.hunger_restore)
            print(f"\n  You ate the {item.name}. Hunger reduced by {item.hunger_restore}!")
            print(f"  Current hunger: {state.hunger}/100")
        elif item.item_type == "pamphlet":
            state.pamphlet_boost_remaining = 5
            state.pamphlet_boost_amount = 0.10
            state.active_pamphlet_tags = item.pamphlet_tags.copy()
            print(f"\n  You prepared the {item.name}. +10% conversion for 5 encounters!")

    def display_dashboard(self, state: GameState) -> None:
        """Display the game dashboard."""
        self.clear_screen()
        print("=" * 40)
        print("         MINISTRY DASHBOARD")
        print("=" * 40)
        print(f"Preacher: {state.preacher_name}")
        print(f"Day: {DAYS[state.day_of_week]}")
        print(f"Weather: {state.weather.value}")
        print("-" * 40)
        # Show current location in hierarchy
        if state.county:
            print(f"County: {state.county.name}")
        if state.current_town:
            print(f"Town: {state.current_town.name}")
        if state.current_neighborhood:
            print(f"Neighborhood: {state.current_neighborhood.name}")
        if state.current_street:
            print(f"Street: {state.current_street.name}")
        print("-" * 40)
        print(f"Total souls won: {state.score}")
        print(f"Souls won today: {state.daily_score}")
        if state.religion.value == "Satanic":
            print(f"Souls for Satan: {state.satanic_score}")
        print("-" * 40)
        print(f"Hunger: {state.hunger}/100")
        print(f"Money: ${state.money}")
        if state.pamphlet_boost_remaining > 0:
            print(f"Pamphlet boost: {state.pamphlet_boost_remaining} encounters left")
        if state.bible_bonus > 0:
            print(f"Bible bonus: +{int(state.bible_bonus * 100)}%")
        # Show reputation in current neighborhood
        if state.current_neighborhood:
            rep_desc = state.reputation.get_reputation_description(state.current_neighborhood.name)
            print(f"Local reputation: {rep_desc}")
        print("=" * 40)
        input("\nPress Enter to continue...")

    # =========================================================================
    # CONVERSATION UI
    # =========================================================================

    def display_conversation_start(self, npc_name: str, mood_hint: str, personality_hint: str = "") -> None:
        """Display the start of a conversation."""
        print(f"\n{'='*50}")
        print(f"Conversation with {npc_name}")
        print(f"{'='*50}")
        print(f"{mood_hint}")
        if personality_hint:
            print(f"({personality_hint})")
        print()

    def display_conversation_header(self, npc_name: str, interest: int) -> None:
        """Display a compact header for ongoing conversation turns."""
        print(f"{'='*50}")
        print(f"  Talking to: {npc_name}")
        # Visual interest indicator
        bar_pos = max(0, min(20, int((interest + 50) / 5)))
        bar = "=" * bar_pos + "-" * (20 - bar_pos)
        print(f"  Interest: [{bar}]")
        print(f"{'='*50}\n")

    def display_npc_mood_hint(self, mood: str) -> str:
        """Get visual hint for NPC mood."""
        mood_data = MOODS.get(mood, MOODS["neutral"])
        return mood_data.get("visual_hint", "They regard you calmly.")

    def display_opener_choices(self, openers: list[dict]) -> int:
        """Display opening line choices and get selection."""
        print("How do you want to start the conversation?\n")
        for i, opener in enumerate(openers, start=1):
            print(f"{i}. \"{opener['text']}\"")
        print()
        return self._get_valid_input("Choose your opener: ", 1, len(openers))

    def display_npc_response(self, response: str, is_positive: bool) -> None:
        """Display NPC's response."""
        mood_indicator = "+" if is_positive else "-"
        print(f"\nThey respond: \"{response}\" [{mood_indicator}]\n")

    def display_objection(self, objection_text: str) -> None:
        """Display NPC's objection."""
        print(f"They say: \"{objection_text}\"\n")

    def display_response_choices(self, responses: list[dict]) -> int:
        """Display response choices and get selection."""
        print("How do you respond?\n")
        for i, response in enumerate(responses, start=1):
            print(f"{i}. \"{response['text']}\"")
        print()
        return self._get_valid_input("Choose your response: ", 1, len(responses))

    def display_interest_bar(self, interest: int, description: str) -> None:
        """Display interest level as a visual bar."""
        # Scale interest to 0-20 range for display
        bar_pos = max(0, min(20, int((interest + 50) / 5)))
        bar = "[" + "=" * bar_pos + " " * (20 - bar_pos) + "]"
        print(f"Interest: {bar} ({description})")

    def display_conversion_result(self, converted: bool, rejected: bool, polite_exit: bool) -> None:
        """Display the final result of a conversation."""
        print()
        if converted:
            print("*" * 40)
            print("  SUCCESS! They want to learn more!")
            print("*" * 40)
        elif rejected:
            print("-" * 40)
            print("  They've had enough and close the door.")
            print("-" * 40)
        elif polite_exit:
            print("You part ways amicably.")
        else:
            print("The conversation ends.")
        print()

    def display_no_answer(self, npc_name: str) -> None:
        """Display when NPC won't answer the door."""
        print(f"\n{npc_name} doesn't answer the door.")
        print("Word has gotten around... Your reputation precedes you.\n")

    def display_pamphlet_selection(self, pamphlets: list[Pamphlet]) -> int:
        """Display pamphlet selection for preparing before a conversation."""
        print("\nWhich pamphlet would you like to use?\n")
        for i, pamphlet in enumerate(pamphlets, start=1):
            print(f"{i}. {pamphlet.name}")
            print(f"   {pamphlet.description}")
        print(f"{len(pamphlets) + 1}. No pamphlet")
        print()
        return self._get_valid_input("Choose pamphlet: ", 1, len(pamphlets) + 1)

    def display_reputation_change(self, neighborhood: str, old_rep: int, new_rep: int) -> None:
        """Display reputation change notification."""
        if new_rep > old_rep:
            print(f"(Your reputation in {neighborhood} has improved)")
        elif new_rep < old_rep:
            print(f"(Your reputation in {neighborhood} has declined)")

    # =========================================================================
    # NARRATIVE UI
    # =========================================================================

    def display_internal_thought(self, thought: str) -> None:
        """Display Belen's internal monologue."""
        if thought:
            print(f"\n  * {thought} *\n")

    def display_narrative_moment(self, text: str) -> None:
        """Display a narrative/atmospheric moment."""
        if text:
            print(f"\n{text}\n")

    def display_weather_narrative(self, narrative: str) -> None:
        """Display weather-related narrative at day start."""
        print(f"{narrative}")

    def display_neighborhood_return(self, narrative: str) -> None:
        """Display narrative when returning to a neighborhood."""
        if narrative:
            print(f"\n{narrative}\n")

    def display_encounter_callback(self, callback: str) -> None:
        """Display a callback to a previous encounter."""
        if callback:
            print(f"  * {callback} *")

    def display_journal_entry(self, entry: str) -> None:
        """Display an end-of-day journal entry."""
        print("\n" + "=" * 50)
        print("             BELEN'S JOURNAL")
        print("=" * 50)
        print()
        for line in entry.split("\n"):
            print(f"  {line}")
        print()
        print("=" * 50)
        input("\nPress Enter to continue...")

    def display_ending_reflection(self, reflection: str) -> None:
        """Display the final ending reflection."""
        print("\n" + "=" * 50)
        print("           FINAL REFLECTIONS")
        print("=" * 50)
        print()
        for line in reflection.split("\n"):
            print(f"  {line}")
        print()
        print("=" * 50)
