# Game Balance

Reference for all balance-affecting numbers and their rationale.

---

## Conversion Rates

Base conversion rates by religion:

| Religion | Base Rate | Notes |
|----------|-----------|-------|
| Evangelist | 30% | Default, balanced |
| Mormon | 25% | Slightly harder |
| Jehovah's Witness | 20% | Harder, realistic door-to-door |
| Custom | 15% | Challenge mode |
| **Satanic** | **50%** | Hidden path, reward for discovery |

### Conversion Modifiers

| Source | Modifier |
|--------|----------|
| Preacher bonus | -5% to +10% |
| Pocket Bible | +5% permanent |
| Pamphlet boost | +10% for 5 encounters |
| Satanic ally | +15% per ally met |
| Friendly church | +15% in neighborhood |
| Hostile church | -10% in neighborhood |
| NPC already converted in location | Multiplier based on % converted |

### Effective Caps

- Maximum conversion rate: 95% (config)
- Minimum: No floor (can be very low)

---

## Hunger System

### Hunger Gain Per Conversation

| Weather | Base Gain |
|---------|-----------|
| Nice | 10 |
| Hot | 15 |
| Cold | 15 |

**Preacher modifier:** `hunger_gain * preacher_hunger_rate`

| Preacher | Hunger Rate | Effective (Nice) |
|----------|-------------|------------------|
| Titi Olga | 0.75x | 7-8 |
| Joel Prosperity | 0.80x | 8 |
| Brother Marcus | 0.85x | 8-9 |
| Sister Joyce | 0.90x | 9 |
| Default/Custom | 1.0x | 10 |
| Belen Torres | 1.1x | 11 |
| Billy Graham Jr. | 1.1x | 11 |
| Dr. Scott Johnson | 1.2x | 12 |

### Hunger Cap

- **Max hunger:** 100
- Reaching 100 ends the day (too exhausted to continue)

### Hunger Reduction (Food)

| Item | Reduction | Cost | Value Ratio |
|------|-----------|------|-------------|
| Candy Bar | 10 | $2 | 5 points/$1 |
| Chips | 10 | $3 | 3.3 points/$1 |
| Hot Dog | 20 | $4 | 5 points/$1 |
| Sandwich | 20 | $5 | 4 points/$1 |
| Burrito | 35 | $6 | 5.8 points/$1 |
| Fried Chicken | 35 | $8 | 4.4 points/$1 |

**Best value:** Microwave Burrito (5.8 hunger/$1)

---

## Economy

### Starting Resources

| Resource | Base | Best Preacher | Worst Preacher |
|----------|------|---------------|----------------|
| Money | $10 | $60 (Joel) | $0 (Marcus) |

### Income Sources

| Source | Amount | Probability |
|--------|--------|-------------|
| Money donation | $1-5 | 30% per conversion |
| Sunday offering | +$10 | 100% (if Sunday) |

### Expected Income Per Day

Assuming 5 conversations, 30% conversion rate:
- Conversions: ~1.5
- Money donations: ~0.45 (30% of 1.5)
- Expected income: ~$1.35/day (average $3 per donation)
- Sunday: +$10

### Expense Analysis

With base $10 + average $1.35/day over 7 days:
- Total: ~$19.50

Possible purchases:
- ~3-4 meals throughout the week, OR
- 1 Pocket Bible + 1 cheap meal, OR
- 2-3 pamphlets + 1 meal

---

## Reputation System

### Thresholds

| Level | Value | Door Open % | Interest Bonus |
|-------|-------|-------------|----------------|
| Beloved | +30 | 100% | +10 |
| Friendly | +15 | 100% | +5 |
| Neutral | 0 | 100% | 0 |
| Suspicious | -10 | 100% | -5 |
| Hostile | -20 | 80% | -10 |
| Hated | Below -20 | 50% | -10 |

### Reputation Changes

