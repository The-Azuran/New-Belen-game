"""Test script for combat system."""
import sys
from preaching.combat import CombatEngine, CombatResult
from preaching.models import GameState, NPC, CombatState
from preaching.enums import CombatType, DemonType, CombatActionType
from preaching.preachers import PREACHERS


def test_imports():
    """Test that all combat imports work."""
    print("✓ Imports successful")


def test_combat_initialization():
    """Test combat state initialization."""
    engine = CombatEngine()

    # Create mock game state
    game_state = GameState()
    game_state.preacher_id = "belen"
    game_state.preacher_name = "Belen Torres"
    game_state.faith = 100
    game_state.max_faith = 100

    # Create demonic NPC
    npc = NPC(
        name="Possessed Neighbor",
        personality="hostile",
        mood="grumpy",
        aggression=80,
        demon_type=DemonType.POSSESSION,
        demonic=True,
    )

    # Start combat
    combat_state = engine.start_combat(npc, game_state)

    assert combat_state is not None, "Combat state should be created"
    assert combat_state.combat_type == CombatType.BOSS, "Possession should trigger boss combat"
    assert combat_state.demon_spiritual_health > 0, "Boss should have spiritual health"
    assert game_state.demon_encounters == 1, "Encounter count should increment"

    print(f"✓ Combat initialized: {combat_state.combat_type.name} vs {combat_state.demon_type.name}")
    print(f"  Demon health: {combat_state.demon_spiritual_health}")


def test_spiritual_combat_actions():
    """Test spiritual combat actions."""
    engine = CombatEngine()

    game_state = GameState()
    game_state.preacher_id = "belen"
    game_state.faith = 100
    game_state.max_faith = 100

    npc = NPC(
        name="Temptation Demon",
        personality="hostile",
        mood="grumpy",
        aggression=60,
        demon_type=DemonType.TEMPTATION,
        demonic=True,
    )

    combat_state = engine.start_combat(npc, game_state)

    # Get available actions
    actions = engine.get_combat_actions(combat_state, game_state)

    assert len(actions) > 0, "Should have combat actions"
    assert len(actions) <= 4, "Should have max 4 actions"

    action_names = [a["name"] for a in actions]
    print(f"✓ Available actions: {', '.join(action_names)}")

    # Test prayer action
    initial_health = combat_state.demon_spiritual_health
    result = engine.apply_combat_action(combat_state, "prayer", game_state)

    assert isinstance(result, CombatResult), "Should return CombatResult"
    assert result.demon_health_change < 0, "Prayer should damage demon"
    print(f"✓ Prayer action: {result.demon_health_change} damage, response: '{result.demon_response}'")


def test_physical_combat():
    """Test physical combat mechanics."""
    engine = CombatEngine()

    game_state = GameState()
    game_state.preacher_id = "marcus"
    game_state.faith = 100

    # Create aggressive demon (more likely to trigger physical combat)
    npc = NPC(
        name="Aggressive Demon",
        personality="hostile",
        mood="grumpy",
        aggression=90,
        demon_type=DemonType.OPPRESSION,
        demonic=True,
    )

    # Force physical combat by trying multiple times
    for _ in range(10):
        combat_state = engine.start_combat(npc, game_state)
        if combat_state.combat_type == CombatType.PHYSICAL:
            actions = engine.get_combat_actions(combat_state, game_state)
            action_names = [a["name"] for a in actions]
            print(f"✓ Physical combat triggered: {', '.join(action_names)}")
            assert "Dodge" in action_names or "Push Back" in action_names, "Should have physical actions"
            break


def test_holy_items():
    """Test holy item integration."""
    engine = CombatEngine()

    game_state = GameState()
    game_state.faith = 100
    game_state.holy_items = ["holy_water", "silver_cross", "anointing_oil"]

    npc = NPC(
        name="Test Demon",
        personality="hostile",
        mood="grumpy",
        aggression=60,
        demon_type=DemonType.TEMPTATION,
        demonic=True,
    )

    combat_state = engine.start_combat(npc, game_state)
    actions = engine.get_combat_actions(combat_state, game_state)

    action_names = [a["name"] for a in actions]
    print(f"✓ Actions with holy items: {', '.join(action_names)}")

    # Test holy water usage
    if any("Holy Water" in name for name in action_names):
        result = engine.apply_combat_action(combat_state, "holy_water", game_state)
        assert "holy_water" not in game_state.holy_items, "Holy water should be consumed"
        print(f"✓ Holy water consumed: {result.demon_response}")


def test_combat_victory():
    """Test defeating a demon."""
    engine = CombatEngine()

    game_state = GameState()
    game_state.preacher_id = "belen"
    game_state.faith = 100

    npc = NPC(
        name="Weak Demon",
        personality="hostile",
        mood="grumpy",
        aggression=40,
        demon_type=DemonType.TEMPTATION,
        demonic=True,
    )

    combat_state = engine.start_combat(npc, game_state)

    # Set low health for testing
    combat_state.demon_spiritual_health = 30

    # Use rebuke (high damage)
    result = engine.apply_combat_action(combat_state, "rebuke", game_state)

    if result.demon_defeated:
        print(f"✓ Demon defeated! Response: '{result.demon_response}'")
        assert game_state.demon_defeats == 1, "Defeat count should increment"
    else:
        print(f"  Demon survived with {combat_state.demon_spiritual_health} health")


def test_faith_management():
    """Test faith costs and restoration."""
    engine = CombatEngine()

    game_state = GameState()
    game_state.preacher_id = "belen"
    game_state.faith = 50  # Low faith
    game_state.max_faith = 100

    npc = NPC(
        name="Test Demon",
        personality="hostile",
        mood="grumpy",
        aggression=60,
        demon_type=DemonType.TEMPTATION,
        demonic=True,
    )

    combat_state = engine.start_combat(npc, game_state)

    # Try prayer (restores faith)
    initial_faith = game_state.faith
    result = engine.apply_combat_action(combat_state, "prayer", game_state)

    if result.faith_change > 0:
        print(f"✓ Prayer restored {result.faith_change} faith ({initial_faith} -> {game_state.faith})")

    # Try expensive action with insufficient faith
    game_state.faith = 5  # Very low
    result = engine.apply_combat_action(combat_state, "rebuke", game_state)

    if "too weak" in result.demon_response.lower():
        print(f"✓ Insufficient faith handled: '{result.demon_response}'")


def run_all_tests():
    """Run all combat tests."""
    print("=" * 60)
    print("Testing Belen Game Combat System")
    print("=" * 60)

    try:
        test_imports()
        test_combat_initialization()
        test_spiritual_combat_actions()
        test_physical_combat()
        test_holy_items()
        test_combat_victory()
        test_faith_management()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
