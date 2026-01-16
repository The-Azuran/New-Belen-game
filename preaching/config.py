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

# Event probabilities
FOOD_DONATION_CHANCE = 0.2
SATANIC_BIBLE_CHANCE = 0.1
FOOD_OR_BIBLE_SPLIT = 0.5

# Satanic bonus per ally met
SATANIC_ALLY_BONUS = 0.15

# Base conversion rates for each religion
CONVERSION_RATES: dict[Religion, float] = {
    Religion.EVANGELIST: 0.3,
    Religion.JEHOVAHS_WITNESS: 0.2,
    Religion.MORMON: 0.25,
    Religion.CUSTOM: 0.15,
    Religion.SATANIC: 0.5,
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
SATANIC_VICTORY_THRESHOLD = 10

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

# Library costs
LIBRARY_RESEARCH_HUNGER = 5

# Location generation weights (out of 100)
LOCATION_WEIGHTS = {
    "HOUSE": 70,
    "STORE": 12,
    "CHURCH": 12,
    "LIBRARY": 6,
}
