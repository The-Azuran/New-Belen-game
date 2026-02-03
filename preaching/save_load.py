"""Save/Load system for game state persistence."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, fields
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .memory import MemoryManager

from .models import (
    GameState, County, Town, Neighborhood, Street,
    Location, NPC, InventoryItem
)
from .enums import Weather, Religion, Strategy, LocationType
from .memory import Memory, DaySummary, EventType, MemoryManager
from .reputation import ReputationManager

# Save file version for compatibility checking
SAVE_VERSION = "1.0"


def _validate_personality(personality: str) -> str:
    """Validate personality is known, default to skeptic if unknown."""
    from .dialogue import PERSONALITIES
    if personality not in PERSONALITIES:
        return "skeptic"
    return personality


def _validate_mood(mood: str) -> str:
    """Validate mood is known, default to neutral if unknown."""
    from .dialogue import MOODS
    if mood not in MOODS:
        return "neutral"
    return mood


def get_save_directory() -> Path:
    """Get the save directory, creating it if needed."""
    save_dir = Path.home() / ".preaching_the_truth" / "saves"
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def _serialize_enum(value: Any) -> str | None:
    """Convert an enum to its string value."""
    if value is None:
        return None
    return value.value


def _serialize_npc(npc: NPC) -> dict:
    """Serialize an NPC to a dict."""
    return {
        "name": npc.name,
        "personality": npc.personality,
        "mood": npc.mood,
        "converted": npc.converted,
        "failed_attempts": npc.failed_attempts,
        "resistant": npc.resistant,
        "revealed_resistant": npc.revealed_resistant,
    }


def _serialize_location(location: Location) -> dict:
    """Serialize a Location to a dict."""
    return {
        "location_type": location.location_type.value,
        "name": location.name,
        "npcs": [_serialize_npc(npc) for npc in location.npcs],
        "affiliation": _serialize_enum(location.affiliation),
        "inventory": [],  # Store inventory is regenerated, not saved
    }


def _serialize_street(street: Street) -> dict:
    """Serialize a Street to a dict."""
    return {
        "name": street.name,
        "locations": [_serialize_location(loc) for loc in street.locations],
    }


def _serialize_neighborhood(neighborhood: Neighborhood) -> dict:
    """Serialize a Neighborhood to a dict."""
    return {
        "name": neighborhood.name,
        "streets": [_serialize_street(street) for street in neighborhood.streets],
        "church_influence": neighborhood.church_influence,
    }


def _serialize_town(town: Town) -> dict:
    """Serialize a Town to a dict."""
    return {
        "name": town.name,
        "neighborhoods": [_serialize_neighborhood(n) for n in town.neighborhoods],
    }


def _serialize_county(county: County) -> dict:
    """Serialize a County to a dict."""
    return {
        "name": county.name,
        "towns": [_serialize_town(town) for town in county.towns],
    }


def _serialize_inventory_item(item: InventoryItem) -> dict:
    """Serialize an InventoryItem to a dict."""
    return {
        "item_type": item.item_type,
        "name": item.name,
        "description": item.description,
        "hunger_restore": item.hunger_restore,
        "pamphlet_id": item.pamphlet_id,
        "pamphlet_tags": item.pamphlet_tags,
    }


def _serialize_memory(memory: Memory) -> dict:
    """Serialize a Memory to a dict."""
    return {
        "day": memory.day,
        "event_type": memory.event_type.value,
        "neighborhood": memory.neighborhood,
        "npc_name": memory.npc_name,
        "npc_personality": memory.npc_personality,
        "location_name": memory.location_name,
        "tags": memory.tags,
        "details": memory.details,
    }


def _serialize_day_summary(summary: DaySummary) -> dict:
    """Serialize a DaySummary to a dict."""
    return {
        "day": summary.day,
        "day_name": summary.day_name,
        "weather": summary.weather,
        "conversions": summary.conversions,
        "rejections": summary.rejections,
        "polite_exits": summary.polite_exits,
        "doors_unanswered": summary.doors_unanswered,
        "money_earned": summary.money_earned,
        "money_spent": summary.money_spent,
        "hostile_churches": summary.hostile_churches,
        "friendly_churches": summary.friendly_churches,
        "neighborhoods_visited": summary.neighborhoods_visited,
        "notable_npcs": summary.notable_npcs,
        "satanic_events": summary.satanic_events,
        "ended_hungry": summary.ended_hungry,
        "tags": summary.tags,
    }


def _find_location_indices(state: GameState) -> dict:
    """Find indices for current location references."""
    indices = {
        "town_idx": None,
        "neighborhood_idx": None,
        "street_idx": None,
        "location_idx": None,
    }

    if not state.county:
        return indices

    # Find current town
    if state.current_town:
        try:
            indices["town_idx"] = state.county.towns.index(state.current_town)
        except ValueError:
            pass

    # Find current neighborhood
    if state.current_neighborhood and state.current_town:
        try:
            indices["neighborhood_idx"] = state.current_town.neighborhoods.index(
                state.current_neighborhood
            )
        except ValueError:
            pass

    # Find current street
    if state.current_street and state.current_neighborhood:
        try:
            indices["street_idx"] = state.current_neighborhood.streets.index(
                state.current_street
            )
        except ValueError:
            pass

    # Find chosen location
    if state.chosen_location and state.current_street:
        try:
            indices["location_idx"] = state.current_street.locations.index(
                state.chosen_location
            )
        except ValueError:
            pass

    return indices


def serialize_game_state(state: GameState, memory: MemoryManager) -> dict:
    """Serialize the complete game state to a JSON-compatible dict."""
    indices = _find_location_indices(state)

    return {
        "metadata": {
            "version": SAVE_VERSION,
            "timestamp": datetime.now().isoformat(),
            "preacher_name": state.preacher_name,
            "day": state.day_of_week,
            "score": state.score,
        },
        "state": {
            "score": state.score,
            "satanic_score": state.satanic_score,
            "hunger": state.hunger,
            "money": state.money,
            "religion": _serialize_enum(state.religion),
            "strategy": _serialize_enum(state.strategy),
            "weather": _serialize_enum(state.weather),
            "day_of_week": state.day_of_week,
            "daily_score": state.daily_score,
            "satanic_bonus": state.satanic_bonus,
            "pamphlet_boost_remaining": state.pamphlet_boost_remaining,
            "pamphlet_boost_amount": state.pamphlet_boost_amount,
            "bible_bonus": state.bible_bonus,
            "active_pamphlet_tags": state.active_pamphlet_tags,
            "preacher_name": state.preacher_name,
            "preacher_id": state.preacher_id,
            "preacher_conversion_bonus": state.preacher_conversion_bonus,
            "preacher_hunger_rate": state.preacher_hunger_rate,
            "preacher_personality_bonus": state.preacher_personality_bonus,
            "world_seed": state.world_seed,
            "inventory": [_serialize_inventory_item(item) for item in state.inventory],
        },
        "world": _serialize_county(state.county) if state.county else None,
        "reputation": state.reputation.reputation,
        "memory": {
            "memories": [_serialize_memory(m) for m in memory.memories],
            "day_summaries": [_serialize_day_summary(s) for s in memory.day_summaries],
        },
        "indices": indices,
    }


def _deserialize_npc(data: dict) -> NPC:
    """Deserialize an NPC from a dict."""
    return NPC(
        name=data["name"],
        personality=_validate_personality(data["personality"]),
        mood=_validate_mood(data["mood"]),
        converted=data["converted"],
        failed_attempts=data["failed_attempts"],
        resistant=data["resistant"],
        revealed_resistant=data["revealed_resistant"],
    )


def _deserialize_location(data: dict) -> Location:
    """Deserialize a Location from a dict."""
    affiliation = None
    if data["affiliation"]:
        affiliation = Religion(data["affiliation"])

    return Location(
        location_type=LocationType(data["location_type"]),
        name=data["name"],
        npcs=[_deserialize_npc(npc) for npc in data["npcs"]],
        affiliation=affiliation,
        inventory=[],  # Stores regenerate inventory
    )


def _deserialize_street(data: dict) -> Street:
    """Deserialize a Street from a dict."""
    return Street(
        name=data["name"],
        locations=[_deserialize_location(loc) for loc in data["locations"]],
    )


def _deserialize_neighborhood(data: dict) -> Neighborhood:
    """Deserialize a Neighborhood from a dict."""
    return Neighborhood(
        name=data["name"],
        streets=[_deserialize_street(street) for street in data["streets"]],
        church_influence=data["church_influence"],
    )


def _deserialize_town(data: dict) -> Town:
    """Deserialize a Town from a dict."""
    return Town(
        name=data["name"],
        neighborhoods=[_deserialize_neighborhood(n) for n in data["neighborhoods"]],
    )


def _deserialize_county(data: dict) -> County:
    """Deserialize a County from a dict."""
    return County(
        name=data["name"],
        towns=[_deserialize_town(town) for town in data["towns"]],
    )


def _deserialize_inventory_item(data: dict) -> InventoryItem:
    """Deserialize an InventoryItem from a dict."""
    return InventoryItem(
        item_type=data["item_type"],
        name=data["name"],
        description=data["description"],
        hunger_restore=data["hunger_restore"],
        pamphlet_id=data["pamphlet_id"],
        pamphlet_tags=data["pamphlet_tags"],
    )


def _deserialize_memory(data: dict) -> Memory:
    """Deserialize a Memory from a dict."""
    return Memory(
        day=data["day"],
        event_type=EventType(data["event_type"]),
        neighborhood=data["neighborhood"],
        npc_name=data["npc_name"],
        npc_personality=data["npc_personality"],
        location_name=data["location_name"],
        tags=data["tags"],
        details=data["details"],
    )


def _deserialize_day_summary(data: dict) -> DaySummary:
    """Deserialize a DaySummary from a dict."""
    return DaySummary(
        day=data["day"],
        day_name=data["day_name"],
        weather=data["weather"],
        conversions=data["conversions"],
        rejections=data["rejections"],
        polite_exits=data["polite_exits"],
        doors_unanswered=data["doors_unanswered"],
        money_earned=data["money_earned"],
        money_spent=data["money_spent"],
        hostile_churches=data["hostile_churches"],
        friendly_churches=data["friendly_churches"],
        neighborhoods_visited=data["neighborhoods_visited"],
        notable_npcs=data["notable_npcs"],
        satanic_events=data["satanic_events"],
        ended_hungry=data["ended_hungry"],
        tags=data["tags"],
    )


def _restore_location_references(state: GameState, indices: dict) -> None:
    """Restore object references from saved indices."""
    if not state.county:
        return

    # Restore current town
    if indices.get("town_idx") is not None:
        try:
            state.current_town = state.county.towns[indices["town_idx"]]
        except (IndexError, TypeError):
            pass

    # Restore current neighborhood
    if indices.get("neighborhood_idx") is not None and state.current_town:
        try:
            state.current_neighborhood = state.current_town.neighborhoods[
                indices["neighborhood_idx"]
            ]
        except (IndexError, TypeError):
            pass

    # Restore current street
    if indices.get("street_idx") is not None and state.current_neighborhood:
        try:
            state.current_street = state.current_neighborhood.streets[
                indices["street_idx"]
            ]
        except (IndexError, TypeError):
            pass

    # Restore chosen location
    if indices.get("location_idx") is not None and state.current_street:
        try:
            state.chosen_location = state.current_street.locations[
                indices["location_idx"]
            ]
        except (IndexError, TypeError):
            pass


def deserialize_game_state(data: dict) -> tuple[GameState, MemoryManager]:
    """Deserialize a game state from a JSON-compatible dict."""
    # Validate save version
    version = data.get("metadata", {}).get("version", "1.0")
    if version != SAVE_VERSION:
        raise ValueError(f"Incompatible save version: {version} (expected {SAVE_VERSION})")

    state_data = data["state"]

    # Rebuild the world hierarchy
    county = None
    if data["world"]:
        county = _deserialize_county(data["world"])

    # Build flat neighborhood list for backward compatibility
    all_neighborhoods = []
    if county:
        for town in county.towns:
            all_neighborhoods.extend(town.neighborhoods)

    # Create the game state
    state = GameState(
        score=state_data["score"],
        satanic_score=state_data["satanic_score"],
        hunger=state_data["hunger"],
        money=state_data["money"],
        religion=Religion(state_data["religion"]),
        strategy=Strategy(state_data["strategy"]),
        weather=Weather(state_data["weather"]),
        county=county,
        neighborhoods=all_neighborhoods,
        day_of_week=state_data["day_of_week"],
        daily_score=state_data["daily_score"],
        satanic_bonus=state_data["satanic_bonus"],
        pamphlet_boost_remaining=state_data["pamphlet_boost_remaining"],
        pamphlet_boost_amount=state_data["pamphlet_boost_amount"],
        bible_bonus=state_data["bible_bonus"],
        active_pamphlet_tags=state_data["active_pamphlet_tags"],
        preacher_name=state_data["preacher_name"],
        preacher_id=state_data["preacher_id"],
        preacher_conversion_bonus=state_data["preacher_conversion_bonus"],
        preacher_hunger_rate=state_data["preacher_hunger_rate"],
        preacher_personality_bonus=state_data["preacher_personality_bonus"],
        world_seed=state_data.get("world_seed", 0),
        inventory=[_deserialize_inventory_item(item) for item in state_data["inventory"]],
        reputation=ReputationManager(reputation=data["reputation"]),
    )

    # Restore location references
    _restore_location_references(state, data["indices"])

    # Rebuild memory manager
    memory = MemoryManager()
    memory.memories = [_deserialize_memory(m) for m in data["memory"]["memories"]]
    memory.day_summaries = [
        _deserialize_day_summary(s) for s in data["memory"]["day_summaries"]
    ]

    return state, memory


def save_game(state: GameState, memory: MemoryManager, slot: int = 0) -> str:
    """Save the game to a slot file. Returns the save file path."""
    save_dir = get_save_directory()
    save_path = save_dir / f"slot_{slot}.json"

    data = serialize_game_state(state, memory)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return str(save_path)


def load_game(slot: int = 0) -> tuple[GameState, MemoryManager] | None:
    """Load a game from a slot file. Returns None if not found."""
    save_dir = get_save_directory()
    save_path = save_dir / f"slot_{slot}.json"

    if not save_path.exists():
        return None

    with open(save_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return deserialize_game_state(data)


def list_saves() -> list[dict]:
    """List all available save files with metadata."""
    save_dir = get_save_directory()
    saves = []

    for save_file in sorted(save_dir.glob("slot_*.json")):
        try:
            with open(save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            slot = int(save_file.stem.split("_")[1])
            saves.append({
                "slot": slot,
                "path": str(save_file),
                "metadata": data.get("metadata", {}),
            })
        except (json.JSONDecodeError, KeyError, ValueError):
            # Skip corrupted saves
            continue

    return saves


def delete_save(slot: int) -> bool:
    """Delete a save file. Returns True if deleted, False if not found."""
    save_dir = get_save_directory()
    save_path = save_dir / f"slot_{slot}.json"

    if save_path.exists():
        save_path.unlink()
        return True
    return False
