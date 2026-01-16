"""
Dialogue data for the conversation system.
All content is data-driven - add/remove entries without touching code.
"""

# =============================================================================
# PERSONALITIES - NPC personality types
# weak_to: tags that work well against this personality
# strong_against: tags that backfire against this personality
# =============================================================================
PERSONALITIES: dict[str, dict] = {
    "skeptic": {
        "name": "Skeptic",
        "description": "Needs evidence and logic",
        "weak_to": ["logical", "evidence", "respectful"],
        "strong_against": ["hellfire", "pushy", "emotional"],
        "opening_responses": [
            "What do you want?",
            "I'm listening... for now.",
            "This better be good.",
        ],
    },
    "seeker": {
        "name": "Seeker",
        "description": "Spiritually curious",
        "weak_to": ["spiritual", "personal", "community"],
        "strong_against": [],
        "opening_responses": [
            "Oh, interesting! Tell me more.",
            "I've been thinking about these things lately...",
            "Come in, come in!",
        ],
    },
    "lonely": {
        "name": "Lonely",
        "description": "Craves connection",
        "weak_to": ["community", "family", "friendly", "personal"],
        "strong_against": ["logical", "cold"],
        "opening_responses": [
            "Oh! A visitor! How nice!",
            "I don't get many visitors...",
            "Would you like some coffee?",
        ],
    },
    "busy": {
        "name": "Busy",
        "description": "No time for this",
        "weak_to": ["quick", "respectful"],
        "strong_against": ["long_winded", "pushy"],
        "opening_responses": [
            "I only have a minute.",
            "Make it quick.",
            "I'm in the middle of something.",
        ],
    },
    "hostile": {
        "name": "Hostile",
        "description": "Actively opposed",
        "weak_to": ["respectful", "humble"],
        "strong_against": ["pushy", "hellfire", "direct"],
        "opening_responses": [
            "Oh great, another one.",
            "Not interested.",
            "You people again?",
        ],
    },
    "devout_other": {
        "name": "Devout (Other Faith)",
        "description": "Strong in different beliefs",
        "weak_to": ["respectful", "common_ground"],
        "strong_against": ["pushy", "hellfire", "exclusive"],
        "opening_responses": [
            "I already have my faith, thank you.",
            "I respect your beliefs, but I have my own.",
            "My family has been [faith] for generations.",
        ],
    },
    "intellectual": {
        "name": "Intellectual",
        "description": "Loves debate",
        "weak_to": ["logical", "evidence", "debate"],
        "strong_against": ["simple", "emotional"],
        "opening_responses": [
            "Ah, a theological discussion? Interesting.",
            "I've read quite a bit on this topic.",
            "Let's hear your argument.",
        ],
    },
    "cynic": {
        "name": "Cynic",
        "description": "Distrusts institutions",
        "weak_to": ["personal", "humble", "authentic"],
        "strong_against": ["institutional", "pushy"],
        "opening_responses": [
            "What's the catch?",
            "Churches just want your money.",
            "I've seen too much hypocrisy.",
        ],
    },
}

# =============================================================================
# MOODS - Affect starting interest and patience
# =============================================================================
MOODS: dict[str, dict] = {
    "receptive": {
        "name": "Receptive",
        "interest_bonus": 15,
        "patience": 5,
        "visual_hint": "They seem friendly and open.",
    },
    "neutral": {
        "name": "Neutral",
        "interest_bonus": 0,
        "patience": 4,
        "visual_hint": "They regard you cautiously.",
    },
    "grumpy": {
        "name": "Grumpy",
        "interest_bonus": -10,
        "patience": 3,
        "visual_hint": "They look annoyed.",
    },
    "distracted": {
        "name": "Distracted",
        "interest_bonus": -5,
        "patience": 3,
        "visual_hint": "They seem preoccupied.",
    },
    "curious": {
        "name": "Curious",
        "interest_bonus": 10,
        "patience": 4,
        "visual_hint": "They look intrigued.",
    },
}

# =============================================================================
# OPENERS - Player's opening lines
# =============================================================================
OPENERS: list[dict] = [
    {
        "id": "friendly",
        "text": "Good morning! Lovely day, isn't it?",
        "tags": ["friendly", "soft", "small_talk"],
        "interest_base": 5,
    },
    {
        "id": "direct",
        "text": "Have you heard the good news?",
        "tags": ["direct", "spiritual"],
        "interest_base": 0,
    },
    {
        "id": "urgent",
        "text": "I need to talk to you about your eternal soul.",
        "tags": ["hellfire", "pushy", "urgent"],
        "interest_base": -5,
    },
    {
        "id": "quick",
        "text": "Got just a minute? This'll be quick, I promise.",
        "tags": ["quick", "respectful"],
        "interest_base": 5,
    },
    {
        "id": "humble",
        "text": "I hope I'm not bothering you. I just wanted to share something.",
        "tags": ["humble", "soft", "respectful"],
        "interest_base": 8,
    },
    {
        "id": "question",
        "text": "Have you ever wondered about the meaning of life?",
        "tags": ["spiritual", "personal", "philosophical"],
        "interest_base": 3,
    },
]

