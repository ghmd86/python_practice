"""Gathering-related actions for the bot."""

import time

from config.settings import Settings
from src.logger import get_logger
from src.utils import ScreenDetector, WindowManager


logger = get_logger(__name__)


class GatheringActions:
    """Handles resource gathering operations."""

    def __init__(self, window_manager: WindowManager, screen_detector: ScreenDetector):
        """
        Initialize gathering actions.

        Args:
            window_manager: WindowManager instance
            screen_detector: ScreenDetector instance
        """
        self.window_manager = window_manager
        self.screen = screen_detector

    def click_world_button(self) -> bool:
        """
        Click the world map button.

        Returns:
            True if button was found and clicked, False otherwise
        """
        logger.info("Looking for world map button")
        world = self.screen.find_on_screen(
            Settings.IMAGE_WORLD,
            confidence=Settings.CONFIDENCE_MEDIUM,
            region=(950, 1250, 500, 500)  # Region from original code
        )

        if world:
            self.screen.click_position(world.left, world.top)
            logger.info("Clicked world map button")
            return True
        else:
            logger.warning("World map button not found")
            return False

    def find_low_level_resource(self) -> bool:
        """
        Find a low-level resource on the map.

        Returns:
            True if low-level resource was found, False otherwise
        """
        logger.info("Searching for low-level resources")
        low_level = self.screen.find_on_window(
            Settings.IMAGE_LOW_LEVEL,
            confidence=Settings.LOW_LEVEL_CONFIDENCE
        )

        if low_level:
            logger.info(f"Found low-level resource at {low_level}")
            return True
        else:
            logger.warning("Low-level resource not found")
            return False

    def gather_food(self, times: int = 1) -> dict:
        """
        Execute the food gathering sequence.

        Note: This is a stub implementation. The original code had incomplete
        logic. This method provides the framework for completing the feature.

        Args:
            times: Number of times to send gathering parties

        Returns:
            Dictionary with execution statistics
        """
        logger.info(f"Starting food gathering sequence (iterations: {times})")
        logger.warning("Food gathering is not fully implemented yet")

        # Activate game window
        if not self.window_manager.activate_window():
            logger.error("Failed to activate game window")
            return {"success": False, "completed": 0, "failed": times}

        time.sleep(Settings.DELAY_MEDIUM)

        stats = {"success": False, "completed": 0, "failed": times}

        # TODO: Complete implementation with the following steps:
        # 1. Click on world map button
        # 2. Click on magnifying glass (search)
        # 3. Click on food icon
        # 4. Select level
        # 5. Click search
        # 6. Click on the food spot
        # 7. Click on gather button
        # 8. Click on Quick Select
        # 9. Click Dispatch

        if self.click_world_button():
            time.sleep(Settings.DELAY_MEDIUM)
            logger.info("World map opened - further implementation needed")
            # Implementation would continue here
            stats["success"] = False
            stats["completed"] = 0
        else:
            logger.error("Failed to open world map")

        return stats
