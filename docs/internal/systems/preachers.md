# System: Preachers

**Status:** Complete
**Location:** `preaching/preachers.py`

---

## Overview

Players choose from 7 preset preachers or create a custom character. Each preacher has unique bonuses, penalties, and personality affinities that affect gameplay.

## Preacher Stats

| Stat | Description |
|------|-------------|
| `conversion_bonus` | Percentage added to base conversion rate |
| `reputation_bonus` | Starting reputation modifier in all neighborhoods |
| `money_bonus` | Extra starting money (added to base $10) |
| `hunger_rate` | Multiplier for hunger gain (lower = better) |
| `personality_bonus` | Dict of personality → bonus% with that NPC type |

---

## Preset Preachers

### Belen Torres (Default)
> An old Dominican woman, former witch turned evangelist with stories to tell

| Stat | Value | Notes |
|------|-------|-------|
| Conversion | +5% | |
| Reputation | -5 | Some have heard rumors |
| Money | +$15 | Online ministry income |
| Hunger Rate | 1.1x | Old bones tire faster |
| Personality | lonely +15%, seeker +20%, skeptic -10% | |

**Special:** Ex-witch who survived Haitian Vudu and demon encounters. Her testimony is wild.

---

### Dr. Scott Johnson
> A scholarly theologian with logical arguments

| Stat | Value | Notes |
|------|-------|-------|
| Conversion | 0% | |
| Reputation | +5 | Respected |
| Money | +$20 | |
| Hunger Rate | 1.2x | Tires easily |
| Personality | intellectual +15%, skeptic +10% | |

**Special:** Persuasive with intellectuals and skeptics, but tires easily.

---

### Sister Joyce Meyer
> An energetic motivational preacher

| Stat | Value | Notes |
|------|-------|-------|
| Conversion | 0% | |
| Reputation | 0 | |
| Money | +$10 | |
| Hunger Rate | 0.9x | High energy |
| Personality | cynic +15%, hostile +5% | |

**Special:** High energy and can break through to cynics.

---

### Pastor Billy Graham Jr.
> A charismatic crusade-style preacher

| Stat | Value | Notes |
|------|-------|-------|
| Conversion | +10% | Strong bonus |
| Reputation | +10 | Famous name |
| Money | $0 | |
| Hunger Rate | 1.1x | |
| Personality | seeker +15% | |

**Special:** Famous name opens doors, great with seekers.

---

### Reverend Joel Prosperity
> A prosperity gospel preacher with a winning smile

| Stat | Value | Notes |
|------|-------|-------|
| Conversion | -5% | People skeptical |
| Reputation | -5 | Some distrust |
| Money | +$50 | Wealthy |
| Hunger Rate | 0.8x | Eats well |
| Personality | lonely +10% | |

**Special:** Wealthy but people are wary of his motives.

---

### Brother Marcus
> A humble street preacher with fire in his heart

| Stat | Value | Notes |
|------|-------|-------|
| Conversion | 0% | |
| Reputation | -10 | Seen as aggressive |
| Money | -$10 | Starts poor |
| Hunger Rate | 0.85x | Used to hardship |
| Personality | hostile +15%, skeptic -10% | |

**Special:** Fearless with hostile crowds but too intense for skeptics.

---

### Titi Olga
> A wonderfully warm community mother with a heart full of love for everyone

| Stat | Value | Notes |
|------|-------|-------|
| Conversion | +8% | She's "persuasive" |
| Reputation | +5 | People think she's sweet |
| Money | +$30 | Good at "fundraising" |
| Hunger Rate | 0.75x | Takes care of herself |
| Personality | lonely +20%, cynic +15%, skeptic +5% | |

**Special:** Such a blessing to everyone she meets. Truly. Everyone says so.

---

### Custom Preacher

| Stat | Value |
|------|-------|
| Conversion | 0% |
| Reputation | 0 |
| Money | $0 |
| Hunger Rate | 1.0x |
| Personality | (none) |

**Special:** A blank slate - no bonuses or penalties.

---

## Data Structure

```python
@dataclass
class Preacher:
    id: str
    name: str
    description: str
    conversion_bonus: float = 0.0
    reputation_bonus: int = 0
    money_bonus: int = 0
    hunger_rate: float = 1.0
    personality_bonus: dict[str, float] = field(default_factory=dict)
    special: str = ""

    def apply_to_state(self, state: GameState) -> None:
        """Apply this preacher's bonuses to the game state."""
```

---

## Personality Bonus Mechanics

Personality bonuses affect **starting interest** in conversations:

```python
# In ConversationState.start():
if npc.personality in personality_bonus:
    # Convert percentage to interest points (e.g., 0.10 = +5 interest)
    starting_interest += int(personality_bonus[npc.personality] * 50)
```

| Bonus | Interest Effect |
|-------|-----------------|
| +20% | +10 starting interest |
| +15% | +7-8 starting interest |
| +10% | +5 starting interest |
| -10% | -5 starting interest |

---

## Balance Considerations

**Best overall:** Titi Olga (high conversion, low hunger, good money, multiple personality bonuses)

**Best conversion:** Pastor Billy Graham Jr. (+10% conversion, +10 reputation, seeker bonus)

**Highest difficulty:** Brother Marcus (-10 reputation, -$10 starting money, penalty with skeptics)

**Economic advantage:** Reverend Joel Prosperity (+$50 starting money)

**Efficiency:** Sister Joyce Meyer (0.9x hunger rate, cynic bonus)

**Narrative flavor:** Belen Torres (complex backstory, mixed bonuses/penalties)

---

## Integration Points

### Game Start

1. Player selects preacher (or custom)
2. `preacher.apply_to_state(state)` called
3. Bonuses applied to GameState

### During Conversation

1. `ConversationState.start()` checks `preacher_personality_bonus`
2. Matching personality gets interest bonus
3. Affects initial conversation state

### Hunger Calculation

1. Base hunger gain determined by weather
2. Multiplied by `state.preacher_hunger_rate`
3. Final hunger added to state

---

*See also: [Game Balance](../design/game-balance.md) | [Conversation System](conversation.md)*
