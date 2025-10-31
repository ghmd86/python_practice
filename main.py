"""
Puzzles & Survival Bot - Main Entry Point

A game automation bot for Puzzles & Survival.
"""

import argparse
import sys
from typing import Optional

from src.bot import PuzzlesSurvivalBot
from src.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Puzzles & Survival Bot - Automate game actions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --action train --times 5
  python main.py --action help --times 3
  python main.py --action heal --times 2
  python main.py --debug

Actions:
  train    - Train troops with speedup
  heal     - Heal wounded troops
  help     - Help alliance members
  gather   - Gather resources (food)
  check    - Check if game window is available
        """
    )

    parser.add_argument(
        '--action',
        type=str,
        choices=['train', 'heal', 'help', 'gather', 'check'],
        help='Action to perform'
    )

    parser.add_argument(
        '--times',
        type=int,
        default=1,
        help='Number of times to repeat the action (default: 1)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    parser.add_argument(
        '--window-title',
        type=str,
        default=None,
        help='Game window title (default: "Puzzles & Survival")'
    )

    return parser


def run_action(bot: PuzzlesSurvivalBot, action: str, times: int) -> Optional[dict]:
    """
    Execute a bot action.

    Args:
        bot: Bot instance
        action: Action to perform
        times: Number of times to repeat

    Returns:
        Result dictionary or None
    """
    action_map = {
        'train': bot.train_troops,
        'heal': bot.heal_troops,
        'help': bot.help_alliance,
        'gather': bot.gather_resources,
    }

    if action == 'check':
        bot.check_game_window()
        return None

    if action in action_map:
        return action_map[action](times)

    return None


def print_results(action: str, results: Optional[dict]):
    """
    Print action results.

    Args:
        action: Action that was performed
        results: Results dictionary
    """
    if results is None:
        return

    print("\n" + "=" * 50)
    print(f"Action: {action.upper()}")
    print("=" * 50)
    print(f"Status: {'SUCCESS' if results.get('success') else 'FAILED'}")
    print(f"Completed: {results.get('completed', 0)}")
    print(f"Failed: {results.get('failed', 0)}")
    print("=" * 50 + "\n")


def main():
    """Main entry point for the bot."""
    parser = create_parser()
    args = parser.parse_args()

    # If no action specified, print help
    if not args.action:
        parser.print_help()
        return 0

    logger = get_logger()

    try:
        # Initialize bot
        logger.info("Starting Puzzles & Survival Bot")
        bot = PuzzlesSurvivalBot(
            window_title=args.window_title,
            debug=args.debug
        )

        # Check window availability first
        if not bot.check_game_window():
            logger.error("Cannot proceed - game window not found")
            print("\nError: Game window not found. Please ensure Puzzles & Survival is running.")
            return 1

        # Run the action
        results = run_action(bot, args.action, args.times)

        # Print results
        print_results(args.action, results)

        # Shutdown
        bot.shutdown()
        logger.info("Bot execution completed")

        return 0

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n\nBot stopped by user (Ctrl+C)")
        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n\nFatal error: {e}")
        print("Check bot.log for details")
        return 1


if __name__ == '__main__':
    sys.exit(main())
