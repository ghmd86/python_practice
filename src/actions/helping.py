"""Helping-related actions for the bot."""

import time

from config.settings import Settings
from src.logger import get_logger
from src.utils import ScreenDetector, WindowManager


logger = get_logger(__name__)


class HelpingActions:
    """Handles alliance help operations."""

    def __init__(self, window_manager: WindowManager, screen_detector: ScreenDetector):
        """
        Initialize helping actions.

        Args:
            window_manager: WindowManager instance
            screen_detector: ScreenDetector instance
        """
        self.window_manager = window_manager
        self.screen = screen_detector

    def complete_helps(self, times: int = 1) -> dict:
        """
        Click the help all button to help alliance members.

        Args:
            times: Number of times to click the help button

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting help sequence (clicks: {times})")

        # Activate game window
        if not self.window_manager.activate_window():
            logger.error("Failed to activate game window")
            return {"success": False, "completed": 0, "failed": times}

        time.sleep(Settings.DELAY_MEDIUM)

        stats = {"success": True, "completed": 0, "failed": 0}

        # Find the help all button
        help_full = self.screen.find_on_window(
            Settings.IMAGE_HELP_FULL,
            confidence=Settings.HELP_FULL_CONFIDENCE
        )

        if not help_full:
            logger.error("Help all button not found")
            return {"success": False, "completed": 0, "failed": times}

        logger.info(f"Help all button found at {help_full}")

        # Click the help button multiple times
        try:
            for click_num in range(times):
                logger.debug(f"Help click {click_num + 1}/{times}")
                self.screen.click_position(
                    help_full.left,
                    help_full.top,
                    clicks=1,
                    interval=Settings.DELAY_SHORT
                )
                stats["completed"] += 1
                time.sleep(Settings.DELAY_SHORT)

            logger.info(f"Completed help sequence: {stats['completed']} clicks")

        except Exception as e:
            logger.error(f"Error during help sequence: {e}")
            stats["failed"] = times - stats["completed"]
            stats["success"] = False

        return stats
