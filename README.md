# Puzzles & Survival Bot

A Python automation bot for Puzzles & Survival game using PyAutoGUI for GUI automation.

## Features

- **Train Troops**: Automatically train troops with speedup items
- **Heal Troops**: Heal wounded troops automatically
- **Help Alliance**: Help alliance members with one click
- **Gather Resources**: Automate resource gathering (in development)
- **Logging**: Comprehensive logging system for debugging
- **CLI Interface**: Easy-to-use command-line interface

## Project Structure

```
python_practice/
├── config/                 # Configuration files
│   ├── __init__.py
│   └── settings.py        # Centralized settings
├── images/                # Game UI images for detection
│   ├── buttons/          # Button images
│   ├── dialogs/          # Dialog box images
│   └── indicators/       # Status indicator images
├── src/                   # Source code
│   ├── actions/          # Action modules
│   │   ├── training.py   # Troop training
│   │   ├── healing.py    # Troop healing
│   │   ├── helping.py    # Alliance help
│   │   └── gathering.py  # Resource gathering
│   ├── utils/            # Utility modules
│   │   ├── screen.py     # Screen detection
│   │   └── window.py     # Window management
│   ├── bot.py            # Main bot class
│   └── logger.py         # Logging configuration
├── tests/                 # Test files
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- Puzzles & Survival game running on Windows
- Tesseract OCR (optional, for text recognition)

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Tesseract OCR** (optional):
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add to system PATH

## Usage

### Basic Commands

Run the bot with various actions:

```bash
# Show help
python main.py

# Check if game window is available
python main.py --action check

# Train troops 5 times
python main.py --action train --times 5

# Help alliance members 3 times
python main.py --action help --times 3

# Heal troops 2 times
python main.py --action heal --times 2

# Enable debug logging
python main.py --action train --times 1 --debug
```

### Available Actions

- `train` - Train troops with automatic speedup
- `heal` - Heal wounded troops
- `help` - Help alliance members
- `gather` - Gather resources (in development)
- `check` - Check if game window is found

### Command-Line Options

```
--action ACTION    Action to perform (train, heal, help, gather, check)
--times N          Number of times to repeat the action (default: 1)
--debug            Enable debug logging
--window-title     Custom game window title (default: "Puzzles & Survival")
```

## Configuration

### Settings

All configuration is centralized in `config/settings.py`:

- **Image paths**: Locations of UI element images
- **Confidence levels**: Image detection confidence thresholds
- **Timing delays**: Wait times between actions
- **Logging settings**: Log levels and formats

### Customization

To customize behavior, edit `config/settings.py`:

```python
# Example: Adjust confidence levels
CONFIDENCE_HIGH = 0.9
CONFIDENCE_MEDIUM = 0.7
CONFIDENCE_LOW = 0.6

# Example: Adjust delays
DELAY_SHORT = 1.0
DELAY_MEDIUM = 2.0
DELAY_LONG = 4.0
```

## Safety Features

- **PyAutoGUI Failsafe**: Move mouse to screen corner to stop execution
- **Window Detection**: Verifies game window before actions
- **Error Handling**: Graceful error handling with detailed logging
- **Keyboard Interrupt**: Stop with Ctrl+C at any time

## Logging

All operations are logged to:
- **Console**: INFO level and above
- **File**: `bot.log` (DEBUG level and above)

View logs:
```bash
# View recent logs
tail -f bot.log

# Windows PowerShell
Get-Content bot.log -Wait -Tail 50
```

## Development

### Adding New Actions

1. Create a new action class in `src/actions/`
2. Implement action methods using `ScreenDetector` and `WindowManager`
3. Add action to `src/bot.py`
4. Update CLI in `main.py`

### Adding New Images

1. Take screenshots of UI elements
2. Save to appropriate `images/` subdirectory
3. Add path constant to `config/settings.py`
4. Reference in action code

## Troubleshooting

### Game Window Not Found
- Ensure Puzzles & Survival is running
- Check window title matches (default: "Puzzles & Survival")
- Use `--window-title` flag if different

### Images Not Detected
- Adjust confidence levels in `config/settings.py`
- Verify image files exist in `images/` directories
- Check game resolution and scaling settings
- Try with `--debug` flag for detailed logs

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.7+)

### Slow Performance
- Reduce image search regions
- Increase confidence thresholds
- Use grayscale image matching where possible

## Contributing

To improve the bot:

1. Follow the existing code structure
2. Add docstrings to all functions
3. Use the logging system (not print statements)
4. Test thoroughly before committing
5. Update README if adding features

## Disclaimer

This bot is for educational purposes. Use at your own risk. Automation may violate game terms of service.

## License

This project is provided as-is for personal use.

## Acknowledgments

- PyAutoGUI for GUI automation
- PyGetWindow for window management
- Pytesseract for OCR capabilities
