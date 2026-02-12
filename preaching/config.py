"""Game configuration and constants."""
from .enums import Religion

# Hunger system
MAX_HUNGER = 100
HUNGER_HARSH_WEATHER = 15
HUNGER_NICE_WEATHER = 10
FOOD_HUNGER_REDUCTION = 20

# Conversion mechanics
FAILED_ATTEMPT_PENALTY = 0.1
MAX_CONVERSION_RATE = 0.95
RESISTANT_CONVERSION_MULTIPLIER = 0.15  # Resistant NPCs are very hard but not impossible

# Event probabilities
FOOD_DONATION_CHANCE = 0.2
SATANIC_BIBLE_CHANCE = 0.1
FOOD_OR_BIBLE_SPLIT = 0.5

# Satanic bonus per ally met
SATANIC_ALLY_BONUS = 0.15

# Base conversion rates for each religion
# Some paths are easier to walk than others...
CONVERSION_RATES: dict[Religion, float] = {
    Religion.EVANGELIST: 0.3,
    Religion.JEHOVAHS_WITNESS: 0.2,
    Religion.MORMON: 0.25,
    Religion.CUSTOM: 0.15,
    Religion.SATANIC: 0.5,  # For the curious
}

# Religions shown to the player (Satanic is hidden)
AVAILABLE_RELIGIONS: list[Religion] = [
    Religion.EVANGELIST,
    Religion.JEHOVAHS_WITNESS,
    Religion.MORMON,
    Religion.CUSTOM,
]

# Days of the week
DAYS: list[str] = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

# Game duration
GAME_DAYS = 7
SATANIC_VICTORY_THRESHOLD = 10  # A different kind of victory awaits the persistent

# Economy
STARTING_MONEY = 10
MONEY_DONATION_CHANCE = 0.3
MONEY_DONATION_MIN = 1
MONEY_DONATION_MAX = 5
SUNDAY_OFFERING_BONUS = 10

# Church influence
FRIENDLY_CHURCH_BUFF = 0.15
HOSTILE_CHURCH_DEBUFF = -0.10
CHURCH_CHASE_HUNGER_COST = 10

# Demon ally mechanics
DEMON_BETRAYAL_RATES: dict[str, float] = {
    "temptation": 0.08,
    "deception": 0.12,
    "oppression": 0.05,
    "possession": 0.15,
}
DEMON_CAPTURE_CORRUPTION = 3
DEMON_CAPTURE_ALIGNMENT_PENALTY = -10.0
DEMON_BANISH_ALIGNMENT_BONUS = 5.0
DEMON_ALLY_SATANIC_BIBLE_SCALE = 0.05
DEMON_ALLY_ENCOUNTER_SCALE = 0.05
MAX_SATANIC_BIBLE_CHANCE = 0.35
MAX_DEMON_ENCOUNTER_CHANCE = 0.40

# Library costs
LIBRARY_RESEARCH_HUNGER = 5

# Location generation weights (out of 100)
LOCATION_WEIGHTS = {
    "HOUSE": 55,
    "STORE": 10,
    "CHURCH": 10,
    "LIBRARY": 5,
    "PARK": 7,
    "DINER": 5,
    "LAUNDROMAT": 4,
    "COMMUNITY_CENTER": 4,
}

# Park mechanics
PARK_WALK_AWAY_CHANCE = 0.25  # NPCs can walk away mid-conversation
PARK_EXTRA_PATIENCE = 1       # People expect preachers at parks

# Diner mechanics
COFFEE_COST = 2               # Buy someone coffee for conversion bonus
COFFEE_INTEREST_BONUS = 10    # Interest bonus from buying coffee
DINER_KICK_OUT_THRESHOLD = -15  # Get kicked out if interest drops this low

# Community center mechanics
COMMUNITY_CENTER_AFFILIATION_CHECK = True  # Must match affiliation or get asked to leave
