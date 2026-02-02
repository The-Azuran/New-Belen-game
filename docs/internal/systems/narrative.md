# System: Narrative & Memory

**Status:** Complete
**Location:** `preaching/narrative.py`, `preaching/memory.py`

---

## Overview

The narrative system creates emergent storytelling by:
1. Recording game events as memories
2. Generating contextual internal monologue
3. Creating personalized journal entries

This transforms mechanical gameplay into a personal story.

---

## Memory System

### Purpose

Tracks all significant game events for later narrative generation.

### Event Types

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

### Memory Structure

```python
@dataclass
class Memory:
    day: int
    event_type: EventType
    neighborhood: str
    npc_name: Optional[str]
    npc_personality: Optional[str]
    location_name: Optional[str]
    tags: list[str]          # Searchable tags
    details: dict            # Arbitrary extra data
```

### MemoryManager

```python
class MemoryManager:
    # Recording
    add_memory(memory)
    record_event(day, event_type, neighborhood, **kwargs)

    # Querying
    get_npc_history(npc_name) -> list[Memory]
    get_events_matching(**criteria) -> list[Memory]
    get_today_memories(day) -> list[Memory]

    # Day tracking
    start_day(day, day_name, weather)
    end_day()
    get_day_summary(day) -> DaySummary
```

### DaySummary

Aggregated statistics for journal generation:

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
    tags: list[str]          # Day mood tags
```

---

## Narrative Engine

### Purpose

Generates contextual text based on current state and memories.

### NarrativeContext

Input for narrative generation:

```python
@dataclass
class NarrativeContext:
    day: int
    weather: str
    hunger: int
    money: int
    total_score: int
    satanic_score: int
    current_neighborhood: str
    rejection_streak: int
    conversion_streak: int
    reputation_in_area: int
```

### Generation Methods

#### Internal Monologue

`get_approach_thought(context, npc)` - Player's thoughts when approaching NPC.

Considers:
- Previous encounters with this NPC
- Current rejection/conversion streak
- Hunger level
- Weather
- Neighborhood reputation
- NPC personality

**Example outputs:**
- "You've spoken to Maria before. It didn't go well."
- "Three in a row. Is anyone listening today?"
- "Your stomach aches. Focus."
- "You sense you're not welcome here anymore."

#### Post-Conversation Reflection

`get_conversion_reflection(context, npc)` - After successful conversion.
`get_rejection_reflection(context, npc)` - After rejection.
`get_polite_exit_reflection(context, npc)` - After polite exit.

#### Journal Entries

`generate_day_journal(day_summary)` - End-of-day journal entry.

Combines:
- Weather description
- Key events (conversions, rejections)
- Notable NPCs encountered
- Emotional state based on performance
- Foreshadowing based on patterns

---

## Context-Aware Text Pools

The narrative engine selects from text pools based on context.

### Hunger-Based Thoughts

| Hunger Level | Example |
|--------------|---------|
| 70+ | "Your stomach aches. Focus." |
| 50-69 | "The hunger gnaws at you, but you push on." |
| Below 50 | (no hunger thoughts) |

### Weather-Based Thoughts

| Weather | Example |
|---------|---------|
| Hot | "Sweat trickles down your back." |
| Cold | "You pull your coat tighter." |
| Nice | (no weather thoughts) |

### Streak-Based Thoughts

| Streak | Example |
|--------|---------|
| 3+ rejections | "Another door. Another chance for rejection." |
| 3+ conversions | "The Spirit is with you today." |

### Reputation-Based Thoughts

| Reputation | Example |
|------------|---------|
| Below -10 | "You sense you're not welcome here anymore." |
| Above +15 | "People here know you now. That helps." |

### Personality-Specific Observations

| Personality | Example |
|-------------|---------|
| hostile | "Something in their posture warns you this won't be easy." |
| seeker | "They seem... searching for something." |
| lonely | "Something in their eyes speaks of isolation." |

---

## Integration Points

### During Gameplay

1. Game loop creates `NarrativeContext` from current state
2. Before conversation: `get_approach_thought()` for internal monologue
3. After conversation: `get_*_reflection()` methods
4. Memory recorded via `MemoryManager.record_event()`

### End of Day

1. `MemoryManager.end_day()` finalizes day summary
2. `NarrativeEngine.generate_day_journal()` creates journal entry
3. Player sees personalized day recap

### End of Game

1. All day summaries aggregated
2. Final journal generation
3. Story arc revealed through accumulated memories

---

## Design Philosophy

**Emergent over scripted**: The narrative is not pre-written. It emerges from:
- Mechanical game state (hunger, money, score)
- Player choices (which neighborhoods, which responses)
- Random events (who they meet, what happens)

**Personal over generic**: By tracking specific NPC names, locations, and events, the narrative feels like *this* player's story, not a generic one.

**Subtle over explicit**: Thoughts are brief observations, not lengthy exposition. The player fills in emotional weight.

---

*See also: [Data Model](../architecture/data-model.md) | [Conversation System](conversation.md)*
