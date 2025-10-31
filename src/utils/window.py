"""Window management utilities."""

import time
from typing import Optional

import pygetwindow as gw

from config.settings import Settings
from src.logger import get_logger


logger = get_logger(__name__)


class WindowManager:
    """Manages game window operations."""

    def __init__(self, window_title: str = None):
        """
        Initialize the window manager.

        Args:
            window_title: Title of the game window to manage
        """
        self.window_title = window_title or Settings.GAME_WINDOW_TITLE
        self._window = None

    def get_window(self, retry: int = 3) -> Optional[gw.Win32Window]:
        """
        Get the game window.

        Args:
            retry: Number of times to retry finding the window

        Returns:
            Game window object or None if not found
        """
        for attempt in range(retry):
            try:
                windows = gw.getWindowsWithTitle(self.window_title)
                if windows:
                    self._window = windows[0]
                    logger.info(f"Found game window: {self.window_title}")
                    return self._window
                else:
                    logger.warning(f"Window '{self.window_title}' not found (attempt {attempt + 1}/{retry})")
                    if attempt < retry - 1:
                        time.sleep(Settings.DELAY_SHORT)
            except Exception as e:
                logger.error(f"Error finding window: {e}")
                if attempt < retry - 1:
                    time.sleep(Settings.DELAY_SHORT)

        logger.error(f"Could not find window '{self.window_title}' after {retry} attempts")
        return None

    def activate_window(self) -> bool:
        """
        Bring the game window to the foreground.

        Returns:
            True if successful, False otherwise
        """
        if not self._window:
            self._window = self.get_window()

        if not self._window:
            logger.error("Cannot activate window - window not found")
            return False

        try:
            self._window.activate()
            logger.debug("Window activated successfully")
            time.sleep(0.5)  # Give window time to activate
            return True
        except Exception as e:
            logger.error(f"Failed to activate window: {e}")
            return False

    def is_window_active(self) -> bool:
        """
        Check if the game window is currently active.

        Returns:
            True if window is active, False otherwise
        """
        try:
            active_window = gw.getActiveWindow()
            if active_window and self.window_title in active_window.title:
                return True
        except Exception as e:
            logger.debug(f"Error checking active window: {e}")
        return False

    def get_all_window_titles(self) -> list:
        """
        Get titles of all open windows.

        Returns:
            List of window titles
        """
        try:
            return gw.getAllTitles()
        except Exception as e:
            logger.error(f"Error getting window titles: {e}")
            return []

    @property
    def window(self):
        """Get the current window object."""
        if not self._window:
            self._window = self.get_window()
        return self._window
