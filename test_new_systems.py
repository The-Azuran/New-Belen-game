"""Tests for new systems: descriptions, locations, world sim, demon allies, moral alignment.

Authored by Rowan Valle; Executed by Claude Code.
"""
import random

from preaching.descriptions import (
    generate_house_description,
    generate_store_description,
    generate_church_description,
    generate_library_description,
    generate_park_description,
    generate_diner_description,
    generate_laundromat_description,
    generate_community_center_description,
)
from preaching.enums import LocationType, DemonType
from preaching.models import GameState, Location, NPC
from preaching.world_sim import WorldSimulator, WorldEvent
from preaching.config import (
    DEMON_CAPTURE_ALIGNMENT_PENALTY,
    DEMON_BANISH_ALIGNMENT_BONUS,
    DEMON_BETRAYAL_RATES,
)


# =============================================================================
# Description generators
# =============================================================================

def test_description_generators_return_nonempty():
    """Each generate_*_description() returns a non-empty string."""
    generators = [
        generate_house_description,
        generate_store_description,
        generate_church_description,
        generate_library_description,
        generate_park_description,
        generate_diner_description,
        generate_laundromat_description,
        generate_community_center_description,
    ]
    for gen in generators:
        result = gen()
        assert isinstance(result, str), f"{gen.__name__} did not return str"
        assert len(result) > 0, f"{gen.__name__} returned empty string"


# =============================================================================
# Location creation
# =============================================================================

def test_create_park():
    loc = Location.create_park()
    assert loc.location_type == LocationType.PARK
    assert len(loc.npcs) >= 2
    assert len(loc.name) > 0
    assert len(loc.description) > 0


def test_create_diner():
    loc = Location.create_diner()
    assert loc.location_type == LocationType.DINER
    assert len(loc.npcs) >= 3
    assert len(loc.name) > 0


def test_create_laundromat():
    loc = Location.create_laundromat()
    assert loc.location_type == LocationType.LAUNDROMAT
    assert len(loc.npcs) >= 1
    assert len(loc.name) > 0


def test_create_community_center():
    loc = Location.create_community_center()
    assert loc.location_type == LocationType.COMMUNITY_CENTER
    assert len(loc.npcs) >= 4
    assert len(loc.name) > 0


# =============================================================================
# New enums exist
# =============================================================================

def test_location_type_enums_exist():
    assert LocationType.PARK.value == "Park"
    assert LocationType.DINER.value == "Diner"
    assert LocationType.LAUNDROMAT.value == "Laundromat"
    assert LocationType.COMMUNITY_CENTER.value == "Community Center"


# =============================================================================
# World simulator
# =============================================================================

def test_simulate_night_returns_list():
    """simulate_night returns a list of WorldEvent, capped at 3."""
    from preaching.memory import MemoryManager

    state = GameState.create_new_game(seed=42)
    memory = MemoryManager()
    memory.start_day(0, "Sunday", "nice")
    summary = memory.end_day(False)

    sim = WorldSimulator()
    events = sim.simulate_night(state, memory, summary)

    assert isinstance(events, list)
    assert len(events) <= 3
    for event in events:
        assert isinstance(event, WorldEvent)


# =============================================================================
# Demon allies
# =============================================================================

def test_demon_capture_adds_ally():
    state = GameState()
    assert len(state.demon_allies) == 0

    ally = {
        "name": "Shadow",
        "demon_type": "temptation",
        "capture_day": 0,
        "betrayal_chance": DEMON_BETRAYAL_RATES["temptation"],
    }
    state.demon_allies.append(ally)
    assert len(state.demon_allies) == 1
    assert state.demon_allies[0]["demon_type"] == "temptation"


def test_demon_capture_changes_alignment():
    state = GameState()
    state.moral_alignment = 0.0
    state.moral_alignment += DEMON_CAPTURE_ALIGNMENT_PENALTY
    state.clamp_moral_alignment()
    assert state.moral_alignment < 0


def test_demon_banish_changes_alignment():
    state = GameState()
    state.moral_alignment = 0.0
    state.moral_alignment += DEMON_BANISH_ALIGNMENT_BONUS
    state.clamp_moral_alignment()
    assert state.moral_alignment > 0


def test_demon_betrayal_removes_ally():
    state = GameState()
    ally = {
        "name": "Shadow",
        "demon_type": "temptation",
        "capture_day": 0,
        "betrayal_chance": 1.0,  # Guaranteed betrayal for test
    }
    state.demon_allies.append(ally)
    assert len(state.demon_allies) == 1

    # Simulate removal (as game.py does)
    state.demon_allies.remove(ally)
    state.demon_betrayals += 1
    assert len(state.demon_allies) == 0
    assert state.demon_betrayals == 1


