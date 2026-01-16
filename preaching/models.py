"""Data models for the game."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from .enums import LocationType, Religion, Strategy, Weather
from .names import (
    generate_person_name,
    generate_store_name,
    generate_church_name,
    generate_library_name,
    generate_house_address,
    generate_neighborhood_name,
)
from .config import LOCATION_WEIGHTS, STARTING_MONEY
from .dialogue import PERSONALITIES, MOODS
from .reputation import ReputationManager


def _random_personality() -> str:
    """Pick a random personality type."""
    return random.choice(list(PERSONALITIES.keys()))


def _random_mood() -> str:
    """Pick a random starting mood (weighted towards neutral)."""
    return random.choice(["neutral", "neutral", "receptive", "grumpy", "distracted", "curious"])


@dataclass
class NPC:
    """A person who can be converted."""
    name: str = field(default_factory=generate_person_name)
    personality: str = field(default_factory=_random_personality)
    mood: str = field(default_factory=_random_mood)
    converted: bool = False
    failed_attempts: int = 0
    resistant: bool = field(default_factory=lambda: random.choice([True, False]))
    revealed_resistant: bool = False  # True if library revealed their resistance status


@dataclass
class Location:
    """A place in the neighborhood."""
    location_type: LocationType = LocationType.HOUSE
    name: str = ""
    npcs: list[NPC] = field(default_factory=list)
    affiliation: Optional[Religion] = None  # For churches
    inventory: list = field(default_factory=list)  # For stores

    @classmethod
    def create_house(cls, num_npcs: int) -> Location:
        """Create a house location."""
        return cls(
            location_type=LocationType.HOUSE,
            name=generate_house_address(),
            npcs=[NPC() for _ in range(num_npcs)],
        )

    @classmethod
    def create_store(cls) -> Location:
        """Create a store location."""
        from .items import get_random_store_inventory
        return cls(
            location_type=LocationType.STORE,
            name=generate_store_name(),
            npcs=[NPC()],  # Store clerk
            inventory=get_random_store_inventory(),
        )

    @classmethod
    def create_church(cls, affiliation: Optional[Religion] = None) -> Location:
        """Create a church location."""
        # Random affiliation if not specified (excluding Satanic usually)
        if affiliation is None:
            choices = [Religion.EVANGELIST, Religion.JEHOVAHS_WITNESS,
                       Religion.MORMON, Religion.CUSTOM, None]
            # Very rare chance of Satanic church (hidden mechanic)
            if random.random() < 0.01:
                affiliation = Religion.SATANIC
            else:
                affiliation = random.choice(choices)

        aff_str = affiliation.value if affiliation else None
        return cls(
            location_type=LocationType.CHURCH,
            name=generate_church_name(aff_str),
            npcs=[NPC() for _ in range(random.randint(3, 8))],
            affiliation=affiliation,
        )

    @classmethod
    def create_library(cls) -> Location:
        """Create a library location."""
        return cls(
            location_type=LocationType.LIBRARY,
            name=generate_library_name(),
            npcs=[NPC()],  # Librarian
        )

    @classmethod
    def create_random(cls) -> Location:
        """Create a random location based on weights."""
        roll = random.randint(1, 100)
        cumulative = 0

        for loc_type, weight in LOCATION_WEIGHTS.items():
            cumulative += weight
            if roll <= cumulative:
                if loc_type == "HOUSE":
                    return cls.create_house(random.randint(1, 6))
                elif loc_type == "STORE":
                    return cls.create_store()
                elif loc_type == "CHURCH":
                    return cls.create_church()
                elif loc_type == "LIBRARY":
                    return cls.create_library()

        # Fallback to house
        return cls.create_house(random.randint(1, 6))

    def convert(self, npc_id: int) -> None:
        """Mark an NPC as converted."""
        self.npcs[npc_id].converted = True

    def get_conversion_rate_multiplier(self) -> float:
        """Get conversion rate multiplier based on converted NPCs."""
        if not self.npcs:
            return 1.0
        num_converted = sum(npc.converted for npc in self.npcs)
        return 1 + (num_converted / len(self.npcs))

    def is_friendly_church(self, player_religion: Religion) -> bool:
        """Check if this church is friendly to the player's religion."""
        if self.location_type != LocationType.CHURCH:
            return False
        if self.affiliation is None:
            return True  # Non-denominational is friendly to all
        return self.affiliation == player_religion

    def is_hostile_church(self, player_religion: Religion) -> bool:
        """Check if this church is hostile to the player's religion."""
        if self.location_type != LocationType.CHURCH:
            return False
        if self.affiliation is None:
            return False  # Non-denominational is not hostile
        return self.affiliation != player_religion


@dataclass
class Neighborhood:
    """A collection of locations."""
    name: str = ""
    locations: list[Location] = field(default_factory=list)
    church_influence: float = 0.0  # Buff/debuff from churches

    @classmethod
    def create(cls, num_locations: int) -> Neighborhood:
        """Create a neighborhood with random locations."""
        locations = [Location.create_random() for _ in range(num_locations)]
        return cls(
            name=generate_neighborhood_name(),
            locations=locations,
        )

    def get_total_conversion_modifier(self) -> float:
        """Get total conversion modifier including church influence."""
        return self.church_influence


@dataclass
class GameState:
    """All mutable game state in one place."""
    score: int = 0
    satanic_score: int = 0
    hunger: int = 0
    money: int = STARTING_MONEY
    religion: Religion = Religion.EVANGELIST
    strategy: Strategy = Strategy.SOFT
    weather: Weather = Weather.NICE
    neighborhoods: list[Neighborhood] = field(default_factory=list)
    current_neighborhood: Optional[Neighborhood] = None
    chosen_location: Optional[Location] = None
    day_of_week: int = 0
    daily_score: int = 0
    satanic_bonus: float = 0.0
    # Item effect tracking
    pamphlet_boost_remaining: int = 0
    pamphlet_boost_amount: float = 0.0
    bible_bonus: float = 0.0
    # Reputation system
    reputation: ReputationManager = field(default_factory=ReputationManager)
    # Active pamphlet for conversations
    active_pamphlet_tags: list[str] = field(default_factory=list)

    @classmethod
    def create_new_game(cls) -> GameState:
        """Create a fresh game state with generated neighborhoods."""
        return cls(
            neighborhoods=[
                Neighborhood.create(random.randint(5, 12)) for _ in range(2)
            ]
        )

    def reset_for_new_day(self) -> None:
        """Reset daily counters."""
        self.hunger = 0
        self.daily_score = 0

    def advance_day(self) -> None:
        """Move to the next day."""
        self.day_of_week = (self.day_of_week + 1) % 7

    def is_sunday(self) -> bool:
        """Check if today is Sunday."""
        return self.day_of_week == 0

    def use_pamphlet_charge(self) -> None:
        """Use one pamphlet boost charge."""
        if self.pamphlet_boost_remaining > 0:
            self.pamphlet_boost_remaining -= 1
            if self.pamphlet_boost_remaining == 0:
                self.pamphlet_boost_amount = 0.0

    def get_total_conversion_bonus(self) -> float:
        """Get total conversion bonus from items and effects."""
        bonus = self.bible_bonus + self.satanic_bonus
        if self.pamphlet_boost_remaining > 0:
            bonus += self.pamphlet_boost_amount
        if self.current_neighborhood:
            bonus += self.current_neighborhood.get_total_conversion_modifier()
        return bonus
