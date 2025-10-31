"""Healing-related actions for the bot."""

import time

from config.settings import Settings
from src.logger import get_logger
from src.utils import ScreenDetector, WindowManager


logger = get_logger(__name__)


class HealingActions:
    """Handles troop healing operations."""

    def __init__(self, window_manager: WindowManager, screen_detector: ScreenDetector):
        """
        Initialize healing actions.

        Args:
            window_manager: WindowManager instance
            screen_detector: ScreenDetector instance
        """
        self.window_manager = window_manager
        self.screen = screen_detector

    def click_clear_button(self) -> bool:
        """
        Click the clear button.

        Returns:
            True if button was found and clicked, False otherwise
        """
        logger.debug("Looking for clear button")
        clear = self.screen.find_on_screen(
            Settings.IMAGE_CLEAR,
            confidence=Settings.CLEAR_CONFIDENCE,
            grayscale=True
        )

        if clear:
            self.screen.click_position(clear.left, clear.top)
            logger.info("Clicked clear button")
            return True
        else:
            logger.debug("Clear button not found")
            return False

    def click_plus_button(self) -> bool:
        """
        Click the plus button to add troops.

        Returns:
            True if button was found and clicked, False otherwise
        """
        logger.debug("Looking for plus button")
        plus = self.screen.find_on_screen(
            Settings.IMAGE_PLUS,
            confidence=Settings.PLUS_CONFIDENCE
        )

        if plus:
            self.screen.click_position(plus.left, plus.top)
            logger.info("Clicked plus button")
            return True
        else:
            logger.warning("Plus button not found")
            return False

    def click_heal_button(self) -> bool:
        """
        Click the heal button.

        Returns:
            True if button was found and clicked, False otherwise
        """
        logger.debug("Looking for heal button")
        heal = self.screen.find_on_screen(
            Settings.IMAGE_HEAL,
            confidence=Settings.HEAL_CONFIDENCE
        )

        if heal:
            self.screen.click_position(heal.left, heal.top)
            logger.info("Clicked heal button")
            return True
        else:
            logger.warning("Heal button not found")
            return False

    def click_help_button(self) -> bool:
        """
        Click the help button (or use fallback coordinates).

        Returns:
            True if successful, False otherwise
        """
        logger.debug("Looking for help button")
        help_button = self.screen.find_on_screen(Settings.IMAGE_HELP)

        if help_button:
            self.screen.click_position(help_button.left, help_button.top)
            logger.info("Clicked help button")
            return True
        else:
            logger.warning("Help button not found, using fallback coordinates")
            # Fallback to hardcoded coordinates from original code
            self.screen.click_position(1229, 1317)
            return True

    def heal_troops(self, times: int = 1) -> dict:
        """
        Execute the full troop healing sequence.

        Args:
            times: Number of times to repeat the healing sequence

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting troop healing sequence (iterations: {times})")

        # Activate game window
        if not self.window_manager.activate_window():
            logger.error("Failed to activate game window")
            return {"success": False, "completed": 0, "failed": times}

        time.sleep(Settings.DELAY_MEDIUM)

        stats = {"success": True, "completed": 0, "failed": 0}

        for iteration in range(times):
            logger.info(f"Healing iteration {iteration + 1}/{times}")

            try:
                # Click clear button (optional)
                self.click_clear_button()
                time.sleep(Settings.DELAY_SHORT)

                # Click plus button to add troops
                if not self.click_plus_button():
                    logger.error(f"Failed to click plus button on iteration {iteration + 1}")
                    stats["failed"] += 1
                    continue

                time.sleep(Settings.DELAY_SHORT)

                # Click heal button
                if not self.click_heal_button():
                    logger.error(f"Failed to click heal button on iteration {iteration + 1}")
                    stats["failed"] += 1
                    continue

                time.sleep(Settings.DELAY_SHORT)

                # Click help button
                self.click_help_button()

                # Wait for healing to process
                time.sleep(Settings.DELAY_LONG)

                stats["completed"] += 1
                logger.info(f"Completed healing iteration {iteration + 1}/{times}")

            except Exception as e:
                logger.error(f"Error during healing iteration {iteration + 1}: {e}")
                stats["failed"] += 1

        logger.info(f"Healing sequence complete. Completed: {stats['completed']}, Failed: {stats['failed']}")
        return stats
