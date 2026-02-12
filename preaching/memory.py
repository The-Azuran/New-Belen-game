"""Memory system for tracking game events and enabling emergent narrative."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class EventType(Enum):
    """Types of memorable events."""
    CONVERSION = "conversion"
    REJECTION = "rejection"
    POLITE_EXIT = "polite_exit"
    HOSTILE_CHURCH = "hostile_church"
    FRIENDLY_CHURCH = "friendly_church"
    NO_ANSWER = "no_answer"  # Door not opened
    SATANIC_ENCOUNTER = "satanic_encounter"
    HUNGRY_DAY = "hungry_day"  # Day ended from exhaustion
    DONATION_RECEIVED = "donation_received"
    ITEM_PURCHASED = "item_purchased"
    LIBRARY_RESEARCH = "library_research"
    RESISTANT_REVEALED = "resistant_revealed"  # Found out someone can't be converted
    DAY_START = "day_start"
    DAY_END = "day_end"
    # Combat events
    DEMON_ENCOUNTER = "demon_encounter"
    DEMON_DEFEAT = "demon_defeat"
    DEMON_ESCAPE = "demon_escape"
    DEMON_CAPTURE = "demon_capture"
    DEMON_BETRAYAL = "demon_betrayal"
    DEMON_BANISH = "demon_banish"
    PHYSICAL_CONFRONTATION = "physical_confrontation"


@dataclass
class Memory:
    """A single memorable event that can influence narrative."""
    day: int
    event_type: EventType
    neighborhood: str
    npc_name: Optional[str] = None
    npc_personality: Optional[str] = None
    location_name: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)

    def has_tag(self, tag: str) -> bool:
        """Check if this memory has a specific tag."""
        return tag in self.tags

    def matches(self, **criteria) -> bool:
        """Check if memory matches given criteria."""
        for key, value in criteria.items():
            if key == "tags":
                if not any(t in self.tags for t in value):
                    return False
            elif hasattr(self, key):
                if getattr(self, key) != value:
                    return False
            elif key in self.details:
                if self.details[key] != value:
                    return False
            else:
                return False
        return True


@dataclass
class DaySummary:
    """Summary of a day's events for journal generation."""
    day: int
    day_name: str
    weather: str
    conversions: int = 0
    rejections: int = 0
    polite_exits: int = 0
    doors_unanswered: int = 0
    money_earned: int = 0
    money_spent: int = 0
    hostile_churches: int = 0
    friendly_churches: int = 0
    neighborhoods_visited: list[str] = field(default_factory=list)
    notable_npcs: list[str] = field(default_factory=list)  # Names worth remembering
    satanic_events: int = 0
    ended_hungry: bool = False
    tags: list[str] = field(default_factory=list)  # Overall day mood tags


