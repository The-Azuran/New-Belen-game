# System: Items & Shop

**Status:** Complete
**Location:** `preaching/items.py`

---

## Overview

The item system provides food (hunger management) and pamphlets (conversion bonuses). Items are purchased at Store locations using the player's limited money.

## Item Categories

### Food Items

Reduce hunger when consumed. Can be stored in inventory for later.

| Item | Price | Hunger Restored |
|------|-------|-----------------|
| Candy Bar | $2 | 10 |
| Bag of Chips | $3 | 10 |
| Hot Dog | $4 | 20 |
| Sandwich | $5 | 20 |
| Microwave Burrito | $6 | 35 |
| Fried Chicken Meal | $8 | 35 |

### Pamphlets

Provide temporary conversion bonuses with personality-specific tags.

| Pamphlet | Price | Tags | Bonus Personalities |
|----------|-------|------|---------------------|
| Family Values | $5 | family, community, traditional | lonely, seeker |
| Salvation Tract | $5 | hellfire, urgent, spiritual | seeker |
| Reasons to Believe | $5 | logical, evidence | skeptic, intellectual |
| Join Our Community | $5 | community, friendly, no_pressure | lonely, cynic |
| Personal Testimony | $5 | personal, authentic | cynic, seeker |
| Basic Pamphlets | $5 | community, friendly, no_pressure | (generic) |

**Pamphlet Effect:** +10% conversion bonus for 5 encounters. Tags match against NPC personality weaknesses.

### Special Items

| Item | Price | Effect |
|------|-------|--------|
| Pocket Bible | $15 | Permanent +5% conversion rate (applied immediately, not stored) |

---

## Store Inventory Generation

Stores have randomly generated inventory:
- 2-3 food items (always)
- 50% chance of special item (Bible or generic pamphlet)
- 30% chance of specific pamphlet type

```python
def get_random_store_inventory(count: int = 5) -> list[Item]
```

---

## Data Structures

### Item

Store item definition:

```python
@dataclass
class Item:
    name: str
    description: str
    price: int
    effect: Callable[[GameState], None]
    storable: bool              # Can be saved in inventory
    item_type: str              # "food" or "pamphlet"
    hunger_restore: int         # For food
    pamphlet_id: str            # For pamphlets
    pamphlet_tags: list[str]    # Tags for conversation matching
```

### Pamphlet

Pamphlet type definition:

```python
@dataclass
class Pamphlet:
    id: str
    name: str
    description: str
    tags: list[str]             # Tags for conversation matching
    bonus_personalities: list[str]
    penalty_personalities: list[str]
```

### InventoryItem

Player's stored items:

```python
@dataclass
class InventoryItem:
    item_type: str              # "food" or "pamphlet"
    name: str
    description: str
    hunger_restore: int
    pamphlet_id: str
    pamphlet_tags: list[str]
```

---

## Economy Balance

| Resource | Value |
|----------|-------|
| Starting money | $10 |
| Money donation (30% chance) | $1-5 |
| Sunday offering bonus | +$10 |

With starting money of $10, player can afford:
- 5 Candy Bars, or
- 2 Sandwiches, or
- 2 Pamphlets, or
- 1 Fried Chicken + 1 Candy Bar

The Pocket Bible ($15) requires saving up or good luck with donations.

---

## Integration Points

### Store Visit Flow

1. Player selects Store location
2. `get_random_store_inventory()` generates available items
3. UI displays items with prices
4. Player purchases → `state.money` decreases
5. Item effect applied immediately OR stored in `state.inventory`

### Pamphlet Usage Flow

1. Player activates pamphlet from inventory
2. `state.pamphlet_boost_remaining = 5`
3. `state.pamphlet_boost_amount = 0.10`
4. `state.active_pamphlet_tags = pamphlet.tags`
5. Conversation engine uses tags for bonus matching
6. Each conversation decrements `pamphlet_boost_remaining`

---

*See also: [Conversation System](conversation.md) | [Game Balance](../design/game-balance.md)*
