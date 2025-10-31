"""Main bot class that coordinates all actions."""

from config.settings import Settings
from src.logger import get_logger, setup_logger
from src.utils import WindowManager, ScreenDetector
from src.actions import TrainingActions, HealingActions, HelpingActions, GatheringActions


logger = get_logger(__name__)


class PuzzlesSurvivalBot:
    """Main bot class for Puzzles & Survival automation."""

    def __init__(self, window_title: str = None, debug: bool = False):
        """
        Initialize the bot.

        Args:
            window_title: Title of the game window (defaults to Settings)
            debug: Enable debug logging
        """
        # Setup logging
        log_level = "DEBUG" if debug else Settings.LOG_LEVEL
        setup_logger(level=log_level)

        logger.info("Initializing Puzzles & Survival Bot")

        # Validate configuration
        errors = Settings.validate_paths()
        if errors:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            raise RuntimeError("Bot initialization failed due to configuration errors")

        # Initialize core components
        self.window_manager = WindowManager(window_title)
        self.screen_detector = ScreenDetector(self.window_manager)

        # Initialize action modules
        self.training = TrainingActions(self.window_manager, self.screen_detector)
        self.healing = HealingActions(self.window_manager, self.screen_detector)
        self.helping = HelpingActions(self.window_manager, self.screen_detector)
        self.gathering = GatheringActions(self.window_manager, self.screen_detector)

        logger.info("Bot initialized successfully")

    def check_game_window(self) -> bool:
        """
        Check if the game window is available.

        Returns:
            True if window is found, False otherwise
        """
        window = self.window_manager.get_window()
        if window:
            logger.info(f"Game window found: {window.title}")
            return True
        else:
            logger.error("Game window not found. Is the game running?")
            return False

    def train_troops(self, times: int = 1) -> dict:
        """
        Train troops.

        Args:
            times: Number of training iterations

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting train troops action ({times} times)")
        return self.training.train_troops(times)

    def heal_troops(self, times: int = 1) -> dict:
        """
        Heal troops.

        Args:
            times: Number of healing iterations

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting heal troops action ({times} times)")
        return self.healing.heal_troops(times)

    def help_alliance(self, times: int = 1) -> dict:
        """
        Help alliance members.

        Args:
            times: Number of times to click help

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting help alliance action ({times} times)")
        return self.helping.complete_helps(times)

    def gather_resources(self, times: int = 1) -> dict:
        """
        Gather resources (food).

        Args:
            times: Number of gathering parties to send

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting gather resources action ({times} times)")
        return self.gathering.gather_food(times)

    def get_mouse_position(self):
        """Get current mouse position (useful for development/debugging)."""
        pos = self.screen_detector.get_mouse_position()
        logger.info(f"Current mouse position: {pos}")
        return pos

    def list_windows(self):
        """List all open windows (useful for debugging)."""
        windows = self.window_manager.get_all_window_titles()
        logger.info("Open windows:")
        for window in windows:
            logger.info(f"  - {window}")
        return windows

    def shutdown(self):
        """Clean shutdown of the bot."""
        logger.info("Shutting down bot")
        # Add any cleanup code here if needed