class MemoryManager:
    """Manages the collection of memories and provides query capabilities."""

    def __init__(self) -> None:
        self.memories: list[Memory] = []
        self.day_summaries: list[DaySummary] = []
        self._current_day_summary: Optional[DaySummary] = None

    def start_day(self, day: int, day_name: str, weather: str) -> None:
        """Begin tracking a new day."""
        self._current_day_summary = DaySummary(
            day=day,
            day_name=day_name,
            weather=weather,
        )
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DAY_START,
            neighborhood="",
            details={"day_name": day_name, "weather": weather}
        ))

    def end_day(self, ended_hungry: bool = False) -> DaySummary:
        """Finalize the current day and return its summary."""
        if self._current_day_summary is None:
            raise RuntimeError("No day in progress")

        summary = self._current_day_summary
        summary.ended_hungry = ended_hungry

        # Determine day mood tags based on what happened
        summary.tags = self._compute_day_tags(summary)

        self.day_summaries.append(summary)
        self.add_memory(Memory(
            day=summary.day,
            event_type=EventType.DAY_END,
            neighborhood="",
            tags=summary.tags,
            details={"ended_hungry": ended_hungry}
        ))

        result = summary
        self._current_day_summary = None
        return result

    def _compute_day_tags(self, summary: DaySummary) -> list[str]:
        """Compute mood tags for a day based on events."""
        tags = []

        # Success/failure ratio
        total_encounters = summary.conversions + summary.rejections + summary.polite_exits
        if total_encounters > 0:
            success_rate = summary.conversions / total_encounters
            if success_rate >= 0.5:
                tags.append("successful")
            elif success_rate <= 0.2:
                tags.append("difficult")
            if summary.conversions == 0:
                tags.append("fruitless")
            if summary.conversions >= 3:
                tags.append("blessed")

        # Rejection heavy
        if summary.rejections >= 3:
            tags.append("rejection_heavy")

        # Doors not opening
        if summary.doors_unanswered >= 2:
            tags.append("unwelcome")

        # Church experiences
        if summary.hostile_churches > 0:
            tags.append("persecuted")
        if summary.friendly_churches > 0:
            tags.append("fellowship")

        # Resource stress
        if summary.ended_hungry:
            tags.append("exhausted")
        if summary.money_spent > summary.money_earned:
            tags.append("costly")

        # Satanic path
        if summary.satanic_events > 0:
            tags.append("dark_touched")

        # Weather influence
        if summary.weather in ["hot", "cold"]:
            tags.append("harsh_conditions")

        return tags

    def add_memory(self, memory: Memory) -> None:
        """Add a memory to the collection."""
        self.memories.append(memory)

    def record_conversion(self, day: int, neighborhood: str, npc_name: str,
                         npc_personality: str, approach_tags: list[str]) -> None:
        """Record a successful conversion."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.CONVERSION,
            neighborhood=neighborhood,
            npc_name=npc_name,
            npc_personality=npc_personality,
            tags=approach_tags + ["success"],
            details={}
        ))
        if self._current_day_summary:
            self._current_day_summary.conversions += 1
            self._current_day_summary.notable_npcs.append(npc_name)
            if neighborhood not in self._current_day_summary.neighborhoods_visited:
                self._current_day_summary.neighborhoods_visited.append(neighborhood)

    def record_rejection(self, day: int, neighborhood: str, npc_name: str,
                        npc_personality: str, was_aggressive: bool = False) -> None:
        """Record a rejection."""
        tags = ["failure"]
        if was_aggressive:
            tags.append("aggressive_backfire")

        self.add_memory(Memory(
            day=day,
            event_type=EventType.REJECTION,
            neighborhood=neighborhood,
            npc_name=npc_name,
            npc_personality=npc_personality,
            tags=tags,
        ))
        if self._current_day_summary:
            self._current_day_summary.rejections += 1
            if neighborhood not in self._current_day_summary.neighborhoods_visited:
                self._current_day_summary.neighborhoods_visited.append(neighborhood)

    def record_polite_exit(self, day: int, neighborhood: str, npc_name: str) -> None:
        """Record a polite exit (neither conversion nor rejection)."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.POLITE_EXIT,
            neighborhood=neighborhood,
            npc_name=npc_name,
            tags=["neutral"],
        ))
        if self._current_day_summary:
            self._current_day_summary.polite_exits += 1

    def record_no_answer(self, day: int, neighborhood: str) -> None:
        """Record when no one answers the door (reputation too low)."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.NO_ANSWER,
            neighborhood=neighborhood,
            tags=["unwelcome"],
        ))
        if self._current_day_summary:
            self._current_day_summary.doors_unanswered += 1

    def record_hostile_church(self, day: int, neighborhood: str, church_name: str) -> None:
        """Record a hostile church encounter."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.HOSTILE_CHURCH,
            neighborhood=neighborhood,
            location_name=church_name,
            tags=["persecution", "painful"],
        ))
        if self._current_day_summary:
            self._current_day_summary.hostile_churches += 1

    def record_friendly_church(self, day: int, neighborhood: str, church_name: str) -> None:
        """Record a friendly church encounter."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.FRIENDLY_CHURCH,
            neighborhood=neighborhood,
            location_name=church_name,
            tags=["fellowship", "encouraged"],
        ))
        if self._current_day_summary:
            self._current_day_summary.friendly_churches += 1

    def record_donation(self, day: int, amount: int) -> None:
        """Record receiving a donation."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DONATION_RECEIVED,
            neighborhood="",
            tags=["provision"],
            details={"amount": amount}
        ))
        if self._current_day_summary:
            self._current_day_summary.money_earned += amount

    def record_purchase(self, day: int, item_name: str, cost: int) -> None:
        """Record purchasing an item."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.ITEM_PURCHASED,
            neighborhood="",
            tags=["resource"],
            details={"item": item_name, "cost": cost}
        ))
        if self._current_day_summary:
            self._current_day_summary.money_spent += cost

    def record_satanic_event(self, day: int, event_description: str) -> None:
        """Record a satanic path event."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.SATANIC_ENCOUNTER,
            neighborhood="",
            tags=["dark", "temptation"],
            details={"description": event_description}
        ))
        if self._current_day_summary:
            self._current_day_summary.satanic_events += 1

    def record_resistant_revealed(self, day: int, neighborhood: str, npc_name: str) -> None:
        """Record discovering someone is resistant to conversion."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.RESISTANT_REVEALED,
            neighborhood=neighborhood,
            npc_name=npc_name,
            tags=["knowledge", "limitation"],
        ))

    def record_demon_encounter(self, day: int, neighborhood: str, npc_name: str,
                              demon_type: str, combat_type: str) -> None:
        """Record encountering a demon."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DEMON_ENCOUNTER,
            neighborhood=neighborhood,
            npc_name=npc_name,
            details={"demon_type": demon_type, "combat_type": combat_type},
            tags=["combat", "supernatural", "danger"],
        ))

    def record_demon_defeat(self, day: int, neighborhood: str, npc_name: str,
                           demon_type: str, combat_type: str) -> None:
        """Record defeating a demon."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DEMON_DEFEAT,
            neighborhood=neighborhood,
            npc_name=npc_name,
            details={"demon_type": demon_type, "combat_type": combat_type},
            tags=["combat", "victory", "supernatural"],
        ))

    def record_demon_escape(self, day: int, neighborhood: str, npc_name: str,
                           demon_type: str) -> None:
        """Record fleeing from a demon."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DEMON_ESCAPE,
            neighborhood=neighborhood,
            npc_name=npc_name,
            details={"demon_type": demon_type},
            tags=["combat", "retreat", "supernatural"],
        ))

    def record_physical_confrontation(self, day: int, neighborhood: str,
                                     npc_name: str) -> None:
        """Record a physical confrontation with a demon."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.PHYSICAL_CONFRONTATION,
            neighborhood=neighborhood,
            npc_name=npc_name,
            tags=["combat", "physical", "danger"],
        ))

    def record_demon_capture(self, day: int, neighborhood: str, npc_name: str,
                            demon_type: str) -> None:
        """Record capturing a demon as an ally."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DEMON_CAPTURE,
            neighborhood=neighborhood,
            npc_name=npc_name,
            details={"demon_type": demon_type},
            tags=["dark_path", "corrupted", "supernatural"],
        ))

    def record_demon_betrayal(self, day: int, neighborhood: str,
                              demon_type: str) -> None:
        """Record a demon ally betrayal."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DEMON_BETRAYAL,
            neighborhood=neighborhood,
            details={"demon_type": demon_type},
            tags=["danger", "consequence", "supernatural"],
        ))

    def record_demon_banish(self, day: int, neighborhood: str, npc_name: str,
                            demon_type: str) -> None:
        """Record banishing a demon."""
        self.add_memory(Memory(
            day=day,
            event_type=EventType.DEMON_BANISH,
            neighborhood=neighborhood,
            npc_name=npc_name,
            details={"demon_type": demon_type},
            tags=["combat", "victory", "righteous"],
        ))

    # Query methods for narrative generation

    def get_memories_for_day(self, day: int) -> list[Memory]:
        """Get all memories from a specific day."""
        return [m for m in self.memories if m.day == day]

    def get_memories_by_type(self, event_type: EventType) -> list[Memory]:
        """Get all memories of a specific type."""
        return [m for m in self.memories if m.event_type == event_type]

    def get_memories_for_neighborhood(self, neighborhood: str) -> list[Memory]:
        """Get all memories from a specific neighborhood."""
        return [m for m in self.memories if m.neighborhood == neighborhood]

    def get_memories_for_npc(self, npc_name: str) -> list[Memory]:
        """Get all memories involving a specific NPC."""
        return [m for m in self.memories if m.npc_name == npc_name]

    def get_memories_with_tag(self, tag: str) -> list[Memory]:
        """Get all memories with a specific tag."""
        return [m for m in self.memories if tag in m.tags]

    def find_similar_memories(self, current: Memory, limit: int = 3) -> list[Memory]:
        """Find memories similar to the current one (for callbacks/echoes)."""
        similar = []
        for m in self.memories:
            if m == current:
                continue
            score = 0
            # Same personality type
            if m.npc_personality == current.npc_personality and current.npc_personality:
                score += 2
            # Same neighborhood
            if m.neighborhood == current.neighborhood and current.neighborhood:
                score += 1
            # Overlapping tags
            score += len(set(m.tags) & set(current.tags))
            # Same event type
            if m.event_type == current.event_type:
                score += 1

            if score > 0:
                similar.append((score, m))

        similar.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in similar[:limit]]

    def get_recurring_patterns(self) -> dict[str, int]:
        """Identify recurring patterns in memories."""
        patterns = {
            "total_conversions": len(self.get_memories_by_type(EventType.CONVERSION)),
            "total_rejections": len(self.get_memories_by_type(EventType.REJECTION)),
            "hostile_encounters": len(self.get_memories_by_type(EventType.HOSTILE_CHURCH)),
            "satanic_touches": len(self.get_memories_by_type(EventType.SATANIC_ENCOUNTER)),
            "doors_closed": len(self.get_memories_by_type(EventType.NO_ANSWER)),
        }

        # Count personality types converted
        conversions = self.get_memories_by_type(EventType.CONVERSION)
        personality_counts: dict[str, int] = {}
        for m in conversions:
            if m.npc_personality:
                personality_counts[m.npc_personality] = personality_counts.get(m.npc_personality, 0) + 1
        patterns["favorite_converts"] = personality_counts

        return patterns

    def get_streak(self, event_type: EventType) -> int:
        """Get current streak of consecutive events of a type."""
        if not self.memories:
            return 0

        streak = 0
        for m in reversed(self.memories):
            if m.event_type == event_type:
                streak += 1
            elif m.event_type in [EventType.DAY_START, EventType.DAY_END]:
                continue  # Don't break streak on day boundaries
            else:
                break
        return streak

    def had_previous_encounter(self, npc_name: str) -> bool:
        """Check if we've encountered this NPC before."""
        return any(m.npc_name == npc_name for m in self.memories)

    def get_npc_history(self, npc_name: str) -> list[Memory]:
        """Get full history with a specific NPC."""
        return [m for m in self.memories if m.npc_name == npc_name]
