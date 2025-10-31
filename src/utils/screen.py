"""Screen detection and image recognition utilities."""

import time
from typing import Optional, Tuple, Union

import pyautogui
from pyautogui import Box

from config.settings import Settings
from src.logger import get_logger


logger = get_logger(__name__)


class ScreenDetector:
    """Handles screen detection and image recognition operations."""

    def __init__(self, window_manager=None):
        """
        Initialize the screen detector.

        Args:
            window_manager: WindowManager instance for window-specific operations
        """
        self.window_manager = window_manager
        # Set PyAutoGUI safety settings
        pyautogui.FAILSAFE = Settings.FAILSAFE
        pyautogui.PAUSE = Settings.PAUSE

    def find_on_screen(
        self,
        image_path: str,
        confidence: float = None,
        region: Optional[Tuple[int, int, int, int]] = None,
        grayscale: bool = False
    ) -> Optional[Box]:
        """
        Find an image on the screen.

        Args:
            image_path: Path to the image file to find
            confidence: Confidence level for image matching (0.0 to 1.0)
            region: Region to search in (x, y, width, height)
            grayscale: Whether to use grayscale for faster searching

        Returns:
            Box object with image location or None if not found
        """
        confidence = confidence or Settings.CONFIDENCE_MEDIUM

        try:
            location = pyautogui.locateOnScreen(
                image_path,
                confidence=confidence,
                region=region,
                grayscale=grayscale
            )

            if location:
                logger.debug(f"Found image '{image_path}' at {location}")
            else:
                logger.debug(f"Image '{image_path}' not found on screen")

            return location

        except Exception as e:
            logger.error(f"Error finding image '{image_path}': {e}")
            return None

    def find_on_window(
        self,
        image_path: str,
        confidence: float = None,
        limit: Optional[Box] = None
    ) -> Optional[Box]:
        """
        Find an image within the game window.

        Args:
            image_path: Path to the image file to find
            confidence: Confidence level for image matching
            limit: Bounding box to limit search area

        Returns:
            Box object with image location or None if not found
        """
        if not self.window_manager or not self.window_manager.window:
            logger.warning("Window manager not set, falling back to screen search")
            return self.find_on_screen(image_path, confidence)

        confidence = confidence or Settings.CONFIDENCE_MEDIUM

        try:
            if limit:
                # Search within a limited region
                location = pyautogui.locateOnScreen(
                    image_path,
                    region=(limit.left, limit.top, limit.width, limit.height),
                    confidence=confidence
                )
            else:
                # Search within the window
                location = pyautogui.locateOnWindow(
                    image_path,
                    title=self.window_manager.window.title,
                    confidence=confidence
                )

            if location:
                logger.debug(f"Found image '{image_path}' in window at {location}")
            else:
                logger.debug(f"Image '{image_path}' not found in window")

            return location

        except Exception as e:
            logger.error(f"Error finding image '{image_path}' in window: {e}")
            return None

    def click_image(
        self,
        image_path: str,
        confidence: float = None,
        clicks: int = 1,
        interval: float = 0.0,
        button: str = 'left',
        on_window: bool = True
    ) -> bool:
        """
        Find and click an image.

        Args:
            image_path: Path to the image file to click
            confidence: Confidence level for image matching
            clicks: Number of clicks
            interval: Interval between clicks
            button: Mouse button to click ('left', 'right', 'middle')
            on_window: Whether to search within window or entire screen

        Returns:
            True if image was found and clicked, False otherwise
        """
        try:
            if on_window:
                location = self.find_on_window(image_path, confidence)
            else:
                location = self.find_on_screen(image_path, confidence)

            if location:
                pyautogui.click(location, clicks=clicks, interval=interval, button=button)
                logger.info(f"Clicked image '{image_path}' at {location}")
                return True
            else:
                logger.warning(f"Could not click '{image_path}' - image not found")
                return False

        except Exception as e:
            logger.error(f"Error clicking image '{image_path}': {e}")
            return False

    def click_position(
        self,
        x: int,
        y: int,
        clicks: int = 1,
        interval: float = 0.0,
        button: str = 'left'
    ) -> bool:
        """
        Click at a specific screen position.

        Args:
            x: X coordinate
            y: Y coordinate
            clicks: Number of clicks
            interval: Interval between clicks
            button: Mouse button to click

        Returns:
            True if successful, False otherwise
        """
        try:
            pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
            logger.debug(f"Clicked position ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"Error clicking position ({x}, {y}): {e}")
            return False

    def wait_for_image(
        self,
        image_path: str,
        timeout: float = 10.0,
        confidence: float = None,
        check_interval: float = 0.5
    ) -> Optional[Box]:
        """
        Wait for an image to appear on screen.

        Args:
            image_path: Path to the image file to wait for
            timeout: Maximum time to wait in seconds
            confidence: Confidence level for image matching
            check_interval: Time between checks in seconds

        Returns:
            Box object with image location or None if timeout
        """
        logger.debug(f"Waiting for image '{image_path}' (timeout: {timeout}s)")
        start_time = time.time()

        while time.time() - start_time < timeout:
            location = self.find_on_window(image_path, confidence)
            if location:
                logger.info(f"Image '{image_path}' appeared after {time.time() - start_time:.1f}s")
                return location
            time.sleep(check_interval)

        logger.warning(f"Timeout waiting for image '{image_path}'")
        return None

    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.

        Returns:
            Tuple of (x, y) coordinates
        """
        return pyautogui.position()
