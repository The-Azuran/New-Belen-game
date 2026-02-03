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
            "Let me guess. You want to save my soul.",
            "I've debunked three of you this month already.",
            "Alright, let's hear your pitch.",
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
            "You know, I was just reading about this.",
            "Perfect timing. I've had questions.",
            "I've been feeling... drawn to something. I don't know what.",
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
            "Please, come in. It's been so quiet.",
            "My cat and I were just settling in. Join us?",
            "It's nice to have someone to talk to.",
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
            "The roast is in the oven. Talk fast.",
            "I've got a call in five minutes.",
            "Can you give me the short version?",
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
            "I have a sign that says 'No Solicitors' for a reason.",
            "Whatever you're selling, I'm not buying.",
            "Don't you have somewhere else to be?",
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
            "I'm quite content with my spiritual path.",
            "We probably worship the same God, you know.",
            "I'm sure you mean well, but I'm settled in my beliefs.",
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
            "Have you read Hitchens? Dawkins?",
            "I hope you've done your homework.",
            "Finally, someone I can have a real conversation with.",
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
            "Let me guess - you need donations.",
            "I trust organized religion about as far as I can throw it.",
            "What's your angle here?",
        ],
    },
    "grieving": {
        "name": "Grieving",
        "description": "Processing loss",
        "weak_to": ["empathy", "community", "personal"],
        "strong_against": ["pushy", "hellfire", "quick"],
        "opening_responses": [
            "I'm not really in the mood for visitors...",
            "It's been a hard week.",
            "I suppose you can come in. Nothing else matters anyway.",
            "Sorry, I'm... I'm not myself today.",
            "You'll have to forgive me. Things have been difficult.",
            "I don't know why I answered the door.",
        ],
    },
    "parent": {
        "name": "Busy Parent",
        "description": "Overwhelmed with kids",
        "weak_to": ["quick", "family", "community"],
        "strong_against": ["long_winded", "pushy"],
        "opening_responses": [
            "Kids, get back here! Sorry, what?",
            "I've got about two minutes before someone needs a snack.",
            "Uh huh, uh huh... TYLER PUT THAT DOWN!",
            "Hold on - NO RUNNING WITH SCISSORS!",
            "You have thirty seconds. The baby's napping.",
            "If this is quick, I'm listening. If not, try next decade.",
        ],
    },
    "former_believer": {
        "name": "Former Believer",
        "description": "Left the faith years ago",
        "weak_to": ["personal", "humble", "no_pressure"],
        "strong_against": ["hellfire", "institutional", "pushy"],
        "opening_responses": [
            "I used to be just like you, you know.",
            "Been there, done that, got the t-shirt.",
            "Look, I know the whole playbook. Save your breath.",
            "I gave twenty years to the church. That's enough.",
            "You can't tell me anything I don't already know.",
            "I've read every apologetics book. None of it holds up.",
        ],
    },
    "elderly_religious": {
        "name": "Devout Elder",
        "description": "Deep in their own tradition",
        "weak_to": ["respectful", "common_ground"],
        "strong_against": ["hellfire", "pushy", "exclusive"],
        "opening_responses": [
            "Oh dear, another one? Come in, I'll make tea.",
            "I've had my faith for 60 years. What could you tell me?",
            "You remind me of myself, once upon a time.",
            "My pastor wouldn't approve of me talking to you, but...",
            "I've seen missionaries come and go. What makes you different?",
            "At my age, I'm set in my ways. But I do enjoy the company.",
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
    "sleepy": {
        "name": "Sleepy",
        "interest_bonus": -5,
        "patience": 2,
        "visual_hint": "They look like they just woke up from a nap.",
    },
    "cheerful": {
        "name": "Cheerful",
        "interest_bonus": 8,
        "patience": 5,
        "visual_hint": "They seem to be in a great mood today.",
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
    {
        "id": "community_event",
        "text": "We're having a potluck this Saturday. Would you be interested?",
        "tags": ["community", "friendly", "no_pressure"],
        "interest_base": 7,
    },
    {
        "id": "testimony_hook",
        "text": "Can I tell you about the strangest thing that ever happened to me?",
        "tags": ["personal", "authentic", "spiritual"],
        "interest_base": 6,
    },
    {
        "id": "philosophical",
        "text": "Do you ever wonder what happens after we die?",
        "tags": ["spiritual", "philosophical", "personal"],
        "interest_base": 4,
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
    {
        "id": "lost_someone",
        "text": "I prayed when my mother was dying. Nobody answered.",
        "good_responses": ["empathy", "listen", "grieve_with"],
        "personality_weight": {"grieving": 3, "cynic": 2},
    },
    {
        "id": "kids_busy",
        "text": "Look, I've got three kids screaming in there...",
        "good_responses": ["respect_time", "quick_point", "parenting_solidarity"],
        "personality_weight": {"parent": 3, "busy": 2},
    },
    {
        "id": "tried_before",
        "text": "I was a believer for twenty years. I know how this ends.",
        "good_responses": ["listen", "personal_story", "former_believer_relate"],
        "personality_weight": {"former_believer": 3, "cynic": 1},
    },
    # --- Intellectual/Philosophical objections ---
    {
        "id": "theodicy",
        "text": "If God is good, why do bad things happen to good people?",
        "good_responses": ["empathy", "humble", "listen", "mystery_acknowledge"],
        "personality_weight": {"intellectual": 3, "grieving": 2, "skeptic": 2},
    },
    {
        "id": "many_religions",
        "text": "Which God? There are thousands of religions. Why is yours right?",
        "good_responses": ["respect_beliefs", "humble", "personal_story", "common_ground"],
        "personality_weight": {"intellectual": 3, "skeptic": 2, "devout_other": 1},
    },
    {
        "id": "coping_mechanism",
        "text": "Religion is just a coping mechanism. A crutch for the weak.",
        "good_responses": ["agree_imperfect", "humble", "logical_appeal", "authentic"],
        "personality_weight": {"intellectual": 2, "skeptic": 3, "cynic": 2},
    },
    {
        "id": "contradictions",
        "text": "I've read the Bible. It contradicts itself constantly.",
        "good_responses": ["evidence_based", "humble", "curious_ask", "listen"],
        "personality_weight": {"intellectual": 3, "skeptic": 2, "former_believer": 2},
    },
    {
        "id": "philosophical",
        "text": "I studied philosophy. The logical arguments for God just don't hold up.",
        "good_responses": ["logical_appeal", "evidence_based", "humble", "respect_view"],
        "personality_weight": {"intellectual": 3, "skeptic": 2},
    },
    # --- Personal/Emotional objections ---
    {
        "id": "spouse_left",
        "text": "My spouse just left me. I can't think about anything else right now.",
        "good_responses": ["empathy", "listen", "grieve_with", "respect_time"],
        "personality_weight": {"grieving": 3, "busy": 1},
    },
    {
        "id": "unanswered_prayers",
        "text": "I prayed every day for years. Nothing ever changed.",
        "good_responses": ["empathy", "listen", "humble", "personal_story"],
        "personality_weight": {"former_believer": 3, "grieving": 2, "cynic": 2},
    },
    {
        "id": "forced_as_child",
        "text": "My parents forced religion on me. I'm done with all of it.",
        "good_responses": ["empathy", "different_approach", "no_pressure_offer", "listen"],
        "personality_weight": {"former_believer": 3, "hostile": 2, "cynic": 1},
    },
    {
        "id": "trauma",
        "text": "Something happened to me in a church. I'd rather not talk about it.",
        "good_responses": ["empathy", "respect_choice", "listen", "different_approach"],
        "personality_weight": {"hostile": 2, "former_believer": 2, "grieving": 2},
    },
    # --- Practical/Cynical objections ---
    {
        "id": "work_sundays",
        "text": "I work Sundays. Church just isn't practical for me.",
        "good_responses": ["community_free", "quick_point", "flexible_offer", "respect_time"],
        "personality_weight": {"busy": 3, "cynic": 1},
    },
    {
        "id": "happy_as_is",
        "text": "I'm happy the way I am. Why would I change?",
        "good_responses": ["respect_view", "curious_ask", "humble", "no_pressure_offer"],
        "personality_weight": {"skeptic": 2, "hostile": 1, "busy": 1},
    },
    {
        "id": "cult_concern",
        "text": "How do I know you're not some kind of cult?",
        "good_responses": ["no_money", "authentic", "humble", "community_free"],
        "personality_weight": {"cynic": 3, "skeptic": 2, "intellectual": 1},
    },
    # --- Hostile/Dismissive objections ---
    {
        "id": "colonial_history",
        "text": "Missionaries destroyed my ancestors' culture. Why should I listen to you?",
        "good_responses": ["empathy", "humble", "listen", "agree_imperfect"],
        "personality_weight": {"hostile": 3, "intellectual": 2, "cynic": 2},
    },
    {
        "id": "spiritual_not_religious",
        "text": "I'm spiritual, but not religious. Organized religion ruins everything.",
        "good_responses": ["respect_view", "common_ground", "humble", "personal_story"],
        "personality_weight": {"seeker": 2, "cynic": 2, "former_believer": 1},
    },
    {
        "id": "politics",
        "text": "Churches are too political these days. I want no part of it.",
        "good_responses": ["agree_imperfect", "different_approach", "humble", "community_free"],
        "personality_weight": {"cynic": 3, "intellectual": 1, "former_believer": 1},
    },
    # --- Softer/Curious objections (positive momentum) ---
    {
        "id": "tell_me_more",
        "text": "I'm listening. Go on...",
        "good_responses": ["share_story", "explain_faith", "personal_story"],
        "personality_weight": {"seeker": 3, "lonely": 2, "curious": 1},
        "is_positive": True,
    },
    {
        "id": "genuine_interest",
        "text": "You seem different from the others who come by. What's your story?",
        "good_responses": ["personal_story", "share_story", "authentic"],
        "personality_weight": {"seeker": 2, "lonely": 2, "intellectual": 1},
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

    # New responses for new personalities
    {
        "id": "grieve_with",
        "text": "I'm so sorry. Sometimes there are no words. Would you like to talk?",
        "tags": ["empathy", "personal", "humble"],
        "interest_change": 12,
    },
    {
        "id": "parenting_solidarity",
        "text": "I totally get it. Here's a flyer - no pressure, whenever you have time.",
        "tags": ["respectful", "quick", "family"],
        "interest_change": 6,
        "ends_conversation": True,
        "polite_exit": True,
    },
    {
        "id": "former_believer_relate",
        "text": "What made you leave, if you don't mind me asking?",
        "tags": ["empathy", "curious_ask", "personal"],
        "interest_change": 8,
    },
    # --- Probing/Listening responses ---
    {
        "id": "curious_ask",
        "text": "What happened, if you don't mind sharing?",
        "tags": ["empathy", "curious_ask", "personal"],
        "interest_change": 9,
    },
    {
        "id": "when_did_start",
        "text": "That sounds painful. When did this start?",
        "tags": ["empathy", "personal"],
        "interest_change": 8,
    },
    {
        "id": "validate_feelings",
        "text": "I hear you. A lot of people feel that way.",
        "tags": ["humble", "empathy"],
        "interest_change": 7,
    },
    {
        "id": "mystery_acknowledge",
        "text": "I don't have easy answers. Some things are a mystery, even to me.",
        "tags": ["humble", "authentic", "personal"],
        "interest_change": 10,
    },
    {
        "id": "silence_listen",
        "text": "...",
        "tags": ["empathy", "humble"],
        "interest_change": 6,
        "description": "Sometimes silence says more than words.",
    },
    # --- Bridge-building responses ---
    {
        "id": "common_ground",
        "text": "We have more in common than you might think.",
        "tags": ["common_ground", "humble", "friendly"],
        "interest_change": 7,
    },
    {
        "id": "not_here_to_argue",
        "text": "I'm not here to argue or convince you. Just to listen.",
        "tags": ["humble", "no_pressure", "empathy"],
        "interest_change": 9,
    },
    {
        "id": "doubts_valid",
        "text": "Your doubts are valid. I've had them too.",
        "tags": ["authentic", "personal", "humble"],
        "interest_change": 10,
    },
    {
        "id": "not_like_others",
        "text": "I know you've probably met pushy religious types before. I try not to be.",
        "tags": ["humble", "authentic", "different"],
        "interest_change": 8,
    },
    {
        "id": "authentic",
        "text": "I'm not here with a script. I'm just a person who found something meaningful.",
        "tags": ["authentic", "personal", "humble"],
        "interest_change": 9,
    },
    # --- Tactful retreat responses ---
    {
        "id": "wrong_time",
        "text": "I can see this isn't the right time. God bless you.",
        "tags": ["respectful", "quick", "humble"],
        "interest_change": 5,
        "ends_conversation": True,
        "polite_exit": True,
    },
    {
        "id": "leave_card",
        "text": "I'll leave you my card. No pressure, no follow-up calls.",
        "tags": ["respectful", "no_pressure", "quick"],
        "interest_change": 4,
        "ends_conversation": True,
        "polite_exit": True,
    },
    {
        "id": "no_pressure_offer",
        "text": "There's no pressure here. If you ever want to talk, I'm around.",
        "tags": ["no_pressure", "humble", "friendly"],
        "interest_change": 6,
        "ends_conversation": True,
        "polite_exit": True,
    },
    {
        "id": "flexible_offer",
        "text": "We have weeknight meetings too, if Sundays don't work.",
        "tags": ["community", "practical", "helpful"],
        "interest_change": 7,
    },
    # --- Addressing specific concerns ---
    {
        "id": "church_hurt",
        "text": "What happened to you shouldn't have happened. I'm sorry.",
        "tags": ["empathy", "humble", "personal"],
        "interest_change": 11,
    },
    {
        "id": "not_about_control",
        "text": "Real faith isn't about control. It's about freedom.",
        "tags": ["spiritual", "authentic", "humble"],
        "interest_change": 8,
    },
    {
        "id": "acknowledge_history",
        "text": "You're right. The church has done terrible things. I won't defend that.",
        "tags": ["humble", "authentic", "common_ground"],
        "interest_change": 10,
    },
    {
        "id": "personal_journey",
        "text": "My journey isn't yours. I just want to share what helped me.",
        "tags": ["personal", "humble", "no_pressure"],
        "interest_change": 8,
    },
    {
        "id": "fresh_perspective",
        "text": "Maybe I can offer a different angle than what you've heard before?",
        "tags": ["humble", "curious_ask"],
        "interest_change": 6,
    },
    {
        "id": "humble_offer",
        "text": "I don't have all the answers, but I found something worth sharing.",
        "tags": ["humble", "authentic", "personal"],
        "interest_change": 8,
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
    # --- New positive reactions ---
    "Go on...",
    "I hadn't considered that before.",
    "You're not like the others who come by.",
    "My neighbor mentioned your church, actually.",
    "I suppose one visit couldn't hurt.",
    "That... actually makes sense.",
    "You really believe all this, don't you?",
    "Huh. That's a new one.",
    "At least you're honest about it.",
    "I can respect that approach.",
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
    # --- New negative reactions ---
    "I really don't have time for this.",
    "You're not going to change my mind.",
    "I'm sorry, but no.",
    "Maybe some other time.",
    "Look, I appreciate the effort, but...",
    "This conversation is over.",
    "I think you should go.",
    "That's not going to work on me.",
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
    # --- New conversion lines ---
    "Something about you feels... different.",
    "My mother would have liked you. Alright, I'll come.",
    "One Sunday. That's all I'm promising.",
    "I don't know why, but I trust you.",
    "Fine. But only because you actually listened to me.",
    "You caught me at the right time, I guess.",
    "I've been feeling lost lately. Maybe this is a sign.",
    "Okay. But if it's weird, I'm leaving.",
]

# =============================================================================
# THRESHOLDS - Game balance constants
# Note: Pamphlet types are defined in items.py with proper dataclass structure
# =============================================================================
CONVERSION_THRESHOLD = 50      # Interest level needed to convert
REJECTION_THRESHOLD = -30      # Interest level that ends conversation
INTEREST_PER_GOOD_MATCH = 12   # Bonus for matching personality weakness
INTEREST_PER_BAD_MATCH = -8    # Penalty for matching personality strength
