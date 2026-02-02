# System: Conversation Engine

**Status:** Complete
**Location:** `preaching/conversation.py`, `preaching/dialogue.py`

---

## Overview

The conversation system handles multi-turn dialogue between the player and NPCs. Each conversation tracks "interest" which determines whether the NPC converts, rejects, or politely exits.

## Core Flow

```
1. Start conversation with NPC
2. Player selects opening line
3. Loop:
   a. NPC raises objection
   b. Player selects response
   c. Interest adjusts based on tag matching
   d. Check for conversion/rejection thresholds
4. End: Conversion, Rejection, or Polite Exit
```

## Key Classes

### ConversationState

Tracks the state of an active conversation.

| Field | Type | Description |
|-------|------|-------------|
| `npc_name` | str | NPC's name |
| `personality` | str | NPC personality type |
| `mood` | str | Current mood |
| `interest` | int | -100 to +100, conversion threshold at +50 |
| `patience` | int | Turns remaining before NPC leaves |
| `turn` | int | Current turn number |
| `objections_raised` | list[str] | Objection IDs already used (no repeats) |
| `active_pamphlet_tags` | list[str] | Tags from equipped pamphlet |

### ConversationEngine

Handles conversation logic:

- `get_openers()` - Get available opening lines
- `apply_opener(state, opener_id)` - Apply player's opening
- `get_next_objection(state)` - Get NPC's next challenge
- `get_available_responses(state)` - Get player response options
- `apply_response(state, response_id)` - Resolve player's response
- `check_conversion(state)` - Check if thresholds reached

### ConversationResult

Returned after player actions:

| Field | Type | Description |
|-------|------|-------------|
| `npc_response` | str | What the NPC says |
| `interest_change` | int | How much interest changed |
| `new_interest` | int | Current interest level |
| `is_positive` | bool | Was response well-received |
| `conversation_ended` | bool | Did conversation end |
| `converted` | bool | Did NPC convert |
| `rejected` | bool | Did NPC reject |
| `polite_exit` | bool | Did NPC leave politely |

---

## Tag Matching System

Responses have **tags** that match against personality **weak_to** and **strong_against** lists.

### Example: Skeptic Personality

```python
"skeptic": {
    "weak_to": ["logical", "evidence", "respectful"],
    "strong_against": ["hellfire", "pushy", "emotional"],
}
```

If a response has:
- `logical` tag → **bonus interest** (+10 per match)
- `hellfire` tag → **penalty interest** (-10 per match)

### Interest Calculation

```
base_change = response["interest_base"]
for tag in response.tags:
    if tag in personality.weak_to:
        base_change += INTEREST_PER_GOOD_MATCH  # +10
    if tag in personality.strong_against:
        base_change += INTEREST_PER_BAD_MATCH   # -10
```

### Pamphlet Integration

When a pamphlet is equipped, its tags are added to the matching pool:
- Family Values pamphlet adds `["family", "community", "traditional"]`
- These provide bonus interest when matched to NPC weaknesses

---

## Thresholds

| Threshold | Value | Outcome |
|-----------|-------|---------|
| Conversion | +50 | NPC accepts faith |
| Rejection | -30 | NPC shuts door |
| Patience = 0 | - | Polite exit |

---

## Personality Reference

| Personality | Weak To | Strong Against |
|-------------|---------|----------------|
| `skeptic` | logical, evidence, respectful | hellfire, pushy, emotional |
| `seeker` | spiritual, personal, community | (none) |
| `lonely` | community, family, friendly, personal | logical, cold |
| `busy` | quick, respectful | long_winded, pushy |
| `hostile` | respectful, humble | pushy, hellfire, direct |
| `devout_other` | respectful, common_ground | pushy, hellfire, exclusive |
| `intellectual` | logical, evidence, debate | simple, emotional |
| `cynic` | personal, humble, authentic | institutional, pushy |

---

## Mood Effects

| Mood | Interest Bonus | Patience |
|------|----------------|----------|
| `receptive` | +15 | 5 |
| `curious` | +10 | 4 |
| `neutral` | 0 | 4 |
| `distracted` | -5 | 3 |
| `grumpy` | -10 | 3 |

---

## Data Files

All dialogue content is in `dialogue.py`:
- `PERSONALITIES` - Personality definitions with weakness tags
- `MOODS` - Mood definitions with bonuses
- `OPENERS` - Player opening lines
- `OBJECTIONS` - NPC challenges
- `RESPONSES` - Player response options
- `POSITIVE_REACTIONS` - NPC responses to good choices
- `NEGATIVE_REACTIONS` - NPC responses to bad choices
- `CONVERSION_LINES` - Success messages

---

*See also: [Data Model](../architecture/data-model.md) | [Reputation System](reputation.md)*
