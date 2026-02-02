# Data Model

All game data structures are defined using Python dataclasses for clean, type-safe representations.

---

## Core Enumerations

Defined in `preaching/enums.py`:

```python
class Religion(Enum):
    EVANGELIST = "Evangelist"
    JEHOVAHS_WITNESS = "Jehovah's Witness"
    MORMON = "Mormon"
    CUSTOM = "Custom"
    SATANIC = "Satanic"  # Hidden path

class Strategy(Enum):
    SOFT = "Preach Softly"
    INTENSE = "Preach Intensely"

class Weather(Enum):
    HOT = "hot"
    COLD = "cold"
    NICE = "nice"

class LocationType(Enum):
    HOUSE = "House"
    STORE = "Store"
    CHURCH = "Church"
    LIBRARY = "Library"
```

---

## World Hierarchy

### County

Top-level world container. One per game.

```python
@dataclass
class County:
    name: str                    # "Willow County"
    towns: list[Town]            # 3 towns
```

### Town

Contains neighborhoods.

```python
@dataclass
class Town:
    name: str                    # "Springfield"
    neighborhoods: list[Neighborhood]  # 2-3 neighborhoods
```

### Neighborhood

Contains streets. Tracks church influence.

```python
@dataclass
class Neighborhood:
    name: str                    # "Oak Hills"
    streets: list[Street]        # 2-5 streets
    church_influence: float      # Buff/debuff from churches (-0.10 to +0.15)
```

### Street

Contains locations.

```python
@dataclass
class Street:
    name: str                    # "Main Street"
    locations: list[Location]    # 3-6 locations
```

### Location

A visitable place with NPCs.

```python
@dataclass
class Location:
    location_type: LocationType  # HOUSE, STORE, CHURCH, LIBRARY
    name: str                    # "123 Oak Lane" or "Piggly Wiggly"
    npcs: list[NPC]              # 1-8 NPCs depending on type
    affiliation: Optional[Religion]  # For churches only
    inventory: list              # For stores only
```

**Factory Methods:**
- `Location.create_house(num_npcs)` - House with 1-6 NPCs
- `Location.create_store()` - Store with clerk + inventory
- `Location.create_church(affiliation)` - Church with 3-8 NPCs
- `Location.create_library()` - Library with librarian
- `Location.create_random()` - Random based on weights (70% house, 12% store, 12% church, 6% library)

---

## Characters

### NPC

A person who can be preached to.

```python
@dataclass
class NPC:
    name: str                    # "Maria Garcia"
    personality: str             # "skeptic", "seeker", "lonely", etc.
    mood: str                    # "neutral", "receptive", "grumpy", etc.
    converted: bool              # Has accepted the faith
    failed_attempts: int         # Number of failed conversion attempts
    resistant: bool              # Some NPCs cannot be converted (hidden)
    revealed_resistant: bool     # Library revealed their resistance
```

**Personalities (9 types):**
- `skeptic` - Doubts claims, needs evidence
- `seeker` - Open to spiritual discussion
- `lonely` - Values connection and community
- `busy` - Limited patience, needs quick pitch
- `hostile` - Actively resistant
- `devout_other` - Already has strong faith
- `intellectual` - Values logical arguments
- `cynic` - Distrustful of organized religion
- `neutral` - No strong bias

**Moods (5 types):**
- `neutral` - Starting interest: 0, patience: 4
- `receptive` - Starting interest: +10, patience: 5
- `grumpy` - Starting interest: -10, patience: 3
- `distracted` - Starting interest: -5, patience: 3
- `curious` - Starting interest: +5, patience: 5

---

## Game State

Central mutable state object.

```python
@dataclass
class GameState:
    # Scoring
    score: int                   # Total conversions
    satanic_score: int           # Satanic path conversions
    daily_score: int             # Today's conversions

    # Resources
    hunger: int                  # 0-100, day ends at 100
    money: int                   # Starting $10

    # Player choices
    religion: Religion           # Chosen faith
    strategy: Strategy           # Soft or intense

    # World state
    weather: Weather             # Today's weather
    county: County               # World root
    current_town: Town           # Current location
    current_neighborhood: Neighborhood
    current_street: Street
    chosen_location: Location

    # Time
    day_of_week: int             # 0=Sunday, 6=Saturday

    # Bonuses
    satanic_bonus: float         # From Satanic encounters
    pamphlet_boost_remaining: int  # Turns left with pamphlet bonus
    pamphlet_boost_amount: float
    bible_bonus: float           # Permanent +5% from pocket Bible

    # Systems
    reputation: ReputationManager
    inventory: list[InventoryItem]
    active_pamphlet_tags: list[str]

    # Preacher stats
    preacher_name: str           # "Belen Torres"
    preacher_id: str             # "belen"
    preacher_conversion_bonus: float
    preacher_hunger_rate: float
    preacher_personality_bonus: dict[str, float]
```