# =============================================================================
# OBJECTIONS - What NPCs say to push back
# =============================================================================
OBJECTIONS: list[dict] = [
    {
        "id": "busy",
        "text": "I'm really busy right now.",
        "good_responses": ["respect_time", "quick_point"],
        "personality_weight": {"busy": 3, "hostile": 1},
    },
    {
        "id": "not_interested",
        "text": "I'm not interested, sorry.",
        "good_responses": ["soft_persist", "leave_pamphlet", "respect_choice"],
        "personality_weight": {"hostile": 2, "skeptic": 1},
    },
    {
        "id": "own_beliefs",
        "text": "I have my own beliefs, thanks.",
        "good_responses": ["respect_beliefs", "common_ground", "curious_ask"],
        "personality_weight": {"devout_other": 3, "skeptic": 1},
    },
    {
        "id": "bad_experience",
        "text": "I had a bad experience with church.",
        "good_responses": ["empathy", "different_approach", "listen"],
        "personality_weight": {"cynic": 3, "hostile": 2},
    },
    {
        "id": "atheist",
        "text": "I don't believe in God.",
        "good_responses": ["respect_view", "logical_appeal", "community_secular"],
        "personality_weight": {"skeptic": 3, "intellectual": 2},
    },
    {
        "id": "seen_enough",
        "text": "I've heard it all before.",
        "good_responses": ["fresh_perspective", "personal_story", "humble_offer"],
        "personality_weight": {"cynic": 2, "intellectual": 1},
    },
    {
        "id": "money",
        "text": "You just want my money.",
        "good_responses": ["no_money", "authentic", "community_free"],
        "personality_weight": {"cynic": 3, "hostile": 1},
    },
    {
        "id": "hypocrites",
        "text": "Church is full of hypocrites.",
        "good_responses": ["agree_imperfect", "personal_journey", "humble"],
        "personality_weight": {"cynic": 3, "skeptic": 1},
    },
    {
        "id": "science",
        "text": "I believe in science, not religion.",
        "good_responses": ["both_compatible", "evidence_based", "respect_view"],
        "personality_weight": {"intellectual": 3, "skeptic": 2},
    },
    {
        "id": "curious",
        "text": "Hmm, tell me more...",
        "good_responses": ["share_story", "explain_faith", "invite"],
        "personality_weight": {"seeker": 3, "lonely": 2},
        "is_positive": True,
    },
]

