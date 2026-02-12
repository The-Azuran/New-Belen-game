"""Event system for random encounters."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState
    from .ui import ConsoleUI

from .config import (
    FOOD_DONATION_CHANCE,
    SATANIC_BIBLE_CHANCE,
    FOOD_OR_BIBLE_SPLIT,
    SATANIC_ALLY_BONUS,
    DEMON_ALLY_SATANIC_BIBLE_SCALE,
    DEMON_ALLY_ENCOUNTER_SCALE,
    MAX_SATANIC_BIBLE_CHANCE,
    MAX_DEMON_ENCOUNTER_CHANCE,
)
from .enums import Religion, DemonType
from .logic import reduce_hunger
from .combat import CombatEngine


@dataclass
class Event:
    """A random event that can occur during the game."""
    name: str
    probability: float
    condition: Callable[[GameState], bool]
    handler: Callable[[GameState, ConsoleUI], None]


def always(_state: GameState) -> bool:
    """Condition that always returns True."""
    return True


def not_satanic(state: GameState) -> bool:
    """Condition: player is not a Satanic preacher."""
    return state.religion != Religion.SATANIC


def is_satanic(state: GameState) -> bool:
    """Condition: player is a Satanic preacher."""
    return state.religion == Religion.SATANIC


def has_high_satanic_score(state: GameState) -> bool:
    """Condition: player has high satanic score (>5)."""
    return state.satanic_score > 5


def in_satanic_church(state: GameState) -> bool:
    """Condition: player is in a Satanic church."""
    return (state.chosen_location and
            state.chosen_location.location_type.name == "CHURCH" and
            state.chosen_location.affiliation == Religion.SATANIC)


def handle_food_donation(state: GameState, ui: ConsoleUI) -> None:
    """Handle the food donation event."""
    ui.display_food_donation()
    if ui.prompt_yes_no("Do you want to eat the donated food now?"):
        ui.display_ate_food()
        reduce_hunger(state)


def handle_satanic_bible(state: GameState, ui: ConsoleUI) -> None:
    """Handle receiving a Satanic Bible."""
    ui.display_satanic_bible_thrown()
    if ui.prompt_yes_no("Do you want to take the Satanic Bible and become a Satanic preacher?"):
        ui.display_became_satanic()
        state.religion = Religion.SATANIC


def handle_satanic_ally(state: GameState, ui: ConsoleUI) -> None:
    """Handle meeting another Satanic preacher."""
    ui.display_met_satanic_ally()
    state.satanic_bonus += SATANIC_ALLY_BONUS


class EventManager:
    """Manages and triggers random events."""

    def __init__(self) -> None:
        self.success_events: list[Event] = []
        self.failure_events: list[Event] = []
        self._register_default_events()

    def _register_default_events(self) -> None:
        """Register the built-in events."""
        # Events that can happen on successful conversion
        self.success_events.append(Event(
            name="Food Donation",
            probability=FOOD_DONATION_CHANCE,
            condition=always,
            handler=handle_food_donation,
        ))

        # Events that can happen on failed conversion (bad response)
        # These are nested - first check if any bad response event triggers
        # Then determine which specific one

        # Demon encounter on failed conversion (15% chance when satanic_score > 5)
        self.failure_events.append(Event(
            name="Demon Encounter",
            probability=0.15,
            condition=has_high_satanic_score,
            handler=handle_demon_encounter,
        ))

        # Demon encounter in Satanic church (30% chance)
        self.failure_events.append(Event(
            name="Satanic Church Demon",
            probability=0.30,
            condition=in_satanic_church,
            handler=handle_satanic_church_demon,
        ))

    def register_success_event(self, event: Event) -> None:
        """Register a new event that can trigger on success."""
        self.success_events.append(event)

    def register_failure_event(self, event: Event) -> None:
        """Register a new event that can trigger on failure."""
        self.failure_events.append(event)

    def trigger_success_events(self, state: GameState, ui: ConsoleUI) -> None:
        """Check and trigger events after successful conversion."""
        for event in self.success_events:
            if event.condition(state) and random.random() < event.probability:
                event.handler(state, ui)

    def trigger_bad_response(self, state: GameState, ui: ConsoleUI) -> None:
        """Handle bad response events (the hidden Satanic mechanic).

        Demon allies increase the chance of satanic recruitment and
        demon encounters - keeping demons corrupts you further.
        """
        # Scale satanic bible chance with demon allies
        ally_count = len(state.demon_allies)
        scaled_bible_chance = SATANIC_BIBLE_CHANCE + (ally_count * DEMON_ALLY_SATANIC_BIBLE_SCALE)
        scaled_bible_chance = min(scaled_bible_chance, MAX_SATANIC_BIBLE_CHANCE)

        if random.random() < scaled_bible_chance:
            # Something special happens
            if random.random() < FOOD_OR_BIBLE_SPLIT:
                # Sometimes they give food anyway
                handle_food_donation(state, ui)
            elif state.religion != Religion.SATANIC:
                # Non-Satanic preachers can receive the Satanic Bible
                handle_satanic_bible(state, ui)
            else:
                # Satanic preachers meet allies
                handle_satanic_ally(state, ui)

        # Demon encounter: allies lower threshold and increase chance
        encounter_threshold = max(2, 5 - ally_count)
        encounter_chance = 0.15 + (ally_count * DEMON_ALLY_ENCOUNTER_SCALE)
        encounter_chance = min(encounter_chance, MAX_DEMON_ENCOUNTER_CHANCE)

        if state.satanic_score > encounter_threshold and random.random() < encounter_chance:
            trigger_demon_encounter(state, ui)


def handle_demon_encounter(state: GameState, ui: ConsoleUI) -> None:
    """Handle a demon encounter event."""
    from .models import NPC
    from .enums import DemonType

    ui.display_message("You sense a dark presence...")
    ui.display_message("This person seems... different. Unclean.")

    # Create a demonic NPC
    demon_npc = NPC(
        name=f"Demonic Presence",
        personality="hostile",
        mood="aggressive",
        demonic=True,
        demon_type=random.choice([DemonType.TEMPTATION, DemonType.DECEPTION, DemonType.OPPRESSION]),
        faith_resistance=random.randint(20, 60),
        demonic_power=random.randint(30, 70),
        aggression=random.randint(40, 90),  # Higher aggression for potential physical combat
        spiritual_health=random.randint(40, 80),
        physical_health=random.randint(20, 60),
    )

    # Scale difficulty with day_of_week and satanic_score
    difficulty_scale = 1.0 + (state.day_of_week * 0.1) + (state.satanic_score * 0.05)
    demon_npc.faith_resistance = int(demon_npc.faith_resistance * difficulty_scale)
    demon_npc.demonic_power = int(demon_npc.demonic_power * difficulty_scale)
    demon_npc.spiritual_health = int(demon_npc.spiritual_health * difficulty_scale)
    demon_npc.physical_health = int(demon_npc.physical_health * difficulty_scale)

    # Start combat
    combat_engine = CombatEngine()
    combat_state = combat_engine.start_combat(demon_npc, state)

    ui.display_message(f"A {demon_npc.demon_type.value} demon reveals itself!")
    ui.display_message("You must engage in spiritual warfare!")


def handle_satanic_church_demon(state: GameState, ui: ConsoleUI) -> None:
    """Handle demon encounter in Satanic church (30% chance)."""
    from .models import NPC
    from .enums import DemonType

    ui.display_message("The air in this Satanic church feels heavy with evil...")
    ui.display_message("A powerful demonic presence manifests!")

    # Create a stronger demon for Satanic church (possibly boss)
    demon_npc = NPC(
        name=f"Ancient Demon",
        personality="hostile",
        mood="aggressive",
        demonic=True,
        demon_type=random.choice([DemonType.OPPRESSION, DemonType.POSSESSION]),
        faith_resistance=random.randint(50, 80),
        demonic_power=random.randint(60, 90),
        aggression=random.randint(60, 100),
        spiritual_health=random.randint(60, 100),
        physical_health=random.randint(40, 80),
    )

    # Start combat
    combat_engine = CombatEngine()
    combat_state = combat_engine.start_combat(demon_npc, state)

    ui.display_message(f"A powerful {demon_npc.demon_type.value} demon attacks!")


def trigger_demon_encounter(state: GameState, ui: ConsoleUI) -> None:
    """Trigger a demon encounter based on context."""
    # Check if in Satanic church (30% chance)
    if (state.chosen_location and
        state.chosen_location.location_type.name == "CHURCH" and
        state.chosen_location.affiliation == Religion.SATANIC and
        random.random() < 0.30):
        handle_satanic_church_demon(state, ui)
    else:
        handle_demon_encounter(state, ui)
