"""
Combat engine - extends ConversationEngine for spiritual warfare combat.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .models import NPC, GameState, CombatState
    from .enums import CombatType, DemonType, CombatActionType

from .conversation import ConversationEngine, ConversationResult
from .enums import CombatType, DemonType, CombatActionType


@dataclass
class CombatResult:
    """Result of a combat action."""
    demon_response: str
    faith_change: int = 0
    demon_health_change: int = 0
    player_health_change: int = 0
    combat_ended: bool = False
    demon_defeated: bool = False
    player_fled: bool = False
    modifiers: List[tuple[str, int]] = field(default_factory=list)


class CombatEngine(ConversationEngine):
    """Extends ConversationEngine for combat mechanics."""

    def start_combat(self, npc: NPC, game_state: GameState) -> CombatState:
        """Start a combat encounter with a demonic NPC.

        Args:
            npc: The demonic NPC to fight
            game_state: Current game state

        Returns:
            CombatState object tracking the combat
        """
        # Determine combat type: 75% spiritual, 25% physical based on aggression
        # Boss demons (possession) are always spiritual combat
        if npc.demon_type == DemonType.POSSESSION:
            combat_type = CombatType.BOSS
        elif random.random() < 0.25 and npc.aggression > 50:
            combat_type = CombatType.PHYSICAL
        else:
            combat_type = CombatType.SPIRITUAL

        # Set demon health based on type and combat type
        if combat_type == CombatType.BOSS:
            # Boss demons have high spiritual health
            demon_health = random.randint(80, 120)  # High spiritual health for boss
            physical_health = 0
        elif combat_type == CombatType.SPIRITUAL:
            demon_health = random.randint(40, 80)  # Spiritual health
            physical_health = 0
        else:
            demon_health = 0
            physical_health = random.randint(20, 60)  # Physical health

        # Create combat state
        from .models import CombatState
        combat_state = CombatState(
            combat_type=combat_type,
            demon_type=npc.demon_type or DemonType.TEMPTATION,
            npc=npc,
            player_faith=game_state.faith,
            demon_spiritual_health=demon_health,
            demon_physical_health=physical_health,
        )

        # Track encounter
        game_state.demon_encounters += 1
        game_state.current_combat = combat_state

        return combat_state

    def get_combat_actions(self, state: CombatState, game_state: GameState) -> List[dict]:
        """Get available combat actions based on combat type and state.

        Returns 4 actions max (matches conversation UI).
        """
        actions = []

        if state.combat_type == CombatType.SPIRITUAL:
            # Spiritual combat actions
            spiritual_actions = [
                {
                    "id": "prayer",
                    "name": "Pray",
                    "description": "Pray for strength (restores 5-10 faith, damages demon)",
                    "faith_restore": random.randint(5, 10),
                    "damage": 10,
                    "type": CombatActionType.PRAYER,
                },
                {
                    "id": "scripture",
                    "name": "Quote Scripture",
                    "description": "Quote holy scripture (costs 10 faith, good damage)",
                    "faith_cost": 10,
                    "damage": 20,
                    "type": CombatActionType.SCRIPTURE,
                },
                {
                    "id": "rebuke",
                    "name": "Rebuke Demon",
                    "description": "Command demon to leave (costs 15 faith, high damage)",
                    "faith_cost": 15,
                    "damage": 35,
                    "type": CombatActionType.REBUKE,
                },
            ]
            actions.extend(spiritual_actions)
        else:
            # Physical combat actions
            physical_actions = [
                {
                    "id": "dodge",
                    "name": "Dodge",
                    "description": "Avoid demon's attack (no cost, reduces damage)",
                    "faith_cost": 0,
                    "damage_reduction": 0.5,
                    "type": CombatActionType.DODGE,
                },
                {
                    "id": "push",
                    "name": "Push Back",
                    "description": "Push demon away (costs 5 faith, minor damage)",
                    "faith_cost": 5,
                    "damage": 5,
                    "type": CombatActionType.PUSH,
                },
                {
                    "id": "restrain",
                    "name": "Attempt Restraint",
                    "description": "Try to restrain demon (costs 10 faith, chance to stun)",
                    "faith_cost": 10,
                    "damage": 0,
                    "stun_chance": 0.3,
                    "type": CombatActionType.RESTRAIN,
                },
            ]
            actions.extend(physical_actions)

        # Add item actions if player has holy items
        if "holy_water" in game_state.holy_items:
            actions.append({
                "id": "holy_water",
                "name": "Use Holy Water",
                "description": "Splash holy water on demon (no cost, 20 damage)",
                "faith_cost": 0,
                "damage": 20,
                "consumes_item": "holy_water",
                "type": CombatActionType.USE_HOLY_WATER,
            })

        if "silver_cross" in game_state.holy_items:
            actions.append({
                "id": "silver_cross",
                "name": "Brandish Cross",
                "description": "Show silver cross (no cost, +50% faith regen this combat)",
                "faith_cost": 0,
                "faith_regen_bonus": 0.5,
                "type": CombatActionType.USE_CROSS,
            })

        if "anointing_oil" in game_state.holy_items:
            actions.append({
                "id": "anointing_oil",
                "name": "Anoint with Oil",
                "description": "Apply holy oil (+25% damage vs oppression demons)",
                "faith_cost": 0,
                "damage_bonus": 0.25,
                "type": CombatActionType.USE_OIL,
            })

        # Limit to 4 actions (matching conversation UI)
        if len(actions) > 4:
            # Prioritize: spiritual/physical actions first, then items
            spiritual_count = sum(1 for a in actions if a["type"] in [
                CombatActionType.PRAYER, CombatActionType.SCRIPTURE, CombatActionType.REBUKE,
                CombatActionType.DODGE, CombatActionType.PUSH, CombatActionType.RESTRAIN
            ])
            if spiritual_count >= 4:
                actions = [a for a in actions if a["type"] in [
                    CombatActionType.PRAYER, CombatActionType.SCRIPTURE, CombatActionType.REBUKE,
                    CombatActionType.DODGE, CombatActionType.PUSH, CombatActionType.RESTRAIN
                ]][:4]
            else:
                # Keep all spiritual actions and top items
                spiritual_actions = [a for a in actions if a["type"] in [
                    CombatActionType.PRAYER, CombatActionType.SCRIPTURE, CombatActionType.REBUKE,
                    CombatActionType.DODGE, CombatActionType.PUSH, CombatActionType.RESTRAIN
                ]]
                item_actions = [a for a in actions if a["type"] not in [
                    CombatActionType.PRAYER, CombatActionType.SCRIPTURE, CombatActionType.REBUKE,
                    CombatActionType.DODGE, CombatActionType.PUSH, CombatActionType.RESTRAIN
                ]]
                # Take enough items to reach 4 total
                actions = spiritual_actions + item_actions[:4 - len(spiritual_actions)]

        return actions

    def apply_combat_action(self, state: CombatState, action_id: str, game_state: GameState) -> CombatResult:
        """Apply a combat action and calculate results.

        Args:
            state: Current combat state
            action_id: ID of the action to apply
            game_state: Current game state

        Returns:
            CombatResult with outcome
        """
        # Get available actions
        actions = self.get_combat_actions(state, game_state)
        action = next((a for a in actions if a["id"] == action_id), None)

        if not action:
            # Fallback to prayer
            action = {
                "id": "prayer",
                "name": "Pray",
                "description": "Pray for strength",
                "faith_cost": 5,
                "damage": 10,
                "type": CombatActionType.PRAYER,
            }

        modifiers = []
        faith_change = 0
        demon_health_change = 0
        player_health_change = 0

        # Apply faith cost
        faith_cost = action.get("faith_cost", 0)
        if faith_cost > 0:
            if game_state.faith >= faith_cost:
                game_state.faith -= faith_cost
                faith_change = -faith_cost
                modifiers.append(("faith cost", -faith_cost))
            else:
                # Not enough faith - action fails
                return CombatResult(
                    demon_response="Your faith is too weak! The demon laughs at your attempt.",
                    faith_change=0,
                    demon_health_change=0,
                    player_health_change=-5,  # Take damage for failed action
                    combat_ended=False,
                    demon_defeated=False,
                    player_fled=False,
                    modifiers=[("insufficient faith", -5)],
                )

        # Apply action effects based on type
        action_type = action.get("type")

        if action_type == CombatActionType.PRAYER:
            damage = action.get("damage", 10)
            faith_restore = action.get("faith_restore", random.randint(5, 10))

            # Apply preacher bonus if applicable
            if state.demon_type == DemonType.TEMPTATION:
                # Belen gets +25% vs temptation
                if game_state.preacher_id == "belen":
                    damage = int(damage * 1.25)
                    modifiers.append(("Belen's ex-witch insight", int(damage * 0.25)))

            demon_health_change = -damage
            modifiers.append(("prayer damage", -damage))

            # Restore faith
            old_faith = game_state.faith
            game_state.faith = min(game_state.max_faith, game_state.faith + faith_restore)
            actual_restore = game_state.faith - old_faith
            if actual_restore > 0:
                faith_change = actual_restore
                modifiers.append(("faith restored", actual_restore))

            # Demon response
            demon_response = self._get_demon_response(state, "prayer", damage)

        elif action_type == CombatActionType.SCRIPTURE:
            damage = action.get("damage", 20)
            demon_health_change = -damage
            modifiers.append(("scripture damage", -damage))
            demon_response = self._get_demon_response(state, "scripture", damage)

        elif action_type == CombatActionType.REBUKE:
            damage = action.get("damage", 35)
            demon_health_change = -damage
            modifiers.append(("rebuke damage", -damage))
            demon_response = self._get_demon_response(state, "rebuke", damage)

        elif action_type == CombatActionType.DODGE:
            # Dodge reduces next demon attack
            demon_response = "You dodge the demon's attack!"
            modifiers.append(("dodged", 0))

        elif action_type == CombatActionType.PUSH:
            damage = action.get("damage", 5)
            demon_health_change = -damage
            modifiers.append(("push damage", -damage))
            demon_response = self._get_demon_response(state, "push", damage)

        elif action_type == CombatActionType.RESTRAIN:
            stun_chance = action.get("stun_chance", 0.3)
            if random.random() < stun_chance:
                demon_response = "You manage to restrain the demon temporarily!"
                modifiers.append(("restrained", 0))
            else:
                demon_response = "The demon breaks free from your grasp!"
                player_health_change = -5
                modifiers.append(("failed restraint", -5))

        elif action_type == CombatActionType.USE_HOLY_WATER:
            damage = action.get("damage", 20)
            demon_health_change = -damage
            modifiers.append(("holy water damage", -damage))
            # Consume the item
            if "holy_water" in game_state.holy_items:
                game_state.holy_items.remove("holy_water")
            demon_response = self._get_demon_response(state, "holy_water", damage)

        elif action_type == CombatActionType.USE_CROSS:
            faith_regen_bonus = action.get("faith_regen_bonus", 0.5)
            # Apply faith regeneration bonus for this combat
            demon_response = "The silver cross glows with divine light!"
            modifiers.append(("faith regen +50%", 0))

        elif action_type == CombatActionType.USE_OIL:
            damage_bonus = action.get("damage_bonus", 0.25)
            # Apply damage bonus vs oppression demons
            if state.demon_type == DemonType.OPPRESSION:
                demon_response = "The anointing oil weakens the oppressive demon!"
                modifiers.append(("+25% vs oppression", 0))
            else:
                demon_response = "The oil has little effect on this type of demon."

        else:
            # Unknown action
            demon_response = "Your action has no apparent effect."

        # Update combat state
        state.turn += 1

        if state.combat_type == CombatType.SPIRITUAL:
            state.demon_spiritual_health += demon_health_change
        else:
            state.demon_physical_health += demon_health_change

        # Check if demon is defeated
        demon_defeated = False
        if state.combat_type == CombatType.SPIRITUAL:
            if state.demon_spiritual_health <= 0:
                demon_defeated = True
        else:
            if state.demon_physical_health <= 0:
                demon_defeated = True

        if demon_defeated:
            game_state.demon_defeats += 1
            demon_response += " The demon flees in defeat!"

        return CombatResult(
            demon_response=demon_response,
            faith_change=faith_change,
            demon_health_change=demon_health_change,
            player_health_change=player_health_change,
            combat_ended=demon_defeated,
            demon_defeated=demon_defeated,
            player_fled=False,
            modifiers=modifiers,
        )

    def _get_demon_response(self, state: CombatState, action_type: str, damage: int) -> str:
        """Get appropriate demon response based on action and damage."""
        responses = {
            "prayer": [
                "The demon recoils from your prayer!",
                "Your prayer weakens the demon's hold.",
                "The demon scoffs at your prayer.",
            ],
            "scripture": [
                "The holy scripture burns the demon!",
                "The demon writhes in pain from the scripture.",
                "The scripture has little effect.",
            ],
            "rebuke": [
                "The demon screams as you command it to leave!",
                "Your rebuke shakes the very foundations!",
                "The demon resists your rebuke.",
            ],
            "push": [
                "You push the demon back!",
                "The demon stumbles from your push.",
                "The demon barely moves.",
            ],
            "holy_water": [
                "The holy water sizzles on the demon's skin!",
                "The demon howls in pain from the holy water!",
                "The holy water evaporates on contact.",
            ],
        }

        # Select response based on damage
        if damage > 25:
            response_index = 0  # High damage response
        elif damage > 10:
            response_index = 1  # Medium damage response
        else:
            response_index = 2  # Low damage response

        action_responses = responses.get(action_type, ["The demon reacts."])
        if response_index < len(action_responses):
            return action_responses[response_index]
        return action_responses[0]

    def end_combat(self, state: CombatState, game_state: GameState, player_fled: bool = False) -> None:
        """Clean up combat state and apply post-combat effects."""
        game_state.current_combat = None

        # Apply hunger cost for combat
        if state.combat_type == CombatType.PHYSICAL:
            hunger_cost = random.randint(15, 25)
        else:
            hunger_cost = random.randint(10, 15)

        game_state.hunger = min(100, game_state.hunger + hunger_cost)

        # Apply reputation changes
        if state.demon_spiritual_health <= 0 or state.demon_physical_health <= 0:
            # Demon defeated
            game_state.reputation.add_reputation("demon_defeated", 5)
        elif player_fled:
            # Player fled
            game_state.reputation.add_reputation("fled_combat", -3)