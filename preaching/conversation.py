"""
Conversation engine - handles the back-and-forth preaching encounters.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .models import NPC, GameState

from .dialogue import (
    PERSONALITIES,
    MOODS,
    OPENERS,
    OBJECTIONS,
    RESPONSES,
    POSITIVE_REACTIONS,
    NEGATIVE_REACTIONS,
    CONVERSION_LINES,
    CONVERSION_THRESHOLD,
    REJECTION_THRESHOLD,
    INTEREST_PER_GOOD_MATCH,
    INTEREST_PER_BAD_MATCH,
)


@dataclass
class ConversationResult:
    """Result of a player action in conversation."""
    npc_response: str
    interest_change: int
    new_interest: int
    is_positive: bool
    conversation_ended: bool = False
    converted: bool = False
    rejected: bool = False
    polite_exit: bool = False


@dataclass
class ConversationState:
    """Tracks the state of an ongoing conversation."""
    npc_name: str
    personality: str
    mood: str
    interest: int = 0
    patience: int = 4
    turn: int = 0
    objections_raised: list[str] = field(default_factory=list)
    opener_used: Optional[str] = None
    active_pamphlet_tags: list[str] = field(default_factory=list)
    preacher_personality_bonus: dict[str, float] = field(default_factory=dict)

    @classmethod
    def start(
        cls,
        npc: NPC,
        reputation_bonus: int = 0,
        pamphlet_tags: list[str] | None = None,
        preacher_personality_bonus: dict[str, float] | None = None,
    ) -> ConversationState:
        """Start a new conversation with an NPC."""
        mood_data = MOODS.get(npc.mood, MOODS["neutral"])
        starting_interest = mood_data["interest_bonus"] + reputation_bonus
        patience = mood_data["patience"]

        # Apply preacher's personality bonus as starting interest
        personality_bonus = preacher_personality_bonus or {}
        if npc.personality in personality_bonus:
            # Convert percentage to interest points (e.g., 0.10 = +5 interest)
            starting_interest += int(personality_bonus[npc.personality] * 50)

        # Resistant NPCs start with a severe interest penalty
        if npc.resistant:
            starting_interest -= 25
            patience = max(2, patience - 1)  # Less patient too

        return cls(
            npc_name=npc.name,
            personality=npc.personality,
            mood=npc.mood,
            interest=starting_interest,
            patience=patience,
            active_pamphlet_tags=pamphlet_tags or [],
            preacher_personality_bonus=personality_bonus,
        )


class ConversationEngine:
    """Handles conversation logic."""

    def get_openers(self) -> list[dict]:
        """Get available opening lines."""
        return OPENERS

    def get_personality_data(self, personality: str) -> dict:
        """Get data for a personality type."""
        return PERSONALITIES.get(personality, PERSONALITIES["neutral"] if "neutral" in PERSONALITIES else list(PERSONALITIES.values())[0])

    def get_mood_hint(self, mood: str) -> str:
        """Get visual hint for NPC mood."""
        mood_data = MOODS.get(mood, MOODS["neutral"])
        return mood_data.get("visual_hint", "They regard you calmly.")

    def get_opening_response(self, state: ConversationState) -> str:
        """Get NPC's initial response based on personality."""
        personality_data = self.get_personality_data(state.personality)
        responses = personality_data.get("opening_responses", ["Hello."])
        return random.choice(responses)

    def apply_opener(self, state: ConversationState, opener_id: str) -> ConversationResult:
        """Apply player's opening line and get NPC response."""
        opener = next((o for o in OPENERS if o["id"] == opener_id), OPENERS[0])
        state.opener_used = opener_id
        state.turn = 1

        # Calculate interest change based on personality match
        interest_change = opener.get("interest_base", 0)
        interest_change += self._calculate_tag_bonus(state.personality, opener.get("tags", []))
        interest_change += self._calculate_pamphlet_bonus(state)

        state.interest += interest_change

        # Get NPC response
        npc_response = self.get_opening_response(state)

        return ConversationResult(
            npc_response=npc_response,
            interest_change=interest_change,
            new_interest=state.interest,
            is_positive=interest_change > 0,
        )

    def get_available_responses(self, state: ConversationState, objection_id: str) -> list[dict]:
        """Get available responses to an objection."""
        objection = next((o for o in OBJECTIONS if o["id"] == objection_id), None)
        if not objection:
            return RESPONSES[:4]  # Default fallback

        good_response_ids = objection.get("good_responses", [])

        # Get the good responses plus some random others
        responses = []
        for r in RESPONSES:
            if r["id"] in good_response_ids:
                responses.append(r)

        # Add some other responses for variety (including bad options)
        other_responses = [r for r in RESPONSES if r["id"] not in good_response_ids]
        random.shuffle(other_responses)
        responses.extend(other_responses[:max(0, 4 - len(responses))])

        # Shuffle so good answers aren't always first
        random.shuffle(responses)
        return responses[:4]

    def get_next_objection(self, state: ConversationState) -> dict:
        """Get the next objection/response from NPC based on interest and personality."""
        # If interest is high enough, show positive reaction
        if state.interest >= 30:
            positive_objections = [o for o in OBJECTIONS if o.get("is_positive")]
            if positive_objections:
                return random.choice(positive_objections)

        # Weight objections by personality
        personality = state.personality
        available = [o for o in OBJECTIONS if o["id"] not in state.objections_raised and not o.get("is_positive")]

        if not available:
            available = [o for o in OBJECTIONS if not o.get("is_positive")]

        # Weight by personality
        weighted = []
        for obj in available:
            weight = obj.get("personality_weight", {}).get(personality, 1)
            weighted.extend([obj] * weight)

        if weighted:
            chosen = random.choice(weighted)
            state.objections_raised.append(chosen["id"])
            return chosen

        return OBJECTIONS[0]

    def apply_response(self, state: ConversationState, response_id: str, current_objection_id: str) -> ConversationResult:
        """Apply player's response and determine outcome."""
        response = next((r for r in RESPONSES if r["id"] == response_id), RESPONSES[0])
        objection = next((o for o in OBJECTIONS if o["id"] == current_objection_id), None)

        state.turn += 1
        state.patience -= 1

        # Calculate interest change
        base_change = response.get("interest_change", 0)

        # Bonus/penalty for matching personality
        tag_bonus = self._calculate_tag_bonus(state.personality, response.get("tags", []))
        pamphlet_bonus = self._calculate_pamphlet_bonus(state)

        # Extra bonus if this is a "good response" for the objection
        if objection and response_id in objection.get("good_responses", []):
            base_change += 5

        total_change = base_change + tag_bonus + pamphlet_bonus
        state.interest += total_change

        # Determine NPC response text
        is_positive = total_change > 0
        if response.get("ends_conversation"):
            npc_response = "Thank you for understanding."
            return ConversationResult(
                npc_response=npc_response,
                interest_change=total_change,
                new_interest=state.interest,
                is_positive=is_positive,
                conversation_ended=True,
                polite_exit=response.get("polite_exit", False),
            )

        # Check for conversion or rejection
        if state.interest >= CONVERSION_THRESHOLD:
            return ConversationResult(
                npc_response=random.choice(CONVERSION_LINES),
                interest_change=total_change,
                new_interest=state.interest,
                is_positive=True,
                conversation_ended=True,
                converted=True,
            )

        if state.interest <= REJECTION_THRESHOLD:
            return ConversationResult(
                npc_response=random.choice(NEGATIVE_REACTIONS),
                interest_change=total_change,
                new_interest=state.interest,
                is_positive=False,
                conversation_ended=True,
                rejected=True,
            )

        if state.patience <= 0:
            return ConversationResult(
                npc_response="I really need to go now.",
                interest_change=total_change,
                new_interest=state.interest,
                is_positive=is_positive,
                conversation_ended=True,
            )

        # Continue conversation
        if is_positive:
            npc_response = random.choice(POSITIVE_REACTIONS)
        else:
            npc_response = random.choice(NEGATIVE_REACTIONS[:3])  # Less harsh

        return ConversationResult(
            npc_response=npc_response,
            interest_change=total_change,
            new_interest=state.interest,
            is_positive=is_positive,
        )

    def _calculate_tag_bonus(self, personality: str, tags: list[str]) -> int:
        """Calculate interest bonus/penalty based on personality vs tags."""
        personality_data = self.get_personality_data(personality)
        weak_to = personality_data.get("weak_to", [])
        strong_against = personality_data.get("strong_against", [])

        bonus = 0

        for tag in tags:
            if tag in weak_to:
                bonus += INTEREST_PER_GOOD_MATCH // 2
            if tag in strong_against or "all" in strong_against:
                bonus += INTEREST_PER_BAD_MATCH // 2

        return bonus

    def _calculate_pamphlet_bonus(self, state: ConversationState) -> int:
        """Calculate bonus from active pamphlet matching personality."""
        if not state.active_pamphlet_tags:
            return 0

        personality_data = self.get_personality_data(state.personality)
        weak_to = personality_data.get("weak_to", [])

        bonus = 0
        for tag in state.active_pamphlet_tags:
            if tag in weak_to:
                bonus += 3

        return bonus

    def get_interest_description(self, interest: int) -> str:
        """Get a text description of current interest level."""
        if interest >= 40:
            return "very interested"
        elif interest >= 20:
            return "somewhat interested"
        elif interest >= 0:
            return "neutral"
        elif interest >= -15:
            return "skeptical"
        else:
            return "hostile"
