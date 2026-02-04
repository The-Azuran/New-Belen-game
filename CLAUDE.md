# New Belen Game - AI Assistant Context

Quick reference for AI assistants working on this project.

**Last updated:** 2026-02-02

---

## What This Is

"Belen Torres: Preaching The Truth" - A narrative-driven door-to-door preaching simulation game set in 1990s suburban America.

**Author:** Rowan Valle (Valis) - Symbiont Systems LLC

**Tech Stack:**
- Python 3.10+ (main game, ~4,500 lines)
- JavaScript (web port, ~1,200 lines)
- PyInstaller (cross-platform builds)
- GitHub Actions (CI/CD to itch.io)

---

## Standing Orders

This project follows the universal standing orders at `~/.claude/STANDING-ORDERS.md`.

**Project-specific additions:**

- **Preserve existing behavior** - Don't break what works; game balance is fragile
- **Flag design uncertainty** - Game balance and narrative decisions need human judgment
- **No external dependencies** - Pure Python stdlib for portability

---

## Project Structure

```
New-Belen-game/
├── CLAUDE.md           # This file
├── preaching/          # Main Python game module
│   ├── game.py         # Main game loop
│   ├── ui.py           # Console interface
│   ├── models.py       # Data structures
│   ├── conversation.py # Dialogue engine
│   ├── dialogue.py     # Dialogue content
│   ├── narrative.py    # Story generation
│   ├── memory.py       # Event tracking
│   ├── reputation.py   # Reputation system
│   ├── logic.py        # Game logic
│   ├── items.py        # Shop/inventory
│   ├── events.py       # Random events
│   ├── preachers.py    # Character definitions
│   ├── names.py        # Procedural names
│   └── config.py       # Constants
├── docs/               # Web version
│   ├── index.html
│   ├── style.css
│   └── game.js
├── assets/             # Icons, desktop entry
└── .github/workflows/  # CI/CD
```

---

## Key Design Principles

1. **Emergent narrative** - Memory + narrative systems create personalized stories
2. **Data-driven content** - Dialogue, preachers, items are data, not hardcoded logic
3. **No external dependencies** - Pure Python stdlib for portability
4. **Procedural generation** - World is fully random each playthrough

---

*Standing orders adapted from Symbiont Systems methodology.*
