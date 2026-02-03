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
    Preacher(
        id="maria",
        name="Sister Maria Guadalupe",
        description="A gentle nun who sees the divine in everyone",
        conversion_bonus=0.0,
        reputation_bonus=10,  # People trust nuns
        money_bonus=-5,  # Vow of poverty
        hunger_rate=0.9,  # Used to fasting
        personality_bonus={"grieving": 0.25, "lonely": 0.15, "hostile": -0.10},
        special="Exceptional with those in pain, but struggles with open hostility",
    ),
    Preacher(
        id="derek",
        name="Pastor Derek Thompson",
        description="A former addict turned youth pastor with street smarts",
        conversion_bonus=0.05,
        reputation_bonus=-5,  # Rough past
        money_bonus=0,
        hunger_rate=1.0,
        personality_bonus={"cynic": 0.20, "hostile": 0.10, "intellectual": -0.15},
        special="Connects with cynics and the hardened, but scholars see through him",
    ),
    Preacher(
        id="grandma_ruth",
        name="Grandma Ruth",
        description="An 85-year-old who's seen it all and won't take no for an answer",
        conversion_bonus=0.08,
        reputation_bonus=15,  # Who can say no to grandma?
        money_bonus=25,  # Social Security
        hunger_rate=1.3,  # Gets tired easily
        personality_bonus={"parent": 0.20, "elderly_religious": 0.15, "busy": -0.10},
        special="Older folks and parents love her, but busy people find her slow",
    ),
    Preacher(
        id="carl",
        name="Brother Carl",
        description="A soft-spoken introvert who preaches through kindness, not words",
        conversion_bonus=-0.05,  # Quiet approach has lower base rate
        reputation_bonus=5,
        money_bonus=10,
        hunger_rate=0.85,
        personality_bonus={"intellectual": 0.15, "seeker": 0.10, "hostile": 0.15},  # Non-threatening
        special="Disarms hostile people with gentleness, but quiet approach takes longer",
    ),
]


# =============================================================================
# PREACHER INSIGHTS - Internal voice observations during conversations
# Based on Disco Elysium's "skills as voices" pattern
# =============================================================================
PREACHER_INSIGHTS: dict[str, dict[str, dict[str, list[str]]]] = {
    "belen": {
        "positive": {
            "lonely": [
                "Their eyes have that emptiness. You know it well.",
                "This one needs community more than doctrine.",
                "You see yourself in them, before you found your path.",
            ],
            "seeker": [
                "A searching soul. Your testimony was made for moments like this.",
                "They're hungry for something real. Give them the truth.",
                "This is why you do this. They're ready to hear it.",
            ],
        },
        "negative": {
            "skeptic": [
                "They want proof. You have faith, not footnotes.",
                "This one argues with their head, not their heart.",
                "Be patient. Your story sounds crazy even to you sometimes.",
            ],
        },
    },
    "scott": {
        "positive": {
            "intellectual": [
                "Ah, a thinker. Finally, a real conversation.",
                "They've read the counterarguments. Good. So have you.",
                "Engage the mind first. The heart follows.",
            ],
            "skeptic": [
                "Their doubt is structured. You can work with that.",
                "Skepticism is just faith that hasn't found its foundation yet.",
                "They need reasons, not feelings. Give them reasons.",
            ],
        },
        "negative": {},
    },
    "joyce": {
        "positive": {
            "cynic": [
                "They've been burned before. Show them you're different.",
                "Cynicism is just hope wearing armor.",
                "Break through the wall. There's someone hurting behind it.",
            ],
            "hostile": [
                "Their anger comes from somewhere. Find the wound.",
                "Don't match their energy. Transform it.",
            ],
        },
        "negative": {},
    },
    "billy": {
        "positive": {
            "seeker": [
                "They came to the door hoping for something. Give it to them.",
                "The harvest is ready. You just need to gather it.",
                "Your father would have known exactly what to say here.",
            ],
        },
        "negative": {},
    },
    "joel": {
        "positive": {
            "lonely": [
                "They need to feel special. You can give them that.",
                "Promise them the life they deserve. God wants them blessed.",
                "Loneliness is just untapped potential waiting for purpose.",
            ],
        },
        "negative": {},
    },
    "marcus": {
        "positive": {
            "hostile": [
                "You've faced worse on the streets. Stand your ground.",
                "Their fire reminds you of yourself. Channel it.",
                "Don't back down. They'll respect you for it.",
            ],
        },
        "negative": {
            "skeptic": [
                "They want debate. You have testimony, not talking points.",
                "Sometimes the streets taught you more than any book.",
                "Logic won't reach this one. Move on.",
            ],
        },
    },
    "olga": {
        "positive": {
            "lonely": [
                "Oh, pobrecito. They just need someone to listen.",
                "You know exactly what they need to hear, mi amor.",
                "A little kindness goes a long way with this one.",
            ],
            "cynic": [
                "They think they're so clever. Bless their heart.",
                "Let them think they're winning. Then close the deal.",
                "Cynics are just disappointed optimists, cariño.",
            ],
            "skeptic": [
                "Even doubters have their price. Find it.",
            ],
        },
        "negative": {},
    },
    "maria": {
        "positive": {
            "grieving": [
                "The Lord weeps with them. So will you.",
                "Don't preach. Just be present.",
                "They don't need words. They need witness.",
            ],
            "lonely": [
                "Every soul deserves to feel seen.",
                "Christ was lonely too. Share that with them.",
            ],
        },
        "negative": {
            "hostile": [
                "Turn the other cheek, but... this one tests you.",
                "Their anger frightens you. Pray for courage.",
                "Perhaps this door is not yours to open.",
            ],
        },
    },
    "derek": {
        "positive": {
            "cynic": [
                "Takes one to know one. You were harder than this.",
                "They think they're tough. Show them real survival.",
                "Cut through the act. Ask what really happened.",
            ],
            "hostile": [
                "You've stared down worse in the mirror.",
                "Their bark is worse than their bite. Probably.",
            ],
        },
        "negative": {
            "intellectual": [
                "They're using big words to feel superior. Don't play.",
                "Book smarts ain't street smarts.",
                "You'll never out-argue them. Don't try.",
            ],
        },
    },
    "grandma_ruth": {
        "positive": {
            "parent": [
                "Oh, the poor dear looks exhausted. You remember those days.",
                "Children are a blessing. Remind them of that.",
                "They need a moment of peace. Give it to them.",
            ],
            "elderly_religious": [
                "Another old soul! You'll get along just fine.",
                "Respect their journey. They've walked longer than most.",
                "Share stories. That's how our generation connects.",
            ],
        },
        "negative": {
            "busy": [
                "Everyone's so rushed these days. No time for what matters.",
                "They'll regret not stopping. But you can't force them.",
            ],
        },
    },
    "carl": {
        "positive": {
            "intellectual": [
                "Listen more than you speak. They'll appreciate that.",
                "Sometimes silence says more than sermons.",
                "Ask questions. Let them find their own answers.",
            ],
            "seeker": [
                "They're almost there. A gentle nudge is enough.",
                "Don't overwhelm them. Just open the door a crack.",
            ],
            "hostile": [
                "Softness disarms better than force.",
                "They expect a fight. Surprise them with peace.",
                "Your quiet is your strength here.",
            ],
        },
        "negative": {},
    },
    "custom": {
        "positive": {},
        "negative": {},
    },
}


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
