"""Entry point for running the game as a module."""
import argparse


def main() -> None:
    """Run the game."""
    parser = argparse.ArgumentParser(
        description="Preaching the Truth - A door-to-door evangelism simulation"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="World generation seed for reproducible worlds",
    )
    args = parser.parse_args()

    # Use absolute imports that work both as module and frozen executable
    try:
        from preaching.ui import ConsoleUI
        from preaching.game import Game
    except ImportError:
        from .ui import ConsoleUI
        from .game import Game

    ui = ConsoleUI()
    game = Game(ui, seed=args.seed)
    game.run()


if __name__ == "__main__":
    main()
