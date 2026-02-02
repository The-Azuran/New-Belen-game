# Future Expansion Ideas

Potential features and enhancements for future development.

---

## Priority: High (Low Effort, High Impact)

### Save/Load System

**Current state:** No persistence. Games must be completed in one session.

**Implementation:**
- Serialize `GameState` to JSON
- Add `save_game()` and `load_game()` methods
- Dataclass architecture makes this straightforward
- Store in user's home directory or game folder

**Benefits:**
- Players can resume campaigns
- Enables longer, more thoughtful play
- Standard expected feature

---

### Seeded World Generation

**Current state:** `random` module used without exposed seed.

**Implementation:**
- Add `seed` parameter to `GameState.create_new_game()`
- Call `random.seed(user_seed)` before world generation
- Display seed at game start for sharing

**Benefits:**
- Reproducible games for speedrunning
- Share interesting worlds with friends
- Debug specific scenarios

---

### More Dialogue Content

**Current state:** ~20 objections, ~20 responses.

**Implementation:**
- Expand `dialogue.py` with more entries
- No code changes needed (data-driven)
- Community contributions possible

**Content ideas:**
- More personality-specific objections
- Regional/cultural variants
- Seasonal content (Christmas, Easter)
- More NPC reactions

---

### Additional Preachers

**Current state:** 7 preset + custom.

**Implementation:**
- Add entries to `PREACHERS` list in `preachers.py`
- Balance new stat combinations
- Write compelling backstories

**Character ideas:**
- Historical figures (Martin Luther, etc.)
- Regional archetypes (Southern Baptist, etc.)
- Unlockable characters (based on achievements)
- Satirical characters

---

## Priority: Medium (Moderate Effort)

### Companion System

**Concept:** Recruit converted NPCs as traveling companions.

**Mechanics:**
- Certain NPCs offer to join after conversion
- Companions provide passive bonuses
- Can handle conversations autonomously (lower success rate)
- Unlock special dialogue options

**Implementation:**
- Add `Companion` dataclass
- Track in `GameState.companions`
- Modify conversation flow for companion interactions
- Add companion management UI

---

### Relationship Depth

**Concept:** Track individual NPC relationships across days.

**Mechanics:**
- Revisiting "polite exit" NPCs warms them up
- Multiple visits to same NPC builds relationship
- Some NPCs only convert after multiple visits
- Memory system already tracks NPC history

**Implementation:**
- Add `relationship_level` to NPC
- Modify conversation start based on history
- Add "revisit" action for known NPCs

---

### Rival Preachers

**Concept:** Other denominations competing in same neighborhoods.

**Mechanics:**
- Rival preachers work same territory
- They can convert NPCs before you reach them
- Spread negative reputation about you
- Can be converted themselves (boss encounters)

**Implementation:**
- Add `Rival` dataclass
- Simulate rival progress each day
- Add rival encounter events
- Modify NPC availability based on rival conversions

---

### Weather Events

**Concept:** Expanded weather system with events.

**Current:** Weather affects hunger rate only.

**Expansion ideas:**
- Storms lock you in current location
- Heat waves increase hunger faster
- Rain makes some NPCs more receptive (staying inside)
- Snow days change NPC availability

---

### Special Locations

**New location types:**

| Location | Mechanic |
|----------|----------|
| Community Center | Group preaching (higher risk/reward) |
| Park | Random NPC encounters |
| Hospital | Vulnerable but ethically complex |
| Coffee Shop | Multiple NPCs, relaxed atmosphere |
| Bus Stop | Captive audience, time pressure |

---

### Achievement System

**Concept:** Track milestones for replayability.

**Achievement ideas:**
- "Perfect Day" - 10+ conversions, no rejections
- "Diplomat" - Max reputation in all neighborhoods
- "Dark Path" - Complete Satanic ending
- "Pacifist" - Win without hostile encounters
- "Speedrunner" - Win in minimum days
- "Completionist" - Visit every location in county
- "Underdog" - Win as Brother Marcus with Custom religion

---

## Priority: Lower (High Effort)

### Branching Campaign

**Concept:** Story branches based on performance.

**Branch points:**
- Day 3: Church offers staff position (end early with modest score, or continue)
- Day 5: Scandal breaks (newspaper event affects all neighborhoods)
- Day 7: Multiple endings based on score, reputation, path

**Implementation:**
- Add story event system
- Track campaign state
- Write branching narrative content
- Multiple ending sequences

---

### NPC Schedules & Routines

**Concept:** NPCs move between locations by time of day.

**Schedule examples:**
- Morning: Adults at work, elderly at home
- Afternoon: Kids home from school, parents return
- Evening: Families together (harder but higher reward)

**Implementation:**
- Add time-of-day tracking
- NPC availability by schedule
- Location population varies by time

---

### Faction System

**Concept:** Churches and organizations with competing agendas.