| Event | Change | Net Effect |
|-------|--------|------------|
| Conversion | +2 | Positive |
| Polite exit | 0 | Neutral |
| Rejection | -1 | Slightly negative |
| Aggressive fail | -3 | Very negative |
| Hostile church | -2 | Negative |

### Reputation Math

To reach "Beloved" (+30) from neutral:
- Need 15 conversions with no failures, OR
- 20 conversions with 10 rejections, OR
- 30+ conversations with mixed results

To reach "Hated" (-20) from neutral:
- 20 rejections, OR
- 7 aggressive failures, OR
- 10 hostile church encounters

---

## Conversation Interest

### Starting Interest

| Factor | Effect |
|--------|--------|
| Receptive mood | +15 |
| Curious mood | +10 |
| Neutral mood | 0 |
| Distracted mood | -5 |
| Grumpy mood | -10 |
| Reputation bonus | -10 to +10 |
| Preacher personality match | -5 to +10 |
| Resistant NPC | -25 |

### Interest Thresholds

| Threshold | Value | Outcome |
|-----------|-------|---------|
| Conversion | +50 | NPC accepts |
| Rejection | -30 | NPC shuts door |

### Interest Per Response

| Match Type | Change |
|------------|--------|
| Good tag match | +10 per tag |
| Bad tag match | -10 per tag |
| Base response | Varies by response |

### Conversation Length

**Patience by mood:**

| Mood | Patience (turns) |
|------|------------------|
| Receptive | 5 |
| Curious | 4 |
| Neutral | 4 |
| Distracted | 3 |
| Grumpy | 3 |

If patience runs out before threshold: **polite exit** (no reputation penalty).

---

## Church Mechanics

### Friendly Church Effects

- +15% conversion bonus in neighborhood
- Positive interaction, no hunger cost

### Hostile Church Effects

- -10% conversion bonus in neighborhood
- -2 reputation
- +10 hunger (chased out)

### Church Affiliation

| Affiliation | Player Match | Result |
|-------------|--------------|--------|
| Same as player | Friendly | +15% bonus |
| Different | Hostile | -10% penalty, chased |
| Non-denominational | Friendly | +15% bonus |
| Satanic (1% spawn) | Satanic player only | Friendly |

---

## Time Economy

### Game Length

- 7 days total
- Each day ends at 100 hunger

### Conversations Per Day

With nice weather (10 hunger/conversation):
- Max theoretical: 10 conversations
- Realistic (some hunger events): 6-8 conversations
- With harsh weather (15 hunger): 4-6 conversations

### Total Game Conversations

- Theoretical max: ~70 (10/day × 7 days)
- Realistic estimate: 40-50 conversations
- At 30% conversion: ~12-15 conversions expected

---

## Hidden Mechanics

### Satanic Path Discovery

- Requires failed conversation (bad response)
- 10% chance of special event
- 50% of those: Satanic Bible thrown
- Player chooses to accept

**Expected attempts to discover:** ~20 failures (1/(0.1 × 0.5))

### Satanic Victory

- Requires 10+ conversions as Satanic
- With 50% base rate + ally bonuses, achievable in ~3-4 days

### Resistant NPCs

- 50% of NPCs are secretly resistant (cannot convert)
- -25 starting interest penalty
- -1 patience
- Library research reveals resistance status

---

## Difficulty Analysis

### Easiest Configuration

- Preacher: Titi Olga (+8% conversion, 0.75x hunger, +$30)
- Religion: Evangelist (30% base)
- Strategy: Target seekers and lonely NPCs

**Effective rate:** ~38% + pamphlet bonuses + church bonuses

### Hardest Configuration

- Preacher: Brother Marcus (-10 reputation, -$10 money)
- Religion: Custom (15% base)
- Hostile neighborhoods from start

**Effective rate:** ~15%, doors may not open, starting broke

---

*See also: [Preachers](../systems/preachers.md) | [Conversation System](../systems/conversation.md)*
