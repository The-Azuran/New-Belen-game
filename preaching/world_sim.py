"""Between-day world simulation for emergent narrative.

Authored by Rowan Valle; Executed by Claude Code.

Simulates what happens in the world overnight: reputation spreading,
NPC reactions, conversion ripple effects, and community gossip.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import GameState
    from .memory import MemoryManager, DaySummary, EventType


@dataclass
class WorldEvent:
    """An event that happened in the world between days."""
    category: str  # "reputation", "gossip", "ripple", "community"
    text: str
    neighborhood: str = ""
    reputation_change: int = 0  # Applied to a neighborhood
    target_neighborhood: str = ""  # If different from source


# =============================================================================
# Narrative templates for world events
# =============================================================================

REPUTATION_SPREAD_POSITIVE = [
    "Word of your kindness in {source} has reached {target}. People are curious about you.",
    "Someone from {source} mentioned the 'nice preacher' to a friend in {target}.",
    "A woman from {source} told her sister in {target} about your visit. She seemed impressed.",
    "The pastor in {target} heard about your work in {source}. He mentioned it in passing.",
]

REPUTATION_SPREAD_NEGATIVE = [
    "News travels fast. People in {target} heard about trouble in {source}.",
    "A man from {source} warned his coworkers in {target} about a 'pushy preacher.'",
    "Someone in {target} saw you get turned away in {source}. Word gets around.",
    "The gossip from {source} reached {target}. They're wary of strangers now.",
]

NPC_REACTION_POSITIVE = [
    "{npc} told a neighbor about your conversation. They seemed moved.",
    "{npc} has been thinking about what you said. Their spouse noticed a change.",
    "You made an impression on {npc}. They mentioned you at dinner.",
    "{npc} kept the pamphlet you left. It's sitting on their kitchen table.",
]

NPC_REACTION_NEGATIVE = [
    "{npc} told their family about the door-to-door preacher. They weren't kind about it.",
    "{npc} put up a 'No Solicitors' sign after your visit.",
    "{npc} called their friend to complain about being bothered at home.",
    "{npc} warned the neighbors: 'Don't answer the door if a preacher comes by.'",
]

CONVERSION_RIPPLE = [
    "After converting {npc}, their neighbor is asking questions about faith.",
    "{npc}'s family noticed the change in them. Some are curious, others concerned.",
    "The conversion of {npc} in {neighborhood} is the talk of the block.",
    "{npc} invited a friend to church. Your work is spreading.",
    "{npc} told their coworker about finding faith. It sparked a long conversation.",
]

COMMUNITY_EVENTS = [
    "A church in {neighborhood} is organizing a community dinner this weekend.",
    "Someone left religious tracts at the bus stop in {neighborhood}. It wasn't you.",
    "A heated letter about door-to-door preachers appeared in the {town} Gazette.",
    "The convenience store in {neighborhood} has a 'No Soliciting' sign now.",
    "A family in {neighborhood} put up a yard sign: 'Protected by prayer.'",
    "Kids in {neighborhood} were playing 'preacher' in the yard. You're becoming folklore.",
    "The local diner in {town} had a debate about religion at the counter. Your name came up.",
    "Rain is expected tomorrow. People will be home.",
    "A neighborhood watch meeting in {neighborhood} discussed 'strangers at doors.'",
    "Someone spray-painted 'REPENT' on a fence in {neighborhood}. Wasn't you, but people wonder.",
]

DEMON_ALLY_EVENTS = [
    "Your demon allies whisper in the dark. They speak of others like them, nearby.",
    "You dream of shadows moving through {neighborhood}. The demons are restless.",
    "One of your demons claims it knows a family in {neighborhood}. 'They are ripe,' it says.",
    "The darkness in you draws attention. Something in {neighborhood} knows you're coming.",
]


class WorldSimulator:
    """Simulates world events between days."""

    def simulate_night(self, state: GameState,
                       memory: MemoryManager,
                       day_summary: DaySummary) -> list[WorldEvent]:
        """Run between-day simulation. Returns events to narrate next morning."""
        events: list[WorldEvent] = []

        events.extend(self._spread_reputation(state, day_summary))
        events.extend(self._npc_reactions(state, day_summary, memory))
        events.extend(self._conversion_ripples(state, day_summary, memory))
        events.extend(self._community_chatter(state, day_summary))
        events.extend(self._demon_ally_events(state))

        # Cap at 3 events to avoid info overload
        if len(events) > 3:
            events = random.sample(events, 3)

        return events

    def _spread_reputation(self, state: GameState,
                           summary: DaySummary) -> list[WorldEvent]:
        """Reputation bleeds to adjacent neighborhoods in the same town."""
        events = []
        if not state.county:
            return events

        for visited_name in summary.neighborhoods_visited:
            rep = state.reputation.get_reputation(visited_name)
            if abs(rep) < 5:
                continue  # Not notable enough to spread

            # Find the town containing this neighborhood
            source_town = None
            for town in state.county.towns:
                for n in town.neighborhoods:
                    if n.name == visited_name:
                        source_town = town
                        break

            if not source_town:
                continue

            # 30% chance to spread to each adjacent neighborhood in same town
            for neighbor in source_town.neighborhoods:
                if neighbor.name == visited_name:
                    continue
                if random.random() > 0.30:
                    continue

                spread_amount = rep // 5  # 20% of current rep
                if spread_amount == 0:
                    continue

                state.reputation.modify_reputation(neighbor.name, spread_amount)

                if spread_amount > 0:
                    template = random.choice(REPUTATION_SPREAD_POSITIVE)
                else:
                    template = random.choice(REPUTATION_SPREAD_NEGATIVE)

                events.append(WorldEvent(
                    category="reputation",
                    text=template.format(source=visited_name, target=neighbor.name),
                    neighborhood=visited_name,
                    reputation_change=spread_amount,
                    target_neighborhood=neighbor.name,
                ))

        return events

    def _npc_reactions(self, state: GameState, summary: DaySummary,
                       memory: MemoryManager) -> list[WorldEvent]:
        """NPCs react to today's encounters overnight."""
        events = []

        # Get today's memories for NPC reactions
        today_memories = memory.get_memories_for_day(state.day_of_week)

        for mem in today_memories:
            if not mem.npc_name:
                continue

            # 25% chance any NPC generates a reaction event
            if random.random() > 0.25:
                continue

            if mem.event_type.value == "conversion":
                template = random.choice(NPC_REACTION_POSITIVE)
                events.append(WorldEvent(
                    category="gossip",
                    text=template.format(npc=mem.npc_name),
                    neighborhood=mem.neighborhood,
                ))
            elif mem.event_type.value in ("rejection", "polite_exit"):
                # Only negative reaction if rejection (not polite exit)
                if mem.event_type.value == "rejection":
                    template = random.choice(NPC_REACTION_NEGATIVE)
                    events.append(WorldEvent(
                        category="gossip",
                        text=template.format(npc=mem.npc_name),
                        neighborhood=mem.neighborhood,
                        reputation_change=-1,
                    ))

        return events

    def _conversion_ripples(self, state: GameState, summary: DaySummary,
                            memory: MemoryManager) -> list[WorldEvent]:
        """Conversions create ripple effects in the community."""
        events = []

        if summary.conversions == 0:
            return events

        today_memories = memory.get_memories_for_day(state.day_of_week)

        for mem in today_memories:
            if mem.event_type.value != "conversion":
                continue
            if not mem.npc_name:
                continue

            # 40% chance a conversion creates a ripple
            if random.random() > 0.40:
                continue

            template = random.choice(CONVERSION_RIPPLE)
            events.append(WorldEvent(
                category="ripple",
                text=template.format(
                    npc=mem.npc_name,
                    neighborhood=mem.neighborhood,
                ),
                neighborhood=mem.neighborhood,
                reputation_change=1,
            ))

        return events

    def _community_chatter(self, state: GameState,
                           summary: DaySummary) -> list[WorldEvent]:
        """Random community events that make the world feel alive."""
        events = []

        # 40% chance of a community event each night
        if random.random() > 0.40:
            return events

        if not state.county:
            return events

        # Pick a random neighborhood and town
        town = random.choice(state.county.towns)
        neighborhood = random.choice(town.neighborhoods)

        template = random.choice(COMMUNITY_EVENTS)
        text = template.format(
            neighborhood=neighborhood.name,
            town=town.name,
        )

        events.append(WorldEvent(
            category="community",
            text=text,
            neighborhood=neighborhood.name,
        ))

        return events

    def _demon_ally_events(self, state: GameState) -> list[WorldEvent]:
        """Demon allies generate events overnight."""
        events = []

        if not state.demon_allies:
            return events

        # 50% chance of demon chatter per night when you have allies
        if random.random() > 0.50:
            return events

        if not state.county:
            return events

        town = random.choice(state.county.towns)
        neighborhood = random.choice(town.neighborhoods)

        template = random.choice(DEMON_ALLY_EVENTS)
        text = template.format(neighborhood=neighborhood.name)

        events.append(WorldEvent(
            category="demon",
            text=text,
            neighborhood=neighborhood.name,
        ))

        return events
