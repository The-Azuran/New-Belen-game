# System: Random Events

**Status:** Complete
**Location:** `preaching/events.py`

---

## Overview

The event system triggers random encounters during gameplay, including the hidden Satanic path mechanic.

## Event Types

### Success Events

Triggered after successful conversions.

| Event | Probability | Effect |
|-------|-------------|--------|
| Food Donation | 20% | NPC offers food (reduces hunger) |
| Money Donation | 30% | NPC gives $1-5 |

### Bad Response Events

Triggered after negative conversation outcomes.

| Event | Probability | Effect |
|-------|-------------|--------|
| Food Donation | 5% | (10% × 50%) Hostile NPC gives food anyway |
| Satanic Bible | 5% | (10% × 50%) Thrown at player, can accept |
| Satanic Ally | 5% | (Satanic players only) Meet ally, +15% bonus |

---

## The Hidden Satanic Path

The game contains a hidden mechanic where players can become Satanic preachers.

### Discovery

1. Player experiences bad response (rejection)
2. 10% chance of special event
3. 50% of those: angry NPC throws Satanic Bible at player
4. Player chooses to accept or reject

### Acceptance

If player accepts the Satanic Bible:
- `state.religion` changes to `Religion.SATANIC`
- Base conversion rate jumps to 50% (highest in game)
- Can now meet Satanic allies for additional bonuses

### Satanic Allies

Once Satanic, bad response events can trigger ally encounters:
- Each ally grants +15% conversion bonus (`state.satanic_bonus`)
- Cumulative with other bonuses
- Creates positive feedback loop

### Victory Condition

Converting 10+ souls as Satanic triggers special victory message.

---

## Event Architecture

### Event Dataclass

```python
@dataclass
class Event:
    name: str
    probability: float
    condition: Callable[[GameState], bool]
    handler: Callable[[GameState, ConsoleUI], None]
```

### EventManager

```python
class EventManager:
    success_events: list[Event]
    failure_events: list[Event]

    def trigger_success_events(state, ui)
    def trigger_bad_response(state, ui)
```

### Condition Functions

```python
def always(state) -> bool           # Always triggers
def not_satanic(state) -> bool      # Non-Satanic only
def is_satanic(state) -> bool       # Satanic only
```

---

## Event Probabilities (config.py)

```python
FOOD_DONATION_CHANCE = 0.2      # 20% after conversion
SATANIC_BIBLE_CHANCE = 0.1      # 10% on bad response
FOOD_OR_BIBLE_SPLIT = 0.5       # 50/50 food vs bible
SATANIC_ALLY_BONUS = 0.15       # +15% per ally
MONEY_DONATION_CHANCE = 0.3     # 30% after conversion
MONEY_DONATION_MIN = 1
MONEY_DONATION_MAX = 5
```

---

## Integration Points

### After Conversion

```python
event_manager.trigger_success_events(state, ui)
# May trigger food or money donation
```

### After Bad Response

```python
event_manager.trigger_bad_response(state, ui)
# May trigger Satanic Bible or ally encounter
```

---

## Design Intent

The Satanic path serves as:
1. **Easter egg** - Hidden discovery for thorough players
2. **Power fantasy** - High conversion rate feels rewarding
3. **Risk/reward** - Must fail first to discover path
4. **Replay incentive** - Different experience on second playthrough

---

*See also: [Game Balance](../design/game-balance.md) | [Conversation System](conversation.md)*
