"""Narrative engine for generating emergent story from game state and memories."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .memory import MemoryManager, Memory, DaySummary, EventType
    from .models import GameState, NPC


@dataclass
class NarrativeContext:
    """Current context for narrative generation."""
    day: int
    weather: str
    hunger: int
    money: int
    total_score: int
    satanic_score: int
    current_neighborhood: str
    rejection_streak: int
    conversion_streak: int
    reputation_in_area: int  # -100 to 100 scale


class NarrativeEngine:
    """Generates contextual narrative text from game state and memories."""

    def __init__(self, memory_manager: "MemoryManager") -> None:
        self.memory = memory_manager

    # === INTERNAL MONOLOGUE (Belen's thoughts) ===

    def get_approach_thought(self, context: NarrativeContext, npc: "NPC") -> Optional[str]:
        """Get Belen's internal thought when approaching someone."""
        thoughts = []

        # Check for previous encounters with this NPC (relationship depth)
        history = self.memory.get_npc_history(npc.name)
        if history:
            from .memory import EventType
            polite_exits = [m for m in history if m.event_type == EventType.POLITE_EXIT]
            rejections = [m for m in history if m.event_type == EventType.REJECTION]

            # Multiple polite conversations build warmth
            if len(polite_exits) >= 3:
                thoughts.append(f"You've had several good conversations with {npc.name}. They're warming up.")
            elif len(polite_exits) == 2:
                thoughts.append(f"{npc.name} has been polite twice now. You're building something here.")
            elif len(polite_exits) == 1:
                thoughts.append(f"{npc.name} was polite last time. Maybe they're warming up.")

            # Resistant NPCs with persistence
            if npc.resistant and len(history) >= 2:
                thoughts.append(f"{npc.name} is stubborn, but you've been patient. Maybe today.")
            elif npc.resistant and len(history) == 1:
                thoughts.append(f"{npc.name} resisted before, but you sense they might listen now.")

            # Multiple rejections
            if len(rejections) >= 2:
                thoughts.append(f"You've spoken to {npc.name} {len(rejections)} times. It never goes well.")
            elif len(rejections) == 1 and len(polite_exits) == 0:
                thoughts.append(f"You've spoken to {npc.name} before. It didn't go well.")

        # Rejection streak thoughts
        if context.rejection_streak >= 3:
            thoughts.extend([
                "Another door. Another chance for rejection.",
                "Three in a row. Is anyone listening today?",
                "You steel yourself. It has to get better.",
            ])

        # Hunger-based thoughts
        if context.hunger >= 70:
            thoughts.extend([
                "Your stomach aches. Focus.",
                "Almost too tired to care. Almost.",
                "One more conversation. Then you can rest.",
            ])
        elif context.hunger >= 50:
            thoughts.extend([
                "The hunger gnaws at you, but you push on.",
                "You could use a break, but souls don't save themselves.",
            ])

        # Weather-based thoughts
        if context.weather == "hot":
            thoughts.extend([
                "Sweat trickles down your back.",
                "The heat is oppressive, but your purpose is clear.",
            ])
        elif context.weather == "cold":
            thoughts.extend([
                "You pull your coat tighter.",
                "The cold bites, but your faith warms you.",
            ])

        # Reputation-based thoughts
        if context.reputation_in_area < -10:
            thoughts.extend([
                "You sense you're not welcome here anymore.",
                "The neighborhood watches. Remembers.",
            ])
        elif context.reputation_in_area > 15:
            thoughts.extend([
                "People here know you now. That helps.",
                "This neighborhood has been good to you.",
            ])

        # Personality-specific thoughts
        if npc.personality == "hostile":
            thoughts.append("Something in their posture warns you this won't be easy.")
        elif npc.personality == "seeker":
            thoughts.append("They seem... searching for something.")
        elif npc.personality == "lonely":
            thoughts.append("There's a sadness in their eyes.")

        # Money stress
        if context.money <= 2:
            thoughts.append("You need to eat soon. Maybe someone will donate today.")

        # Satanic path thoughts
        if context.satanic_score > 0 and context.satanic_score < 5:
            thoughts.extend([
                "Something feels different since that night.",
                "A shadow at the edge of your thoughts.",
            ])

        if thoughts:
            return random.choice(thoughts)
        return None

    def get_preacher_insight(
        self,
        preacher_id: str,
        personality_bonus: dict[str, float],
        npc_personality: str,
    ) -> Optional[str]:
        """Get preacher-specific observation based on their affinity with NPC personality.

        This creates a "skills as voices" effect where each preacher notices
        different things about the people they meet.
        """
        from .preachers import PREACHER_INSIGHTS

        # Get insights for this preacher
        preacher_insights = PREACHER_INSIGHTS.get(preacher_id, {})
        if not preacher_insights:
            return None

        # Check if preacher has affinity (positive or negative) for this personality
        if npc_personality not in personality_bonus:
            return None

        bonus = personality_bonus[npc_personality]
        insights = []

        if bonus > 0:
            # Positive affinity - preacher notices opportunity
            insights = preacher_insights.get("positive", {}).get(npc_personality, [])
        elif bonus < 0:
            # Negative affinity - preacher notices difficulty
            insights = preacher_insights.get("negative", {}).get(npc_personality, [])

        if insights:
            return random.choice(insights)
        return None

    def get_post_conversion_thought(self, context: NarrativeContext, npc: "NPC") -> Optional[str]:
        """Get Belen's thought after a successful conversion."""
        thoughts = [
            f"{npc.name} has seen the light.",
            "Another soul saved.",
            "This is why you do this.",
        ]

        # Check for patterns
        patterns = self.memory.get_recurring_patterns()

        if patterns["total_conversions"] == 1:
            thoughts = ["Your first. You'll never forget this feeling."]
        elif patterns["total_conversions"] == 5:
            thoughts.append("Five souls now. The work bears fruit.")
        elif patterns["total_conversions"] == 10:
            thoughts.append("Ten saved. You're making a difference.")

        # Breaking a rejection streak
        if context.rejection_streak >= 3:
            thoughts.extend([
                "Finally. After so many closed doors.",
                "Persistence pays off.",
                "You needed this.",
            ])

        # Conversion streak
        if context.conversion_streak >= 2:
            thoughts.extend([
                "Two in a row. You're on fire today.",
                "The Spirit is moving.",
            ])
        if context.conversion_streak >= 3:
            thoughts = ["Three! When has that ever happened?"]

        # Same personality type converted multiple times
        fav_converts = patterns.get("favorite_converts", {})
        if npc.personality and fav_converts.get(npc.personality, 0) >= 2:
            thoughts.append(f"You're getting good at reaching the {npc.personality} ones.")

        return random.choice(thoughts)

    def get_post_rejection_thought(self, context: NarrativeContext, npc: "NPC",
                                   was_aggressive: bool = False) -> Optional[str]:
        """Get Belen's thought after being rejected."""
        thoughts = [
            "Their door closes. You move on.",
            "Not everyone is ready.",
            "You tell yourself it's not personal.",
        ]

        if was_aggressive:
            thoughts.extend([
                "Maybe you pushed too hard.",
                "That could have gone better.",
                "The hellfire approach backfired. Again.",
            ])

        # Rejection streak
        if context.rejection_streak >= 3:
            thoughts.extend([
                f"That's {context.rejection_streak} now. Is something wrong with you?",
                "Another one. The doubt creeps in.",
                "Why won't anyone listen?",
            ])
        if context.rejection_streak >= 5:
            thoughts = [
                "What are you even doing out here?",
                "Five rejections. Maybe they're right to refuse.",
                "The silence after the slammed door feels louder each time.",
            ]

        # Hostile personality
        if npc.personality == "hostile":
            thoughts.append("Some people are just... hard.")
        elif npc.personality == "intellectual":
            thoughts.append("You didn't have answers for their questions.")

        # Low hunger/exhaustion
        if context.hunger >= 60:
            thoughts.append("Rejected. And you're so tired.")

        return random.choice(thoughts)

    def get_no_answer_thought(self, context: NarrativeContext) -> Optional[str]:
        """Get thought when nobody answers the door."""
        thoughts = [
            "No answer. Did they see you coming?",
            "The door stays closed.",
            "Maybe they're not home. Maybe.",
        ]

        if context.reputation_in_area < -5:
            thoughts.extend([
                "Word has spread about you here.",
                "They're home. They're just not answering for you.",
                "Your reputation precedes you.",
            ])

        doors_closed = len(self.memory.get_memories_with_tag("unwelcome"))
        if doors_closed >= 3:
            thoughts.append("How many doors have closed without opening?")

        return random.choice(thoughts)

    # === JOURNAL ENTRIES ===

    def generate_journal_entry(self, summary: "DaySummary") -> str:
        """Generate an end-of-day journal entry from the day's summary."""
        lines = []

        # Opening line based on overall day mood
        if "blessed" in summary.tags:
            lines.append(f"{summary.day_name} was a blessed day.")
        elif "fruitless" in summary.tags:
            lines.append(f"{summary.day_name} bore no fruit.")
        elif "difficult" in summary.tags:
            lines.append(f"{summary.day_name} tested my faith.")
        elif "exhausted" in summary.tags:
            lines.append(f"I pushed too hard on {summary.day_name}.")
        elif "successful" in summary.tags:
            lines.append(f"{summary.day_name} went well.")
        else:
            lines.append(f"{summary.day_name}.")

        # Weather note if harsh
        if summary.weather in ["hot", "cold"]:
            weather_notes = {
                "hot": "The heat was brutal today.",
                "cold": "The cold made every step harder.",
            }
            lines.append(weather_notes[summary.weather])

        # Conversion summary
        if summary.conversions > 0:
            if summary.conversions == 1:
                if summary.notable_npcs:
                    lines.append(f"I reached {summary.notable_npcs[0]} today.")
                else:
                    lines.append("One soul found the light.")
            else:
                lines.append(f"{summary.conversions} souls saved today.")
                if summary.notable_npcs:
                    names = ", ".join(summary.notable_npcs[:3])
                    lines.append(f"I'll remember: {names}.")

        # Rejection note
        if summary.rejections >= 3:
            lines.append(f"{summary.rejections} rejections. Each one stings.")
        elif summary.rejections > 0 and summary.conversions == 0:
            lines.append("Only closed doors today.")

        # Church experiences
        if summary.hostile_churches > 0:
            lines.append("Encountered hostility at a church. That always hurts the most.")
        if summary.friendly_churches > 0:
            lines.append("Found fellowship with believers today. It helped.")

        # Unwelcome
        if "unwelcome" in summary.tags:
            lines.append("Some places, people won't even open the door anymore.")

        # Resource notes
        if summary.money_earned > 0:
            lines.append(f"Received ${summary.money_earned} in donations. The Lord provides.")
        if "costly" in summary.tags:
            lines.append("Spent more than I received. Need to be careful.")

        # Satanic path
        if "dark_touched" in summary.tags:
            lines.append("Something strange happened today. I don't want to write about it.")

        # Exhaustion ending
        if summary.ended_hungry:
            lines.append("Couldn't go on. Had to stop early.")

        # Closing reflection
        closings = self._get_journal_closing(summary)
        if closings:
            lines.append("")
            lines.append(random.choice(closings))

        return "\n".join(lines)

    def _get_journal_closing(self, summary: "DaySummary") -> list[str]:
        """Get possible closing lines for journal based on day."""
        closings = []

        if "blessed" in summary.tags:
            closings.extend([
                "Tomorrow, I'll do even better.",
                "Days like this make it all worth it.",
                "Thank you, Lord.",
            ])
        elif "fruitless" in summary.tags and "rejection_heavy" in summary.tags:
            closings.extend([
                "Maybe tomorrow.",
                "Why do I keep doing this?",
                "They don't understand. They will.",
                "Rest now. Try again tomorrow.",
            ])
        elif "persecuted" in summary.tags:
            closings.extend([
                "Even believers can be cruel.",
                "Not all who claim faith have it.",
            ])
        elif "exhausted" in summary.tags:
            closings.extend([
                "I need to take better care of myself.",
                "Can't help anyone if I collapse.",
            ])
        else:
            closings.extend([
                "Another day done.",
                "Tomorrow is a new day.",
                "Onward.",
            ])

        return closings

    # === CONTEXTUAL NARRATIVE MOMENTS ===

    def get_neighborhood_return_narrative(self, neighborhood: str,
                                         reputation: int) -> Optional[str]:
        """Get narrative when returning to a neighborhood."""
        memories = self.memory.get_memories_for_neighborhood(neighborhood)
        if not memories:
            return None

        conversions = [m for m in memories if m.event_type.value == "conversion"]
        rejections = [m for m in memories if m.event_type.value == "rejection"]
        hostile = [m for m in memories if m.event_type.value == "hostile_church"]

        narratives = []

        if len(conversions) >= 2:
            narratives.append(f"You've had success here before. {len(conversions)} souls saved in this neighborhood.")
        elif len(rejections) >= 3 and len(conversions) == 0:
            narratives.append("This neighborhood has been nothing but closed doors.")

        if hostile:
            narratives.append("You remember the hostile church here. The sting hasn't faded.")

        if reputation < -10:
            narratives.append("The neighborhood seems to tense as you walk in.")
        elif reputation > 15:
            narratives.append("A few people wave. They know you here now.")

        if narratives:
            return random.choice(narratives)
        return None

    def get_encounter_callback(self, npc: "NPC", neighborhood: str) -> Optional[str]:
        """Check if this encounter connects to past memories."""
        callbacks = []

        # Same name as someone we met before
        all_memories = self.memory.memories
        same_name = [m for m in all_memories if m.npc_name == npc.name and m.neighborhood != neighborhood]
        if same_name:
            prev = same_name[0]
            callbacks.append(f"{npc.name}. Like the {npc.name} from {prev.neighborhood}.")

        # Same personality type we've struggled/succeeded with
        from .memory import EventType
        personality_history = [m for m in all_memories
                             if m.npc_personality == npc.personality
                             and m.event_type in [EventType.CONVERSION, EventType.REJECTION]]

        if personality_history:
            conversions = [m for m in personality_history if m.event_type == EventType.CONVERSION]
            rejections = [m for m in personality_history if m.event_type == EventType.REJECTION]

            if len(conversions) >= 2 and len(rejections) == 0:
                callbacks.append(f"The {npc.personality} type. You've had luck with them before.")
            elif len(rejections) >= 2 and len(conversions) == 0:
                callbacks.append(f"Another {npc.personality}. They're always the hardest for you.")

        if callbacks:
            return random.choice(callbacks)
        return None

    def get_weather_narrative(self, weather: str, day: int) -> str:
        """Get opening weather narrative for the day."""
        narratives = {
            "nice": [
                "A pleasant day. Small mercies.",
                "The weather is kind today.",
                "A gentle day for walking.",
            ],
            "hot": [
                "The sun beats down mercilessly.",
                "Heat radiates from the pavement.",
                "Already sweating before you start.",
            ],
            "cold": [
                "The cold bites at your fingers.",
                "Frost lingers on the lawns.",
                "A bitter wind cuts through your coat.",
            ],
        }

        # Check for weather patterns
        recent_days = [s for s in self.memory.day_summaries if s.day >= day - 2]
        same_weather_streak = sum(1 for s in recent_days if s.weather == weather)

        if same_weather_streak >= 2:
            if weather == "hot":
                return "Another scorching day. When will this heat break?"
            elif weather == "cold":
                return "Still cold. This weather is relentless."

        return random.choice(narratives.get(weather, narratives["nice"]))

    def get_money_narrative(self, money: int, context: NarrativeContext) -> Optional[str]:
        """Get narrative about money situation."""
        if money <= 0:
            return "Your pockets are empty. You'll need a donation today."
        elif money <= 3:
            return "Running low on funds. Enough for one meal, maybe."
        elif money >= 20:
            return None  # No comment when comfortable

        return None

    # === ENDING NARRATIVES ===

    def generate_ending_reflection(self, game_state: "GameState",
                                   final_patterns: dict) -> str:
        """Generate final reflection based on full playthrough."""
        lines = []

        total_conversions = final_patterns.get("total_conversions", 0)
        total_rejections = final_patterns.get("total_rejections", 0)
        satanic_touches = final_patterns.get("satanic_touches", 0)

        # Opening based on overall success
        if total_conversions >= 15:
            lines.append("A week of triumphs.")
            lines.append(f"{total_conversions} souls found the light through your words.")
        elif total_conversions >= 8:
            lines.append("A solid week of work.")
            lines.append(f"{total_conversions} people heard the message and believed.")
        elif total_conversions >= 3:
            lines.append("Every soul matters.")
            lines.append(f"You reached {total_conversions} people this week.")
        elif total_conversions > 0:
            lines.append("A difficult week.")
            lines.append(f"Only {total_conversions} conversion{'s' if total_conversions > 1 else ''}. But that's enough.")
        else:
            lines.append("A week of closed doors.")
            lines.append("No one converted. But you tried.")

        # Rejection reflection
        if total_rejections >= 15:
            lines.append(f"{total_rejections} rejections. Each one a small death.")
        elif total_rejections >= 8:
            lines.append("The rejections were hard, but you persisted.")

        # Satanic path hint
        if satanic_touches > 0 and satanic_touches < 5:
            lines.append("")
            lines.append("And then there were the strange moments...")
            lines.append("Best not to dwell on those.")

        # Favorite convert personality
        fav_converts = final_patterns.get("favorite_converts", {})
        if fav_converts:
            best_type = max(fav_converts.items(), key=lambda x: x[1])
            if best_type[1] >= 2:
                lines.append(f"You seemed to connect best with the {best_type[0]} type.")

        # Closing
        lines.append("")
        if total_conversions >= 10:
            lines.append("You've made a difference here.")
        elif total_conversions >= 5:
            lines.append("Not bad for a week's work.")
        elif total_conversions > 0:
            lines.append("Small victories are still victories.")
        else:
            lines.append("Maybe this isn't your calling. Or maybe next week will be different.")

        return "\n".join(lines)
