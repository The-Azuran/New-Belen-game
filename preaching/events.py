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
)
from .enums import Religion
from .logic import reduce_hunger


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
        """Handle bad response events (the hidden Satanic mechanic)."""
        if random.random() < SATANIC_BIBLE_CHANCE:
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
