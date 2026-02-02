# New Belen Game - AI Assistant Context

Quick reference and standing orders for AI assistants working on this project.

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

Based on lessons from prior projects and AI-assisted development best practices.

### 1. Context First, Code Second

Before writing any code:

1. **Understand the codebase** - Know what exists before adding
2. **Read existing modules** - Check patterns and conventions in `preaching/`
3. **Check the architecture** - Understand how components interact

> Don't reinvent what's already there. Extend, don't duplicate.

### 2. Plan Before Implementing

For any non-trivial task:

1. **State what you understand** - Summarize the task back
2. **Identify the approach** - Which modules, what changes, what outputs
3. **Note risks/edge cases** - Breaking changes, balance implications
4. **Get approval** - Present plan before executing

### 3. Small, Testable Chunks

Game code can be complex. Keep changes manageable:

1. **One feature per change** - Atomic, focused modifications
2. **Verify changes work** - Test before moving on
3. **Preserve existing behavior** - Don't break what works

> Large changes are hard to debug when game logic fails silently.

### 4. Document Changes

Track what's modified:

1. **Note what changed** - Which files, what functionality
2. **Explain why** - What problem does this solve?
3. **Version outputs** - Use meaningful commit messages

### 5. Human Accountability

You are an "over-confident pair programmer prone to mistakes":

1. **Flag uncertainty** - Especially about game balance and design decisions
2. **Explain your reasoning** - Don't just dump code
3. **Accept correction** - User feedback overrides your assumptions

### 6. Authorship & Attribution

All code is authored by **Rowan Valle** (also known as Raudhan Valis).

**Git commits:**
- Author: `Rowan Valle <valis@symbiont.systems>`
- Do NOT use Co-Authored-By for Claude/AI

**Code comments and documentation:**
- Credit: "By Symbiont Systems LLC" or "By Rowan Valle"
- Tool acknowledgment: "Built with Claude Code"

The AI assistant is a tool, not a co-author.

### 7. Show Task Progression

Always use the task list system for non-trivial work:

1. **Create tasks upfront** - Break work into trackable steps before starting
2. **Update status as you go** - Mark tasks in_progress when starting, completed when done
3. **Keep the user informed** - The task list provides visibility into what's happening

> This isn't busywork—it's a contract. The task list shows your reasoning, tracks progress, and creates accountability.

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