**Key Methods:**
- `create_new_game()` - Factory for fresh game with generated world
- `reset_for_new_day()` - Reset hunger and daily score
- `advance_day()` - Move to next day
- `is_sunday()` - Check for Sunday bonus
- `get_total_conversion_bonus()` - Sum all active bonuses
- `use_pamphlet_charge()` - Decrement pamphlet effect

---

## Inventory

### InventoryItem

Items the player carries.

```python
@dataclass
class InventoryItem:
    item_type: str               # "food" or "pamphlet"
    name: str                    # "Candy Bar"
    description: str             # Flavor text
    hunger_restore: int          # For food items
    pamphlet_id: str             # For pamphlets
    pamphlet_tags: list[str]     # Tags for matching personalities
```

---

## Conversation

### ConversationState

Tracks an active conversation.

```python
@dataclass
class ConversationState:
    npc_name: str
    personality: str
    mood: str
    interest: int                # -100 to +100
    patience: int                # Turns remaining
    turn: int                    # Current turn number
    objections_raised: list[str] # Objection IDs already used
    opener_used: Optional[str]
    active_pamphlet_tags: list[str]
    preacher_personality_bonus: dict[str, float]
```

**Thresholds:**
- Interest >= +50 → Conversion
- Interest <= -30 → Rejection
- Patience exhausted → Polite exit

### ConversationResult

Outcome of a player response.

```python
@dataclass
class ConversationResult:
    npc_response: str            # What NPC says
    interest_change: int         # How much interest changed
    new_interest: int            # Current interest level
    is_positive: bool            # Was response well-received
    conversation_ended: bool     # Did conversation end
    converted: bool              # Did NPC convert
    rejected: bool               # Did NPC reject
    polite_exit: bool            # Did NPC leave politely
```

---

## Memory System

### EventType

Types of memorable events.

```python
class EventType(Enum):
    CONVERSION = "conversion"
    REJECTION = "rejection"
    POLITE_EXIT = "polite_exit"
    HOSTILE_CHURCH = "hostile_church"
    FRIENDLY_CHURCH = "friendly_church"
    NO_ANSWER = "no_answer"
    SATANIC_ENCOUNTER = "satanic_encounter"
    HUNGRY_DAY = "hungry_day"
    DONATION_RECEIVED = "donation_received"
    ITEM_PURCHASED = "item_purchased"
    LIBRARY_RESEARCH = "library_research"
    RESISTANT_REVEALED = "resistant_revealed"
    DAY_START = "day_start"
    DAY_END = "day_end"
```

### Memory

A single recorded event.

```python
@dataclass
class Memory:
    day: int
    event_type: EventType
    neighborhood: str
    npc_name: Optional[str]
    npc_personality: Optional[str]
    location_name: Optional[str]
    tags: list[str]              # Searchable tags
    details: dict                # Arbitrary extra data
```

### DaySummary

Aggregated day statistics for journal generation.

```python
@dataclass
class DaySummary:
    day: int
    day_name: str
    weather: str
    conversions: int
    rejections: int
    polite_exits: int
    doors_unanswered: int
    money_earned: int
    money_spent: int
    hostile_churches: int
    friendly_churches: int
    neighborhoods_visited: list[str]
    notable_npcs: list[str]
    satanic_events: int
    ended_hungry: bool
    tags: list[str]              # Day mood tags
```

---

## Reputation

### ReputationManager

Tracks per-neighborhood reputation.

```python
class ReputationManager:
    reputation: dict[str, int]   # neighborhood_name → -50 to +50
```

**Events and effects:**
| Event | Change |
|-------|--------|
| Conversion | +2 |
| Polite exit | 0 |
| Rejection | -1 |
| Aggressive failure | -3 |
| Hostile church | -2 |

**Reputation effects on NPCs:**
- High reputation: NPCs more receptive (bonus starting interest)
- Low reputation: NPCs less likely to open door, start hostile

---

*See also: [Architecture Overview](overview.md) | [Conversation System](../systems/conversation.md)*
