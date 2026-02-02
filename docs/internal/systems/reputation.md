# System: Reputation

**Status:** Complete
**Location:** `preaching/reputation.py`

---

## Overview

The reputation system tracks how each neighborhood views the player. Reputation affects NPC moods, whether doors open, and starting interest levels.

## Mechanics

### Reputation Range

-50 (hated) to +50 (beloved)

### Thresholds

| Level | Reputation | Effect |
|-------|------------|--------|
| Beloved | +30 and above | NPCs very receptive, +10 starting interest |
| Well-liked | +15 to +29 | 70% receptive mood, +5 starting interest |
| Unknown | 0 to +14 | Standard distribution |
| Suspicious | -10 to -1 | Leaning negative, -5 starting interest |
| Hostile | -20 to -11 | 80% will open door, -10 starting interest |
| Hated | Below -20 | 50% will open door, -10 starting interest |

### Reputation Changes

| Event | Change |
|-------|--------|
| Successful conversion | +2 |
| Polite exit | 0 |
| Rejection (patience ran out) | -1 |
| Aggressive tactics failure | -3 |
| Chased from hostile church | -2 |

---

## Key Methods

### ReputationManager

```python
class ReputationManager:
    # Get current reputation
    get_reputation(neighborhood_name) -> int

    # Modify reputation (clamped to -50 to +50)
    modify_reputation(neighborhood_name, change) -> int

    # Event handlers
    on_conversion(neighborhood_name) -> int      # +2
    on_polite_exit(neighborhood_name) -> int     # 0
    on_rejection(neighborhood_name) -> int       # -1
    on_aggressive_failure(neighborhood_name) -> int  # -3
    on_hostile_church(neighborhood_name) -> int  # -2

    # NPC behavior modifiers
    get_starting_mood(neighborhood_name) -> str
    will_open_door(neighborhood_name) -> bool
    get_reputation_bonus(neighborhood_name) -> int
    get_reputation_description(neighborhood_name) -> str
```

---

## Integration Points

### Conversation Start

When starting a conversation, reputation affects:
1. Whether NPC opens door at all (`will_open_door`)
2. NPC's starting mood (`get_starting_mood`)
3. Starting interest bonus/penalty (`get_reputation_bonus`)

### After Conversation

The game calls the appropriate handler:
- `on_conversion()` after successful conversion
- `on_rejection()` after NPC patience runs out
- `on_polite_exit()` after player leaves voluntarily

### Church Visits

- Hostile church chases player out → `on_hostile_church()`

---

## Strategic Considerations

- Early negative reputation spirals are punishing (doors don't open)
- Building positive reputation in one neighborhood creates a "safe zone"
- Aggressive tactics risk -3 reputation on failure vs -1 for passive failure
- Players may want to abandon low-reputation neighborhoods

---

*See also: [Conversation System](conversation.md) | [Data Model](../architecture/data-model.md)*
