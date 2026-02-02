# Architecture Overview

Belen Torres: Preaching The Truth is a narrative-driven text-based simulation game built in Python with a JavaScript web port.

---

## Design Principles

1. **Emergent Narrative**: Story emerges from player choices via memory/narrative systems
2. **Data-Driven Content**: Dialogue, preachers, items are data, not hardcoded logic
3. **No External Dependencies**: Pure Python stdlib for maximum portability
4. **Procedural Generation**: World is fully random each playthrough
5. **Separation of Concerns**: Models, logic, UI, and narrative are cleanly separated

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           GAME ORCHESTRATOR                              │
│                              (game.py)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                         Main Game Loop                               ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            ││
│  │  │ Day Loop │→ │ Actions  │→ │  Visit   │→ │  Events  │            ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            ││
│  └──────────────────────────────────────────────────────────────────────┘│
│                                    │                                     │
│  ┌─────────────────────────────────┴─────────────────────────────────┐  │
│  │                        CONVERSATION ENGINE                         │  │
│  │                         (conversation.py)                          │  │
│  │  Opening → Objections → Responses → Resolution (convert/reject)   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│  ┌─────────────────────────────────┴─────────────────────────────────┐  │
│  │                        SUPPORTING SYSTEMS                          │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │Narrative │  │  Memory  │  │Reputation│  │  Items   │          │  │
│  │  │  Engine  │  │  System  │  │  Manager │  │  /Shop   │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴───────────────────────────────────┐
│                              DATA LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │   GameState  │  │   Models     │  │   Config     │                 │
│  │  (mutable)   │  │ (dataclass)  │  │ (constants)  │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │   Dialogue   │  │  Preachers   │  │    Names     │                 │
│  │   (data)     │  │   (data)     │  │ (generators) │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
└────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴───────────────────────────────────┐
│                           PRESENTATION LAYER                           │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                      Console UI (ui.py)                         │   │
│  │  Menus, Status Display, Conversation Rendering, Input Handling  │   │
│  └────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Module Structure

```
preaching/
├── __main__.py      # Entry point
├── __init__.py      # Module exports
│
├── game.py          # Main game orchestrator (750+ lines)
│                    # - Game loop, day management
│                    # - Action handling, location visits
│                    # - Preacher/religion selection
│
├── ui.py            # Console interface (900+ lines)
│                    # - Menu display, input validation
│                    # - Status bars, conversation rendering
│                    # - Cross-platform terminal handling
│
├── models.py        # Data structures (337 lines)
│                    # - GameState, NPC, Location
│                    # - Street, Neighborhood, Town, County
│                    # - World generation factory methods
│
├── conversation.py  # Dialogue engine (308 lines)
│                    # - ConversationState, ConversationEngine
│                    # - Interest tracking, tag matching
│                    # - Conversion/rejection resolution
│
├── dialogue.py      # Dialogue data (~16KB)
│                    # - PERSONALITIES, MOODS
│                    # - OPENERS, OBJECTIONS, RESPONSES
│                    # - Tag definitions, weakness mappings
│
├── narrative.py     # Story generation (530+ lines)
│                    # - Internal monologues
│                    # - Journal entries
│                    # - Contextual callbacks
│
├── memory.py        # Event tracking (350+ lines)
│                    # - Memory dataclass
│                    # - MemoryManager
│                    # - Event recording, querying
│
├── reputation.py    # Reputation system (130 lines)
│                    # - Per-neighborhood tracking
│                    # - Event-based changes
│
├── logic.py         # Game logic functions
│                    # - Conversion calculations
│                    # - Hunger mechanics
│                    # - Functional, side-effect free
│
├── items.py         # Item/shop system (249 lines)
│                    # - Food items, pamphlets
│                    # - Store inventory generation
│
├── events.py        # Random events
│                    # - Food donations
│                    # - Satanic Bible encounters
│                    # - Money donations
│
├── preachers.py     # Character definitions
│                    # - 7 preset preachers
│                    # - Stat bonuses, backstories
│
├── names.py         # Procedural generation
│                    # - Person, store, church names
│                    # - Street, town, county names
│
├── enums.py         # Type-safe enumerations
│                    # - Religion, Strategy, Weather
│                    # - LocationType
│
├── config.py        # Game constants
│                    # - Balance numbers
│                    # - Probabilities
│
└── version.py       # Version info
```

---

## Data Flow

```
User Input → UI → Game Loop → System (Conversation/Event/Shop) → GameState
                                         │
                                         ↓
                                   Memory Recording
                                         │
                                         ↓
                               Narrative Generation
                                         │
                                         ↓
                                    UI Rendering
```

### Detailed Flow: Conversation

```
1. Player selects "Visit Location" → House with NPC
2. UI displays NPC info (name, personality hint, mood)
3. Game creates ConversationState
4. ConversationEngine.apply_opener() → initial interest
5. LOOP:
   a. Engine.get_next_objection() → NPC challenge
   b. Engine.get_available_responses() → player options
   c. Player selects response
   d. Engine.apply_response() → interest change
   e. Check: interest > +50 (convert) or < -30 (reject)
6. Resolution:
   - Conversion: score++, reputation++, Memory recorded
   - Rejection: failed_attempts++, reputation--, Memory recorded
   - Polite Exit: Memory recorded
7. Narrative engine generates internal monologue
8. Check for random events (food donation, Satanic Bible)
```

---

## Key Technologies

| Layer | Technology | Why |
|-------|------------|-----|
| Language | Python 3.10+ | Type hints, dataclasses, modern features |
| Models | dataclasses | Clean, immutable-friendly data structures |
| Type Safety | Enum | Prevent invalid states |
| Build | PyInstaller | Single-file executables |
| CI/CD | GitHub Actions | Multi-platform builds |
| Distribution | itch.io + butler | Game-focused distribution |
| Web Port | Vanilla JavaScript | No dependencies, works everywhere |

---

## World Hierarchy

```
County (1)
├── Town (3)
│   ├── Neighborhood (2-3)
│   │   ├── Street (2-5)
│   │   │   ├── Location (3-6)
│   │   │   │   ├── House (70%) → 1-6 NPCs
│   │   │   │   ├── Store (12%) → 1 clerk + inventory
│   │   │   │   ├── Church (12%) → 3-8 NPCs + affiliation
│   │   │   │   └── Library (6%) → 1 librarian
```

All names procedurally generated. World created once at game start via `GameState.create_new_game()`.

---

## Cross-Platform Support

### Console

- **Screen clearing**: `os.system('clear')` (Unix) / `os.system('cls')` (Windows)
- **Colors**: Not used in base game (web version uses ANSI)
- **Input**: Standard `input()` with validation

### Web Version

Standalone JavaScript port in `docs/`:
- Full game state management
- Same conversation mechanics
- Responsive dark-themed UI
- No backend dependency

---

*See also: [Data Model](data-model.md) | [Conversation System](../systems/conversation.md)*
