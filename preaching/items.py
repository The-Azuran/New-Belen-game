"""Item and shop system."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .models import GameState, InventoryItem


@dataclass
class Item:
    """An item that can be purchased."""
    name: str
    description: str
    price: int
    effect: Callable[[GameState], None]
    # For inventory system
    storable: bool = False
    item_type: str = ""  # "food" or "pamphlet"
    hunger_restore: int = 0
    pamphlet_id: str = ""
    pamphlet_tags: list[str] = field(default_factory=list)


@dataclass
class Pamphlet:
    """A pamphlet type with specific tags for conversation matching."""
    id: str
    name: str
    description: str
    tags: list[str]
    bonus_personalities: list[str]
    penalty_personalities: list[str]


# Pamphlet types - each matches different personality weaknesses
PAMPHLET_TYPES: list[Pamphlet] = [
    Pamphlet(
        id="family",
        name="Family Values Pamphlet",
        description="Focus on family and traditional values",
        tags=["family", "community", "traditional"],
        bonus_personalities=["lonely", "seeker"],
        penalty_personalities=[],
    ),
    Pamphlet(
        id="hellfire",
        name="Salvation Tract",
        description="Urgent message about salvation",
        tags=["hellfire", "urgent", "spiritual"],
        bonus_personalities=["seeker"],
        penalty_personalities=["skeptic", "intellectual", "hostile"],
    ),
    Pamphlet(
        id="logical",
        name="Reasons to Believe",
        description="Evidence-based apologetics",
        tags=["logical", "evidence"],
        bonus_personalities=["skeptic", "intellectual"],
        penalty_personalities=[],
    ),
    Pamphlet(
        id="community",
        name="Join Our Community",
        description="Emphasis on fellowship and belonging",
        tags=["community", "friendly", "no_pressure"],
        bonus_personalities=["lonely", "cynic"],
        penalty_personalities=[],
    ),
    Pamphlet(
        id="testimony",
        name="Personal Testimony",
        description="Real stories of changed lives",
        tags=["personal", "authentic"],
        bonus_personalities=["cynic", "seeker"],
        penalty_personalities=[],
    ),
]


def get_pamphlet_by_id(pamphlet_id: str) -> Pamphlet | None:
    """Get a pamphlet by its ID."""
    return next((p for p in PAMPHLET_TYPES if p.id == pamphlet_id), None)


def create_inventory_item(item: Item) -> "InventoryItem":
    """Create an InventoryItem from a store Item."""
    from .models import InventoryItem
    return InventoryItem(
        item_type=item.item_type,
        name=item.name,
        description=item.description,
        hunger_restore=item.hunger_restore,
        pamphlet_id=item.pamphlet_id,
        pamphlet_tags=item.pamphlet_tags.copy() if item.pamphlet_tags else [],
    )


def effect_reduce_hunger_small(state: GameState) -> None:
    """Reduce hunger by a small amount."""
    state.hunger = max(0, state.hunger - 10)


def effect_reduce_hunger_medium(state: GameState) -> None:
    """Reduce hunger by a medium amount."""
    state.hunger = max(0, state.hunger - 20)


def effect_reduce_hunger_large(state: GameState) -> None:
    """Reduce hunger by a large amount."""
    state.hunger = max(0, state.hunger - 35)


def effect_pamphlet_boost(state: GameState, pamphlet_id: str = "community") -> None:
    """Grant a temporary conversion boost with specific pamphlet tags."""
    pamphlet = get_pamphlet_by_id(pamphlet_id)
    if pamphlet:
        state.pamphlet_boost_remaining = 5
        state.pamphlet_boost_amount = 0.10
        state.active_pamphlet_tags = pamphlet.tags.copy()
    else:
        # Fallback to generic boost
        state.pamphlet_boost_remaining = 3
        state.pamphlet_boost_amount = 0.10
        state.active_pamphlet_tags = []


def create_pamphlet_item(pamphlet: Pamphlet) -> Item:
    """Create a store item from a pamphlet type."""
    def effect(state: GameState) -> None:
        effect_pamphlet_boost(state, pamphlet.id)

    return Item(
        name=pamphlet.name,
        description=f"{pamphlet.description} (+10% for 5 encounters)",
        price=5,
        effect=effect,
        storable=True,
        item_type="pamphlet",
        pamphlet_id=pamphlet.id,
        pamphlet_tags=pamphlet.tags.copy(),
    )


def effect_bible_bonus(state: GameState) -> None:
    """Grant a permanent small conversion bonus."""
    state.bible_bonus += 0.05


# Standard store inventory
STORE_ITEMS = [
    Item(
        name="Candy Bar",
        description="A quick snack to take the edge off (-10 hunger)",
        price=2,
        effect=effect_reduce_hunger_small,
        storable=True,
        item_type="food",
        hunger_restore=10,
    ),
    Item(
        name="Bag of Chips",
        description="Crunchy and satisfying (-10 hunger)",
        price=3,
        effect=effect_reduce_hunger_small,
        storable=True,
        item_type="food",
        hunger_restore=10,
    ),
    Item(
        name="Sandwich",
        description="A filling lunch option (-20 hunger)",
        price=5,
        effect=effect_reduce_hunger_medium,
        storable=True,
        item_type="food",
        hunger_restore=20,
    ),
    Item(
        name="Hot Dog",
        description="Fresh off the roller grill (-20 hunger)",
        price=4,
        effect=effect_reduce_hunger_medium,
        storable=True,
        item_type="food",
        hunger_restore=20,
    ),
    Item(
        name="Microwave Burrito",
        description="Hot, cheesy, and substantial (-35 hunger)",
        price=6,
        effect=effect_reduce_hunger_large,
        storable=True,
        item_type="food",
        hunger_restore=35,
    ),
    Item(
        name="Fried Chicken Meal",
        description="Three pieces with biscuit (-35 hunger)",
        price=8,
        effect=effect_reduce_hunger_large,
        storable=True,
        item_type="food",
        hunger_restore=35,
    ),
    # Generic pamphlet - stores may also have specific types
    Item(
        name="Basic Pamphlets",
        description="Generic religious pamphlets (+10% for 3 encounters)",
        price=5,
        effect=lambda state: effect_pamphlet_boost(state, "community"),
        storable=True,
        item_type="pamphlet",
        pamphlet_id="community",
        pamphlet_tags=["community", "friendly", "no_pressure"],
    ),
    Item(
        name="Pocket Bible",
        description="Permanent +5% conversion rate (used immediately)",
        price=15,
        effect=effect_bible_bonus,
        storable=False,  # Applied immediately
    ),
]


def get_random_store_inventory(count: int = 5) -> list[Item]:
    """Get a random selection of items for a store."""
    import random
    # Always include at least one food item and maybe a pamphlet
    food_items = [i for i in STORE_ITEMS if "hunger" in i.description.lower() or
                  any(word in i.name.lower() for word in ["candy", "chips", "sandwich", "dog", "burrito", "chicken"])]
    special_items = [i for i in STORE_ITEMS if i not in food_items]

    inventory = []
    # Add 2-3 food items
    inventory.extend(random.sample(food_items, min(3, len(food_items))))
    # Maybe add a special item (bible or generic pamphlet)
    if random.random() < 0.5 and special_items:
        inventory.append(random.choice(special_items))

    # Maybe add a specific pamphlet type (30% chance)
    if random.random() < 0.3:
        pamphlet = random.choice(PAMPHLET_TYPES)
        inventory.append(create_pamphlet_item(pamphlet))

    return inventory[:count]
