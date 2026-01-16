"""Preacher/Character definitions with bonuses and penalties."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState


@dataclass
class Preacher:
    """A playable preacher character."""
    id: str
    name: str
    description: str
    # Bonuses/penalties
    conversion_bonus: float = 0.0  # % bonus to conversion rate
    reputation_bonus: int = 0  # Starting reputation modifier
    money_bonus: int = 0  # Extra starting money
    hunger_rate: float = 1.0  # Multiplier for hunger gain (lower = better)
    # Personality affinities - bonus with certain NPC types
    personality_bonus: dict[str, float] = field(default_factory=dict)
    # Special abilities
    special: str = ""

    def apply_to_state(self, state: "GameState") -> None:
        """Apply this preacher's bonuses to the game state."""
        state.money += self.money_bonus
        state.preacher_conversion_bonus = self.conversion_bonus
        state.preacher_hunger_rate = self.hunger_rate
        state.preacher_personality_bonus = self.personality_bonus.copy()


# Preset preachers
PREACHERS: list[Preacher] = [
    Preacher(
        id="belen",
        name="Belen Torres",
        description="An old Dominican woman, former witch turned evangelist with stories to tell",
        conversion_bonus=0.05,  # +5% conversion
        reputation_bonus=-5,  # Some people have heard rumors...
        money_bonus=15,  # Makes money from her online ministry
        hunger_rate=1.1,  # Old bones tire faster
        personality_bonus={"lonely": 0.15, "seeker": 0.20, "skeptic": -0.10},  # Great with seekers, skeptics don't buy it
        special="Ex-witch who survived Haitian Vudu and demon encounters. Her testimony is wild.",
    ),
    Preacher(
        id="scott",
        name="Dr. Scott Johnson",
        description="A scholarly theologian with logical arguments",
        conversion_bonus=0.0,
        reputation_bonus=5,  # Starts with better reputation
        money_bonus=20,  # More starting money
        hunger_rate=1.2,  # Gets hungry faster (older, less stamina)
        personality_bonus={"intellectual": 0.15, "skeptic": 0.10},  # Good with thinkers
        special="Persuasive with intellectuals and skeptics, but tires easily",
    ),
    Preacher(
        id="joyce",
        name="Sister Joyce Meyer",
        description="An energetic motivational preacher",
        conversion_bonus=0.0,
        reputation_bonus=0,
        money_bonus=10,
        hunger_rate=0.9,  # More energy, less hunger
        personality_bonus={"cynic": 0.15, "hostile": 0.05},  # Can reach cynics
        special="High energy and can break through to cynics",
    ),
    Preacher(
        id="billy",
        name="Pastor Billy Graham Jr.",
        description="A charismatic crusade-style preacher",
        conversion_bonus=0.10,  # Strong conversion bonus
        reputation_bonus=10,  # Well known, good reputation
        money_bonus=0,
        hunger_rate=1.1,
        personality_bonus={"seeker": 0.15},
        special="Famous name opens doors, great with seekers",
    ),
    Preacher(
        id="joel",
        name="Reverend Joel Prosperity",
        description="A prosperity gospel preacher with a winning smile",
        conversion_bonus=-0.05,  # Lower conversion (people skeptical)
        reputation_bonus=-5,  # Some distrust
        money_bonus=50,  # Lots of starting money
        hunger_rate=0.8,  # Eats well, less hunger issues
        personality_bonus={"lonely": 0.10},
        special="Wealthy but people are wary of his motives",
    ),
    Preacher(
        id="marcus",
        name="Brother Marcus",
        description="A humble street preacher with fire in his heart",
        conversion_bonus=0.0,
        reputation_bonus=-10,  # Seen as aggressive
        money_bonus=-10,  # Starts poor
        hunger_rate=0.85,  # Used to hardship
        personality_bonus={"hostile": 0.15, "skeptic": -0.10},  # Can handle hostile, bad with skeptics
        special="Fearless with hostile crowds but too intense for skeptics",
    ),
    Preacher(
        id="olga",
        name="Titi Olga",
        description="A wonderfully warm community mother with a heart full of love for everyone",
        conversion_bonus=0.08,  # She's "persuasive"
        reputation_bonus=5,  # People think she's sweet
        money_bonus=30,  # She's good at "fundraising"
        hunger_rate=0.75,  # She always makes sure to take care of herself first
        personality_bonus={"lonely": 0.20, "cynic": 0.15, "skeptic": 0.05},  # Knows exactly what people need to hear
        special="Such a blessing to everyone she meets. Truly. Everyone says so.",
    ),
]


def get_preacher_by_id(preacher_id: str) -> Preacher | None:
    """Get a preacher by ID."""
    return next((p for p in PREACHERS if p.id == preacher_id), None)


def create_custom_preacher(name: str) -> Preacher:
    """Create a custom preacher with balanced stats."""
    return Preacher(
        id="custom",
        name=name,
        description="A dedicated servant of the faith",
        conversion_bonus=0.0,
        reputation_bonus=0,
        money_bonus=0,
        hunger_rate=1.0,
        personality_bonus={},
        special="A blank slate - no bonuses or penalties",
    )
