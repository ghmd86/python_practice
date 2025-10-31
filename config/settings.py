"""Configuration settings for Puzzles & Survival Bot."""

import os
from pathlib import Path


class Settings:
    """Central configuration for the bot."""

    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    IMAGES_DIR = BASE_DIR / "images"
    BUTTONS_DIR = IMAGES_DIR / "buttons"
    DIALOGS_DIR = IMAGES_DIR / "dialogs"
    INDICATORS_DIR = IMAGES_DIR / "indicators"

    # Game window settings
    GAME_WINDOW_TITLE = "Puzzles & Survival"

    # Image detection confidence levels
    CONFIDENCE_HIGH = 0.9
    CONFIDENCE_MEDIUM = 0.7
    CONFIDENCE_LOW = 0.6
    CONFIDENCE_VERY_LOW = 0.4

    # Timing settings (in seconds)
    DELAY_SHORT = 1.0
    DELAY_MEDIUM = 2.0
    DELAY_LONG = 4.0

    # Image file paths - Buttons
    IMAGE_TRAIN = str(BUTTONS_DIR / "train.png")
    IMAGE_CONFIRM = str(BUTTONS_DIR / "confirm.png")
    IMAGE_USE = str(BUTTONS_DIR / "use.png")
    IMAGE_SPEEDUP = str(BUTTONS_DIR / "speedup.png")
    IMAGE_AUTO_SPEEDUP = str(BUTTONS_DIR / "autospeedup.png")
    IMAGE_HEAL = str(BUTTONS_DIR / "heal.png")
    IMAGE_CLEAR = str(BUTTONS_DIR / "Clear.png")
    IMAGE_PLUS = str(BUTTONS_DIR / "plus.png")
    IMAGE_HELP = str(BUTTONS_DIR / "help.png")
    IMAGE_HELP1 = str(BUTTONS_DIR / "help1.png")
    IMAGE_HELP_FULL = str(BUTTONS_DIR / "helpfull.png")
    IMAGE_WORLD = str(BUTTONS_DIR / "world.png")

    # Image file paths - Dialogs
    IMAGE_CONFIRMBOX = str(DIALOGS_DIR / "confirmbox.png")
    IMAGE_CANCEL_CONFIRM = str(DIALOGS_DIR / "cancelconfirm.png")

    # Image file paths - Indicators
    IMAGE_CHECKBOX = str(INDICATORS_DIR / "checkbox.png")
    IMAGE_FIVE_MIN = str(INDICATORS_DIR / "fivemin.png")
    IMAGE_LOW_LEVEL = str(INDICATORS_DIR / "lowlvl.png")
    IMAGE_LVL6_FOOD = str(INDICATORS_DIR / "lvl6food.png")

    # Action-specific settings
    TRAIN_TROOPS_CONFIDENCE = CONFIDENCE_MEDIUM
    SPEEDUP_CONFIDENCE = CONFIDENCE_MEDIUM
    AUTO_SPEEDUP_CONFIDENCE = CONFIDENCE_LOW
    CONFIRMBOX_CONFIDENCE = CONFIDENCE_MEDIUM
    CHECKBOX_CONFIDENCE = CONFIDENCE_MEDIUM
    FIVE_MIN_CONFIDENCE = CONFIDENCE_LOW
    USE_BUTTON_CONFIDENCE = CONFIDENCE_LOW
    HELP_FULL_CONFIDENCE = CONFIDENCE_HIGH
    CLEAR_CONFIDENCE = 0.8
    PLUS_CONFIDENCE = 0.8
    HEAL_CONFIDENCE = 0.8
    LOW_LEVEL_CONFIDENCE = CONFIDENCE_VERY_LOW

    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 0.5

    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = str(BASE_DIR / "bot.log")

    # Safety settings
    FAILSAFE = True  # PyAutoGUI failsafe (move mouse to corner to stop)
    PAUSE = 0.1  # Pause between PyAutoGUI actions

    @classmethod
    def validate_paths(cls):
        """Validate that all required directories and files exist."""
        errors = []

        # Check directories
        for dir_path in [cls.IMAGES_DIR, cls.BUTTONS_DIR, cls.DIALOGS_DIR, cls.INDICATORS_DIR]:
            if not dir_path.exists():
                errors.append(f"Directory not found: {dir_path}")

        # Check critical image files
        critical_images = [
            cls.IMAGE_TRAIN,
            cls.IMAGE_CONFIRM,
            cls.IMAGE_HELP_FULL,
        ]

        for image_path in critical_images:
            if not Path(image_path).exists():
                errors.append(f"Critical image not found: {image_path}")

        return errors

    @classmethod
    def get_image_path(cls, category: str, filename: str) -> str:
        """
        Get the full path for an image file.

        Args:
            category: Image category ('buttons', 'dialogs', 'indicators')
            filename: Name of the image file

        Returns:
            Full path to the image file
        """
        category_map = {
            'buttons': cls.BUTTONS_DIR,
            'dialogs': cls.DIALOGS_DIR,
            'indicators': cls.INDICATORS_DIR,
        }

        if category not in category_map:
            raise ValueError(f"Invalid category: {category}. Must be one of {list(category_map.keys())}")

        return str(category_map[category] / filename)