**Factions:**
- Megachurch: Resources but demands loyalty
- Independent: Freedom but no support
- Secret cults: Hidden questlines
- Community groups: Secular alternatives

**Mechanics:**
- Faction reputation tracking
- Faction-specific quests
- Benefits and restrictions per faction

---

### Multiplayer (Async)

**Concept:** Shared competitive experience.

**Features:**
- Share world seeds and compare scores
- "Ghost" data - see where other players succeeded/failed
- Weekly challenges with leaderboards
- Persistent world state across players

---

### Modding Support

**Concept:** Externalize data files for community mods.

**Moddable content:**
- `preachers.json` - Custom characters
- `dialogue.json` - Dialogue packs
- `locations.json` - New location types
- `events.json` - Custom events

**Implementation:**
- JSON data loaders
- Mod directory scanning
- Merge logic for base + mod content

---

## Technical Improvements

### Mobile App

**Current:** Web version is responsive.

**Path forward:**
- Wrap with Capacitor or Cordova
- Publish to app stores
- Touch-optimized controls

---

### Accessibility

**Improvements:**
- Screen reader support
- High contrast mode
- Font size options
- Keyboard navigation (web version)

---

### Analytics (Optional)

**Track (anonymized):**
- Which personalities are too hard/easy
- Which preachers are most popular
- Where players quit
- Conversion rate distribution

**Purpose:** Balance tuning based on real data.

---

## Implementation Priority Matrix

| Feature | Effort | Impact | Priority |
|---------|--------|--------|----------|
| Save/Load | Low | High | **1** |
| Seeded Generation | Low | Medium | **2** |
| More Dialogue | Low | Medium | **3** |
| More Preachers | Low | Medium | **4** |
| Achievements | Medium | Medium | **5** |
| Relationship Depth | Medium | High | **6** |
| Companion System | Medium | High | **7** |
| Rival Preachers | Medium | High | **8** |
| Special Locations | Medium | Medium | **9** |
| Branching Campaign | High | High | **10** |
| NPC Schedules | High | Medium | **11** |
| Faction System | High | Medium | **12** |
| Modding Support | High | Medium | **13** |

---

---

## World Fleshing Research (2026-02-02)

Brainstormed ideas for making the world more immersive:

### Location Depth

**Houses:**
- Yard descriptions (toys = kids, garden = elderly, cars = working class)
- House condition hints at occupant mood/receptivity
- Seasonal decorations (Christmas lights, Halloween)
- "No Soliciting" signs (warning before knocking)

**Stores:**
- Clerk personalities affecting prices/availability
- Regulars you see repeatedly
- Bulletin boards with community info
- Store-specific events (sales, new stock)

**Churches:**
- Pastors with names and personalities
- Congregation events you can attend
- Potential allies or rivals
- Different service styles affecting approach

**Libraries:**
- Book club meetings
- Community events
- Librarian relationships
- Historical archives about the town

### NPC Relationships

**Family connections:**
- NPCs in same house are related
- Converting one family member affects others
- "My sister told me about you..."

**Neighborhood gossip:**
- Word spreads about you (good or bad)
- NPCs reference specific past encounters
- "I heard you helped Mrs. Garcia..."

**NPC schedules:**
- Same person at home morning, at store afternoon
- Catch someone at work vs at home = different mood

### World Events

**Daily happenings:**
- Local news (parade, accident, school event)
- Weather events (storm coming, heat wave)
- Community gatherings affecting NPC availability

**Week-long arcs:**
- Town festival building up
- Local controversy (new development, school board)
- Competing revival from another church

### Physical Atmosphere

**Street descriptions:**
- Tree-lined vs industrial vs suburban sprawl
- Condition (well-maintained, run-down, gentrifying)
- Traffic, noise, activity level

**Time of day flavor:**
- Morning: coffee smell, newspapers, joggers
- Afternoon: kids playing, lawn mowers
- Evening: dinner smells, TV glow, porch lights

**1990s period details:**
- Specific cars in driveways (minivans, Saturns)
- Yard sale signs
- Basketball hoops, trampolines
- Political yard signs

### Interconnected Systems

**Reputation ripple effects:**
- Convert someone important = bonus in whole neighborhood
- Upset someone connected = multiple doors close
- Churches talk to each other about you

**Economic layer:**
- Rich vs poor neighborhoods (different NPC concerns)
- Donation amounts vary by area
- Store prices vary by location

### Implementation Priority Suggestions

1. **Location descriptions/atmosphere** - Mostly narrative, low code effort
2. **NPC relationships/gossip** - Mechanical + narrative, medium effort
3. **Time-of-day system** - Significant mechanical change, high effort
4. **World events/arcs** - Content + mechanics, high effort

---

*See also: [Architecture Overview](../architecture/overview.md) | [Game Balance](../design/game-balance.md)*
