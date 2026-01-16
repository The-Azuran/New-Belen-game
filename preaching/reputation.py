"""
Reputation system - tracks how neighborhoods view the player.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState

# Reputation thresholds
REPUTATION_HOSTILE = -20      # Below this, some NPCs won't open door
REPUTATION_SKEPTICAL = -10    # NPCs start grumpy
REPUTATION_NEUTRAL = 0        # Default starting point
REPUTATION_FRIENDLY = 15      # NPCs start receptive
REPUTATION_BELOVED = 30       # NPCs very receptive, bonus effects

# Reputation changes
REP_CONVERSION = 2            # Successful conversion
REP_POLITE_EXIT = 0           # Left politely without converting
REP_REJECTION = -1            # Got rejected (patience ran out)
REP_AGGRESSIVE_FAIL = -3      # Used aggressive tactics and failed
REP_HOSTILE_CHURCH = -2       # Got chased out of hostile church


@dataclass
class ReputationManager:
    """Manages reputation across neighborhoods."""
    reputation: dict[str, int] = field(default_factory=dict)

    def get_reputation(self, neighborhood_name: str) -> int:
        """Get reputation in a neighborhood."""
        return self.reputation.get(neighborhood_name, REPUTATION_NEUTRAL)

    def modify_reputation(self, neighborhood_name: str, change: int) -> int:
        """Modify reputation and return new value."""
        current = self.get_reputation(neighborhood_name)
        new_value = max(-50, min(50, current + change))  # Clamp to -50 to 50
        self.reputation[neighborhood_name] = new_value
        return new_value

    def on_conversion(self, neighborhood_name: str) -> int:
        """Call when player successfully converts someone."""
        return self.modify_reputation(neighborhood_name, REP_CONVERSION)

    def on_polite_exit(self, neighborhood_name: str) -> int:
        """Call when player exits conversation politely."""
        return self.modify_reputation(neighborhood_name, REP_POLITE_EXIT)

    def on_rejection(self, neighborhood_name: str) -> int:
        """Call when NPC rejects player (patience ran out)."""
        return self.modify_reputation(neighborhood_name, REP_REJECTION)

    def on_aggressive_failure(self, neighborhood_name: str) -> int:
        """Call when player used aggressive tactics and failed."""
        return self.modify_reputation(neighborhood_name, REP_AGGRESSIVE_FAIL)

    def on_hostile_church(self, neighborhood_name: str) -> int:
        """Call when player gets chased out of hostile church."""
        return self.modify_reputation(neighborhood_name, REP_HOSTILE_CHURCH)

    def get_starting_mood(self, neighborhood_name: str) -> str:
        """Get NPC starting mood based on reputation."""
        rep = self.get_reputation(neighborhood_name)

        if rep >= REPUTATION_BELOVED:
            return "receptive"
        elif rep >= REPUTATION_FRIENDLY:
            # 70% receptive, 30% neutral
            import random
            return random.choice(["receptive", "receptive", "neutral", "curious"])
        elif rep >= REPUTATION_NEUTRAL:
            # Standard distribution
            import random
            return random.choice(["neutral", "neutral", "receptive", "grumpy", "curious"])
        elif rep >= REPUTATION_SKEPTICAL:
            # Leaning negative
            import random
            return random.choice(["neutral", "grumpy", "grumpy", "distracted"])
        else:
            # Hostile territory
            import random
            return random.choice(["grumpy", "grumpy", "distracted"])

    def will_open_door(self, neighborhood_name: str) -> bool:
        """Check if NPC will even open the door based on reputation."""
        rep = self.get_reputation(neighborhood_name)

        if rep >= REPUTATION_NEUTRAL:
            return True
        elif rep >= REPUTATION_HOSTILE:
            # 80% chance they'll open
            import random
            return random.random() < 0.8
        else:
            # Very hostile - 50% chance
            import random
            return random.random() < 0.5

    def get_reputation_bonus(self, neighborhood_name: str) -> int:
        """Get interest bonus/penalty based on reputation."""
        rep = self.get_reputation(neighborhood_name)

        if rep >= REPUTATION_BELOVED:
            return 10
        elif rep >= REPUTATION_FRIENDLY:
            return 5
        elif rep >= REPUTATION_NEUTRAL:
            return 0
        elif rep >= REPUTATION_SKEPTICAL:
            return -5
        else:
            return -10

    def get_reputation_description(self, neighborhood_name: str) -> str:
        """Get text description of reputation level."""
        rep = self.get_reputation(neighborhood_name)

        if rep >= REPUTATION_BELOVED:
            return "beloved"
        elif rep >= REPUTATION_FRIENDLY:
            return "well-liked"
        elif rep >= REPUTATION_NEUTRAL:
            return "unknown"
        elif rep >= REPUTATION_SKEPTICAL:
            return "viewed with suspicion"
        else:
            return "unwelcome"
