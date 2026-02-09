"""Enumerations for the game."""
from enum import Enum


class Weather(Enum):
    HOT = "hot"
    COLD = "cold"
    NICE = "nice"

    def is_harsh(self) -> bool:
        return self in (Weather.HOT, Weather.COLD)


class Strategy(Enum):
    SOFT = "Preach Softly"
    INTENSE = "Preach Intensely"


class Religion(Enum):
    EVANGELIST = "Evangelist"
    JEHOVAHS_WITNESS = "Jehovah's Witness"
    MORMON = "Mormon"
    CUSTOM = "Custom"
    SATANIC = "Satanic"


class LocationType(Enum):
    HOUSE = "House"
    STORE = "Store"
    CHURCH = "Church"
    LIBRARY = "Library"


class CombatType(Enum):
    """Type of combat encounter."""
    SPIRITUAL = "spiritual"  # 75% of encounters
    PHYSICAL = "physical"    # 25% of encounters (high aggression demons only)
    BOSS = "boss"           # Special boss fights


class DemonType(Enum):
    """Types of demons based on their spiritual nature."""
    TEMPTATION = "temptation"    # Weak to faith, strong against doubt
    DECEPTION = "deception"      # Weak to truth, strong against confusion
    OPPRESSION = "oppression"    # Weak to hope, strong against despair
    POSSESSION = "possession"    # Boss demon, appears in Satanic churches or endgame


class CombatActionType(Enum):
    """Types of combat actions available to the player."""
    # Spiritual actions (faith-based)
    PRAYER = "prayer"        # Restores faith, damages demons
    SCRIPTURE = "scripture"  # Stronger faith attack
    REBUKE = "rebuke"        # Powerful faith attack, high cost
    # Physical actions (for physical confrontations)
    DODGE = "dodge"          # Avoid physical attack
    PUSH = "push"            # Push demon back
    RESTRAIN = "restrain"    # Attempt to restrain demon
    # Item actions
    USE_HOLY_WATER = "use_holy_water"    # Use holy water item
    USE_CROSS = "use_cross"              # Use silver cross item
    USE_OIL = "use_oil"                  # Use anointing oil item