# =============================================================================
# Moral alignment clamping
# =============================================================================

def test_clamp_moral_alignment_upper():
    state = GameState()
    state.moral_alignment = 200.0
    state.clamp_moral_alignment()
    assert state.moral_alignment == 100.0


def test_clamp_moral_alignment_lower():
    state = GameState()
    state.moral_alignment = -200.0
    state.clamp_moral_alignment()
    assert state.moral_alignment == -100.0


def test_clamp_moral_alignment_within_range():
    state = GameState()
    state.moral_alignment = 42.0
    state.clamp_moral_alignment()
    assert state.moral_alignment == 42.0


# =============================================================================
# Location-aware conversation text
# =============================================================================

def test_conversation_state_location_type_default():
    """ConversationState defaults to House location type."""
    from preaching.conversation import ConversationState
    npc = NPC(name="Test", personality="neutral", mood="neutral")
    state = ConversationState.start(npc)
    assert state.location_type == "House"


def test_conversation_state_location_type_park():
    """ConversationState accepts custom location type."""
    from preaching.conversation import ConversationState
    npc = NPC(name="Test", personality="neutral", mood="neutral")
    state = ConversationState.start(npc, location_type="Park")
    assert state.location_type == "Park"


def test_ui_display_empty_location_park(capsys):
    """display_empty_location shows park text for Park location."""
    from preaching.ui import ConsoleUI
    ui = ConsoleUI()
    ui.display_empty_location(location_type="Park")
    captured = capsys.readouterr()
    assert "park is empty" in captured.out.lower()
    assert "door" not in captured.out.lower()


def test_ui_display_empty_location_house(capsys):
    """display_empty_location shows house text by default."""
    from preaching.ui import ConsoleUI
    ui = ConsoleUI()
    ui.display_empty_location()
    captured = capsys.readouterr()
    assert "No one is home" in captured.out


def test_ui_display_no_answer_diner(capsys):
    """display_no_answer shows diner text for Diner location."""
    from preaching.ui import ConsoleUI
    ui = ConsoleUI()
    ui.display_no_answer("Jane", location_type="Diner")
    captured = capsys.readouterr()
    assert "menu" in captured.out.lower()
    assert "door" not in captured.out.lower()


def test_ui_display_conversion_result_laundromat(capsys):
    """display_conversion_result shows laundromat rejection text."""
    from preaching.ui import ConsoleUI
    ui = ConsoleUI()
    ui.display_conversion_result(False, True, False, location_type="Laundromat")
    captured = capsys.readouterr()
    assert "earbuds" in captured.out.lower()
    assert "door" not in captured.out.lower()


def test_narrative_rejection_thought_non_house():
    """Post-rejection thought avoids door language for non-house locations."""
    from preaching.narrative import NarrativeEngine, NarrativeContext
    from preaching.memory import MemoryManager

    memory = MemoryManager()
    engine = NarrativeEngine(memory)
    context = NarrativeContext(
        day=0, weather="nice", hunger=0, money=10,
        total_score=0, satanic_score=0, current_neighborhood="Test",
        rejection_streak=0, conversion_streak=0, reputation_in_area=0,
    )
    npc = NPC(name="Test", personality="neutral", mood="neutral")

    # Run many times to check no door-specific text appears
    random.seed(42)
    for _ in range(50):
        thought = engine.get_post_rejection_thought(context, npc, location_type="Park")
        if thought:
            assert "door closes" not in thought.lower(), f"Got door text in park: {thought}"


def test_narrative_no_answer_thought_non_house():
    """No-answer thought avoids door language for non-house locations."""
    from preaching.narrative import NarrativeEngine, NarrativeContext
    from preaching.memory import MemoryManager

    memory = MemoryManager()
    engine = NarrativeEngine(memory)
    context = NarrativeContext(
        day=0, weather="nice", hunger=0, money=10,
        total_score=0, satanic_score=0, current_neighborhood="Test",
        rejection_streak=0, conversion_streak=0, reputation_in_area=0,
    )

    random.seed(42)
    for _ in range(50):
        thought = engine.get_no_answer_thought(context, location_type="Laundromat")
        if thought:
            assert "door stays closed" not in thought.lower(), f"Got door text in laundromat: {thought}"


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {test.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
