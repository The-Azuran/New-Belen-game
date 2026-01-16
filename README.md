# Belen Torres: Preaching The Truth

A narrative-driven door-to-door preaching simulation set in 1990s suburban America.

## About

Step into the shoes of Belen Torres, a devoted door-to-door preacher on a 7-day mission to save souls. Navigate conversations with skeptics, seekers, and hostile neighbors. Manage your hunger, reputation, and resources while the game remembers your choices and weaves them into an emergent personal narrative.

## Features

- **Deep Conversation System** - Every NPC has a personality and mood. Choose your words carefully.
- **Reputation Matters** - Your actions affect how neighborhoods perceive you. Doors may close before you knock.
- **Emergent Narrative** - The game tracks your journey and generates personalized journal entries, internal monologues, and story callbacks.
- **Multiple Paths** - Play as an Evangelist, Jehovah's Witness, Mormon, or create your own faith. Hidden paths await the curious.
- **Resource Management** - Balance hunger, money, and time across 7 days.

## Download

**[Download the latest release](../../releases/latest)**

| Platform | Download |
|----------|----------|
| Windows | `Preaching-windows-x64.exe` |
| macOS | `Preaching-macos-x64` |
| Linux | `Preaching-linux-x64` |

## How to Play

1. Download the executable for your platform
2. Run it (macOS/Linux users may need to `chmod +x` first)
3. Choose your religion and begin your week

### Controls

The game is text-based. Enter numbers to make choices.

### Tips

- Visit the **library** to research residents before approaching them
- **Reputation** carries across visits - be mindful of how you leave conversations
- **Churches** can help or hinder depending on their affiliation
- Your **journal** at the end of each day reflects your experiences

## Building from Source

Requires Python 3.10+

```bash
# Clone the repo
git clone https://github.com/yourusername/belen-preaching.git
cd belen-preaching

# Run directly
python -m preaching

# Or build executable
pip install pyinstaller
pyinstaller Preaching.spec
# Executable will be in dist/
```

## License

Custom License - Free to share, attribution required, commercial use requires revenue sharing. See [LICENSE](LICENSE) for details.

## Credits

Created by Valis

---

*"Another door. Another chance."*
