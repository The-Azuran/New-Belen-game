"""Pure game logic functions - no I/O here."""
from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState, NPC, Location, Neighborhood

from .config import (
    CONVERSION_RATES,
    FAILED_ATTEMPT_PENALTY,
    MAX_CONVERSION_RATE,
    HUNGER_HARSH_WEATHER,
    HUNGER_NICE_WEATHER,
    FOOD_HUNGER_REDUCTION,
    MAX_HUNGER,
    MONEY_DONATION_CHANCE,
    MONEY_DONATION_MIN,
    MONEY_DONATION_MAX,
    SUNDAY_OFFERING_BONUS,
    FRIENDLY_CHURCH_BUFF,
    HOSTILE_CHURCH_DEBUFF,
    CHURCH_CHASE_HUNGER_COST,
    LIBRARY_RESEARCH_HUNGER,
)
from .enums import Religion, Strategy, LocationType


def calculate_conversion_rate(state: GameState, npc: NPC) -> float:
    """Calculate the conversion rate for an NPC based on current game state."""
    if state.chosen_location is None:
        return 0.0

    # Base rate for religion
    base_rate = CONVERSION_RATES[state.religion]

    # Apply all bonuses from game state
    base_rate += state.get_total_conversion_bonus()

    # Location multiplier (more converts = easier to convert)
    location_multiplier = state.chosen_location.get_conversion_rate_multiplier()

    # Strategy modifier
    if state.strategy == Strategy.INTENSE:
        strategy_modifier = 1.3
    else:
        strategy_modifier = 0.9

    # Calculate final rate with penalties
    adjusted_rate = base_rate * location_multiplier * strategy_modifier
    final_rate = adjusted_rate - (npc.failed_attempts * FAILED_ATTEMPT_PENALTY)

    # Clamp between 0 and max
    return max(0.0, min(MAX_CONVERSION_RATE, final_rate))


def attempt_conversion(state: GameState, npc: NPC) -> bool:
    """Attempt to convert an NPC. Returns True if successful."""
    if npc.resistant:
        return False

    conversion_rate = calculate_conversion_rate(state, npc)
    success = random.random() < conversion_rate

    # Use up pamphlet charge after attempt
    state.use_pamphlet_charge()

    return success


def apply_hunger(state: GameState, amount: int | None = None) -> int:
    """Apply hunger. If amount not specified, use weather-based amount."""
    if amount is None:
        if state.weather.is_harsh():
            amount = HUNGER_HARSH_WEATHER
        else:
            amount = HUNGER_NICE_WEATHER
    state.hunger += amount
    return state.hunger


def reduce_hunger(state: GameState, amount: int = FOOD_HUNGER_REDUCTION) -> None:
    """Reduce hunger by specified amount."""
    state.hunger = max(0, state.hunger - amount)


def is_day_over(state: GameState) -> bool:
    """Check if the day is over due to hunger."""
    return state.hunger >= MAX_HUNGER


def record_conversion(state: GameState, npc_id: int) -> None:
    """Record a successful conversion."""
    if state.chosen_location is None:
        return

    state.score += 1
    state.daily_score += 1

    if state.religion == Religion.SATANIC:
        state.satanic_score += 1

    state.chosen_location.convert(npc_id)


def apply_failed_attempt(npc: NPC, strategy: Strategy) -> None:
    """Apply penalty for failed conversion attempt."""
    if strategy == Strategy.INTENSE:
        npc.failed_attempts += 2
    else:
        npc.failed_attempts += 1


def set_random_weather(state: GameState) -> None:
    """Set random weather for the day."""
    from .enums import Weather
    state.weather = random.choice(list(Weather))


# Money system
def try_money_donation(state: GameState) -> int | None:
    """Try to get a money donation. Returns amount or None."""
    if random.random() < MONEY_DONATION_CHANCE:
        amount = random.randint(MONEY_DONATION_MIN, MONEY_DONATION_MAX)
        state.money += amount
        return amount
    return None


def apply_sunday_offering(state: GameState) -> int:
    """Apply Sunday offering bonus. Returns amount."""
    state.money += SUNDAY_OFFERING_BONUS
    return SUNDAY_OFFERING_BONUS


def can_afford(state: GameState, price: int) -> bool:
    """Check if player can afford an item."""
    return state.money >= price


def purchase_item(state: GameState, price: int) -> bool:
    """Attempt to purchase an item. Returns True if successful."""
    if can_afford(state, price):
        state.money -= price
        return True
    return False


# Church mechanics
def apply_friendly_church_buff(state: GameState) -> None:
    """Apply conversion buff from friendly church."""
    if state.current_neighborhood:
        state.current_neighborhood.church_influence += FRIENDLY_CHURCH_BUFF


def apply_hostile_church_debuff(state: GameState) -> None:
    """Apply conversion debuff and hunger cost from hostile church."""
    if state.current_neighborhood:
        state.current_neighborhood.church_influence += HOSTILE_CHURCH_DEBUFF
    apply_hunger(state, CHURCH_CHASE_HUNGER_COST)


def is_church_friendly(location: Location, player_religion: Religion) -> bool:
    """Check if a church is friendly to the player."""
    return location.is_friendly_church(player_religion)


def is_church_hostile(location: Location, player_religion: Religion) -> bool:
    """Check if a church is hostile to the player."""
    return location.is_hostile_church(player_religion)


# Library mechanics
def apply_library_hunger(state: GameState) -> None:
    """Apply hunger cost for library research."""
    apply_hunger(state, LIBRARY_RESEARCH_HUNGER)


def get_neighborhood_tip(neighborhood: Neighborhood) -> str:
    """Generate a tip about the neighborhood."""
    # Count resistant vs receptive NPCs
    total_npcs = 0
    resistant_count = 0

    for location in neighborhood.locations:
        for npc in location.npcs:
            if not npc.converted:
                total_npcs += 1
                if npc.resistant:
                    resistant_count += 1

    if total_npcs == 0:
        return "It seems like you've converted everyone here already!"

    receptive_ratio = (total_npcs - resistant_count) / total_npcs

    if receptive_ratio > 0.6:
        return f"The folks in {neighborhood.name} seem particularly open-minded. Good hunting ground!"
    elif receptive_ratio < 0.4:
        return f"The people of {neighborhood.name} are known to be set in their ways. Tough crowd."
    else:
        return f"{neighborhood.name} has a mixed community. Some will listen, some won't."


def reveal_npc_resistance(npc: NPC) -> None:
    """Mark an NPC's resistance as revealed."""
    npc.revealed_resistant = True


def get_all_npcs_in_neighborhood(neighborhood: Neighborhood) -> list[tuple[str, NPC]]:
    """Get all NPCs in a neighborhood with their location names."""
    result = []
    for location in neighborhood.locations:
        for npc in location.npcs:
            if not npc.converted:
                result.append((location.name, npc))
    return result
