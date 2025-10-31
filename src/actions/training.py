"""Training-related actions for the bot."""

import time
from typing import Optional

from config.settings import Settings
from src.logger import get_logger
from src.utils import ScreenDetector, WindowManager


logger = get_logger(__name__)


class TrainingActions:
    """Handles troop training operations."""

    def __init__(self, window_manager: WindowManager, screen_detector: ScreenDetector):
        """
        Initialize training actions.

        Args:
            window_manager: WindowManager instance
            screen_detector: ScreenDetector instance
        """
        self.window_manager = window_manager
        self.screen = screen_detector

    def click_train_button(self) -> bool:
        """
        Click the train button.

        Returns:
            True if train button was found and clicked, False otherwise
        """
        logger.info("Looking for train button")
        train_location = self.screen.find_on_window(
            Settings.IMAGE_TRAIN,
            confidence=Settings.TRAIN_TROOPS_CONFIDENCE
        )

        if train_location:
            self.screen.click_position(train_location.left, train_location.top)
            logger.info("Clicked train button")
            return True
        else:
            logger.warning("Train button not found")
            return False

    def click_confirm(self, limit_box: Optional[object] = None) -> bool:
        """
        Click the confirm button.

        Args:
            limit_box: Bounding box to limit search area

        Returns:
            True if confirm button was clicked, False otherwise
        """
        logger.debug("Looking for confirm button")
        if limit_box:
            confirm_location = self.screen.find_on_screen(
                Settings.IMAGE_CONFIRM,
                confidence=Settings.CONFIDENCE_MEDIUM,
                region=(limit_box.left, limit_box.top, limit_box.width, limit_box.height)
            )
        else:
            confirm_location = self.screen.find_on_window(
                Settings.IMAGE_CONFIRM,
                confidence=Settings.CONFIDENCE_MEDIUM
            )

        if confirm_location:
            self.screen.click_position(confirm_location.left, confirm_location.top)
            logger.info("Clicked confirm button")
            return True
        else:
            logger.warning("Confirm button not found")
            return False

    def handle_confirm_dialog(self) -> bool:
        """
        Handle the cancel/confirm dialog if it appears.

        Returns:
            True if dialog was handled, False if no dialog found
        """
        logger.debug("Checking for confirm dialog")
        cancel_confirm = self.screen.find_on_window(
            Settings.IMAGE_CANCEL_CONFIRM,
            confidence=Settings.CONFIDENCE_MEDIUM
        )

        if cancel_confirm:
            logger.info("Confirm dialog detected")
            time.sleep(Settings.DELAY_SHORT)
            if self.click_confirm(cancel_confirm):
                time.sleep(Settings.DELAY_SHORT)
                self.click_train_button()
                return True

        return False

    def apply_speedup(self) -> bool:
        """
        Apply training speedup if available.

        Returns:
            True if speedup was successfully applied, False otherwise
        """
        logger.info("Attempting to apply speedup")

        # Click speedup button
        speedup_location = self.screen.find_on_window(
            Settings.IMAGE_SPEEDUP,
            confidence=Settings.SPEEDUP_CONFIDENCE
        )

        if not speedup_location:
            logger.warning("Speedup button not found")
            return False

        self.screen.click_position(speedup_location.left, speedup_location.top)
        logger.info("Clicked speedup button")
        time.sleep(Settings.DELAY_SHORT)

        # Click auto speedup
        auto_speedup = self.screen.find_on_window(
            Settings.IMAGE_AUTO_SPEEDUP,
            confidence=Settings.AUTO_SPEEDUP_CONFIDENCE
        )

        if not auto_speedup:
            logger.warning("Auto speedup button not found")
            return False

        self.screen.click_position(auto_speedup.left, auto_speedup.top)
        logger.info("Clicked auto speedup button")
        time.sleep(Settings.DELAY_SHORT)

        # Handle confirmbox with checkbox
        confirmbox = self.screen.find_on_window(
            Settings.IMAGE_CONFIRMBOX,
            confidence=Settings.CONFIRMBOX_CONFIDENCE
        )

        if confirmbox:
            logger.info("Confirmbox detected")
            # Click checkbox
            checkbox = self.screen.find_on_screen(
                Settings.IMAGE_CHECKBOX,
                confidence=Settings.CHECKBOX_CONFIDENCE,
                region=(confirmbox.left, confirmbox.top, confirmbox.width, confirmbox.height)
            )

            if checkbox:
                self.screen.click_position(checkbox.left, checkbox.top)
                logger.info("Clicked checkbox")
                time.sleep(Settings.DELAY_SHORT)

            # Click confirm in confirmbox
            self.click_confirm(confirmbox)
            time.sleep(Settings.DELAY_SHORT)

        # Use 5-minute speedup if available
        self.use_five_minute_speedup()

        return True

    def use_five_minute_speedup(self) -> bool:
        """
        Use 5-minute speedup item if available.

        Returns:
            True if 5-minute speedup was used, False otherwise
        """
        logger.debug("Checking for 5-minute speedup")
        fivemin = self.screen.find_on_window(
            Settings.IMAGE_FIVE_MIN,
            confidence=Settings.FIVE_MIN_CONFIDENCE
        )

        if fivemin:
            logger.info("5-minute speedup found")
            # Look for 'Use' button within the fivemin area
            use_button = self.screen.find_on_screen(
                Settings.IMAGE_USE,
                confidence=Settings.USE_BUTTON_CONFIDENCE,
                region=(fivemin.left, fivemin.top, fivemin.width, fivemin.height)
            )

            if use_button:
                self.screen.click_position(use_button.left, use_button.top)
                logger.info("Used 5-minute speedup")
                return True

        return False

    def train_troops(self, times: int = 1) -> dict:
        """
        Execute the full troop training sequence.

        Args:
            times: Number of times to repeat the training sequence

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting troop training sequence (iterations: {times})")

        # Activate game window
        if not self.window_manager.activate_window():
            logger.error("Failed to activate game window")
            return {"success": False, "completed": 0, "failed": times}

        time.sleep(Settings.DELAY_MEDIUM)

        stats = {"success": True, "completed": 0, "failed": 0}

        for iteration in range(times):
            logger.info(f"Training iteration {iteration + 1}/{times}")

            try:
                # Click train button
                if not self.click_train_button():
                    logger.error(f"Failed to click train button on iteration {iteration + 1}")
                    stats["failed"] += 1
                    continue

                time.sleep(Settings.DELAY_SHORT)

                # Handle confirm dialog if present
                self.handle_confirm_dialog()
                time.sleep(Settings.DELAY_SHORT)

                # Apply speedup
                self.apply_speedup()
                time.sleep(Settings.DELAY_SHORT)

                stats["completed"] += 1
                logger.info(f"Completed training iteration {iteration + 1}/{times}")

            except Exception as e:
                logger.error(f"Error during training iteration {iteration + 1}: {e}")
                stats["failed"] += 1

        logger.info(f"Training sequence complete. Completed: {stats['completed']}, Failed: {stats['failed']}")
        return stats
