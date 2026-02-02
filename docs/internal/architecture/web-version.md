# Web Version Architecture

**Status:** Complete
**Location:** `docs/index.html`, `docs/style.css`, `docs/game.js`

---

## Overview

The web version is a standalone JavaScript port of the Python game. It runs entirely client-side with no backend dependency.

## File Structure

```
docs/
├── index.html    # HTML structure and UI layout
├── style.css     # Dark theme styling
└── game.js       # Complete game logic (~1,173 lines)
```

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Markup | Semantic HTML5 |
| Styling | CSS3 (custom properties, flexbox) |
| Logic | Vanilla JavaScript (ES6+) |
| Hosting | GitHub Pages (via `docs/` folder) |

**No frameworks or dependencies.** Works in any modern browser.

---

## UI Structure

### Layout

```
┌─────────────────────────────────────────┐
│              Status Bar                  │
│  Day | Score | Hunger | Money | Weather │
├─────────────────────────────────────────┤
│                                         │
│            Game Content                 │
│         (dynamic content area)          │
│                                         │
├─────────────────────────────────────────┤
│            Location Bar                 │
│     County > Town > Neighborhood        │
└─────────────────────────────────────────┘
```

### CSS Theming

Dark 1990s-inspired aesthetic:
- Dark background (#1a1a2e)
- Cyan accents (#00d4ff)
- Monospace font
- Subtle glow effects

---

## JavaScript Architecture

### Game State

```javascript
const gameState = {
    score: 0,
    satanic_score: 0,
    hunger: 0,
    money: 10,
    religion: 'Evangelist',
    day: 0,
    // ... mirrors Python GameState
};
```

### Core Functions

| Function | Purpose |
|----------|---------|
| `initGame()` | Reset state, generate world |
| `generateWorld()` | Create county/town/neighborhood hierarchy |
| `runDay()` | Day loop logic |
| `visitLocation()` | Handle location visits |
| `startConversation()` | Begin NPC dialogue |
| `handleResponse()` | Process player response |
| `checkConversion()` | Check interest thresholds |
| `endGame()` | Display final score |

### UI Update Pattern

```javascript
function updateUI() {
    document.getElementById('score').textContent = gameState.score;
    document.getElementById('hunger').textContent = gameState.hunger;
    // ... update all UI elements
}
```

---

## Parity with Python Version

### Implemented

- Preacher selection (all 7 + custom)
- Religion selection (4 visible + Satanic hidden)
- World generation (County → Town → Neighborhood → Location)
- NPC personalities and moods
- Conversation system with interest tracking
- Reputation system
- Item/shop system
- Random events (food donation, Satanic Bible)
- 7-day game loop
- Score tracking

### Differences

| Feature | Python | Web |
|---------|--------|-----|
| Narrative engine | Full | Simplified |
| Memory system | Full | Basic |
| Journal generation | Full | Minimal |
| Save/Load | Not implemented | Not implemented |

---

## Deployment

### GitHub Pages

The `docs/` folder is configured for GitHub Pages:
1. Repository Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs
4. Accessible at: `https://username.github.io/repo-name/`

### Local Testing

```bash
# Simple HTTP server
cd docs/
python -m http.server 8000
# Open http://localhost:8000
```

---

## Maintenance Considerations

### Code Duplication

The web version duplicates Python logic. Changes must be made in both places:
- `preaching/*.py` - Python version
- `docs/game.js` - JavaScript version

### Future Sync Strategy

Options for keeping versions in sync:
1. **Manual sync** - Update both when changing features
2. **Transpilation** - Use tool to generate JS from Python
3. **Shared spec** - JSON config files used by both
4. **API backend** - Web calls Python backend (adds complexity)

Currently using option 1 (manual sync).

---

## Responsive Design

The web version is mobile-friendly:
- Flexible layout with max-width containers
- Touch-friendly button sizes
- Readable font sizes on small screens
- No horizontal scrolling required

---

*See also: [Architecture Overview](overview.md) | [Future Ideas](../future/expansion-ideas.md)*
