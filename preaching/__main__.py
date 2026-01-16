"""Entry point for running the game as a module."""

def main() -> None:
    """Run the game."""
    # Use absolute imports that work both as module and frozen executable
    try:
        from preaching.ui import ConsoleUI
        from preaching.game import Game
    except ImportError:
        from .ui import ConsoleUI
        from .game import Game

    ui = ConsoleUI()
    game = Game(ui)
    game.run()


if __name__ == "__main__":
    main()