# =============================================================================
# RESPONSES - Player's responses to objections
# =============================================================================
RESPONSES: list[dict] = [
    # Respectful responses
    {
        "id": "respect_time",
        "text": "I understand completely. Here's a pamphlet for when you have time.",
        "tags": ["respectful", "quick"],
        "interest_change": 5,
        "ends_conversation": True,
        "polite_exit": True,
    },
    {
        "id": "respect_choice",
        "text": "I respect that. Have a blessed day.",
        "tags": ["respectful", "humble"],
        "interest_change": 3,
        "ends_conversation": True,
        "polite_exit": True,
    },
    {
        "id": "respect_beliefs",
        "text": "I respect your beliefs. What faith are you, if you don't mind me asking?",
        "tags": ["respectful", "curious_ask", "common_ground"],
        "interest_change": 8,
    },
    {
        "id": "respect_view",
        "text": "That's a valid perspective. I used to think similarly.",
        "tags": ["respectful", "personal"],
        "interest_change": 6,
    },

    # Soft persistence
    {
        "id": "soft_persist",
        "text": "I felt that way too once. Would you give me just two minutes?",
        "tags": ["soft", "personal", "humble"],
        "interest_change": 4,
    },
    {
        "id": "leave_pamphlet",
        "text": "No problem! I'll just leave this here in case you're ever curious.",
        "tags": ["respectful", "quick"],
        "interest_change": 3,
        "ends_conversation": True,
        "polite_exit": True,
    },

    # Empathy responses
    {
        "id": "empathy",
        "text": "I'm really sorry to hear that. Not all churches are the same.",
        "tags": ["empathy", "personal", "humble"],
        "interest_change": 10,
    },
    {
        "id": "listen",
        "text": "Would you like to tell me what happened? I'm here to listen.",
        "tags": ["empathy", "personal"],
        "interest_change": 12,
    },
    {
        "id": "different_approach",
        "text": "Our community is different. We focus on love, not judgment.",
        "tags": ["community", "humble"],
        "interest_change": 8,
    },

    # Logical appeals
    {
        "id": "logical_appeal",
        "text": "Fair enough. Can I share some thoughts that made me reconsider?",
        "tags": ["logical", "respectful"],
        "interest_change": 5,
    },
    {
        "id": "evidence_based",
        "text": "There's actually some interesting historical evidence I could share.",
        "tags": ["logical", "evidence"],
        "interest_change": 6,
    },
    {
        "id": "both_compatible",
        "text": "Many scientists are believers too. They're not mutually exclusive.",
        "tags": ["logical", "respectful"],
        "interest_change": 7,
    },

    # Community appeals
    {
        "id": "community_secular",
        "text": "Even if you don't believe, our community does a lot of good locally.",
        "tags": ["community", "humble"],
        "interest_change": 6,
    },
    {
        "id": "community_free",
        "text": "We have free community dinners every week. No strings attached.",
        "tags": ["community", "humble", "no_pressure"],
        "interest_change": 8,
    },

    # Quick responses
    {
        "id": "quick_point",
        "text": "Just 30 seconds, I promise. One quick thought.",
        "tags": ["quick", "respectful"],
        "interest_change": 3,
    },

    # Personal story
    {
        "id": "personal_story",
        "text": "Let me tell you what faith did for me personally...",
        "tags": ["personal", "authentic"],
        "interest_change": 7,
    },
    {
        "id": "share_story",
        "text": "I'd love to share my journey with you.",
        "tags": ["personal", "spiritual"],
        "interest_change": 8,
    },

    # Addressing cynicism
    {
        "id": "no_money",
        "text": "I'm not here for money. I'm here because I care about people.",
        "tags": ["authentic", "humble"],
        "interest_change": 8,
    },
    {
        "id": "agree_imperfect",
        "text": "You're right, we're all imperfect. That's kind of the point, actually.",
        "tags": ["humble", "authentic", "common_ground"],
        "interest_change": 10,
    },
    {
        "id": "humble",
        "text": "I don't have all the answers. I'm just sharing what helped me.",
        "tags": ["humble", "personal", "authentic"],
        "interest_change": 9,
    },

    # Positive momentum
    {
        "id": "explain_faith",
        "text": "It's about finding peace and purpose. Let me explain...",
        "tags": ["spiritual", "personal"],
        "interest_change": 10,
    },
    {
        "id": "invite",
        "text": "Why don't you come to our Sunday service? No commitment.",
        "tags": ["community", "no_pressure"],
        "interest_change": 8,
    },

    # Aggressive (usually backfire)
    {
        "id": "pushy_persist",
        "text": "But your eternal soul is at stake!",
        "tags": ["hellfire", "pushy"],
        "interest_change": -10,
    },
    {
        "id": "guilt",
        "text": "Don't you want to be saved?",
        "tags": ["pushy", "hellfire"],
        "interest_change": -8,
    },
    {
        "id": "dismissive",
        "text": "You'll regret this when the time comes.",
        "tags": ["hellfire", "pushy", "threatening"],
        "interest_change": -15,
    },
]

# =============================================================================
# POSITIVE REACTIONS - What NPCs say when interested
# =============================================================================
POSITIVE_REACTIONS: list[str] = [
    "Hmm, that's actually interesting...",
    "I never thought of it that way.",
    "You know, you might have a point.",
    "Tell me more about that.",
    "That's different from what I expected.",
    "You seem genuine, I'll give you that.",
    "Maybe I've been too closed-minded.",
    "I appreciate you listening to me.",
]

# =============================================================================
# NEGATIVE REACTIONS - What NPCs say when annoyed
# =============================================================================
NEGATIVE_REACTIONS: list[str] = [
    "I think we're done here.",
    "Please leave me alone.",
    "I've heard enough.",
    "This isn't going anywhere.",
    "I need you to go now.",
    "You're wasting your time.",
]

# =============================================================================
# CONVERSION LINES - What NPCs say when converted
# =============================================================================
CONVERSION_LINES: list[str] = [
    "You know what? I'd like to learn more.",
    "Maybe I'll come to that service you mentioned.",
    "I think... I think you might be onto something.",
    "I've been searching for something. Maybe this is it.",
    "Alright, you've convinced me to give it a try.",
    "There's something different about you. I'm interested.",
]

# =============================================================================
# THRESHOLDS - Game balance constants
# Note: Pamphlet types are defined in items.py with proper dataclass structure
# =============================================================================
CONVERSION_THRESHOLD = 50      # Interest level needed to convert
REJECTION_THRESHOLD = -30      # Interest level that ends conversation
INTEREST_PER_GOOD_MATCH = 12   # Bonus for matching personality weakness
INTEREST_PER_BAD_MATCH = -8    # Penalty for matching personality strength
