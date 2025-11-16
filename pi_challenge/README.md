# Pi Day Challenge Circle Automation

Automates drawing a perfect circle in the Pi Day Challenge game to achieve the highest possible ranking (S rank).

**Game URL:** https://yage.ai/genai/pi.html

## Features

- **Perfect Circle Drawing**: Uses mathematical precision to draw a perfect circle
- **Two Methods Available**:
  - **JavaScript Method** (default): Draws directly on canvas using JavaScript for maximum precision
  - **Mouse Simulation Method**: Simulates mouse movements for games that require mouse events
- **Configurable Parameters**: Customize circle size, center position, and smoothness
- **High Accuracy**: Designed to achieve S-rank by drawing mathematically perfect circles

## Installation

1. Install Python 3.7 or higher
2. Install Chrome browser (ChromeDriver will be managed automatically)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

If you prefer to manage ChromeDriver manually:
```bash
# Windows (using Chocolatey)
choco install chromedriver

# macOS (using Homebrew)
brew install chromedriver

# Or download from: https://chromedriver.chromium.org/
```

## Usage

### Basic Usage

Simply run the script with default settings:

```bash
python pi_circle_automation.py
```

This will:
- Open the game in Chrome browser
- Wait 5 seconds for you to click on the canvas if needed
- Draw a perfect circle using JavaScript
- Display the result

### Advanced Usage

#### Run in Headless Mode (Background)
```bash
python pi_circle_automation.py --headless
```

#### Use Mouse Simulation Instead of JavaScript
```bash
python pi_circle_automation.py --method mouse
```

#### Customize Circle Parameters
```bash
python pi_circle_automation.py --radius 150 --center-x 400 --center-y 400 --points 300
```

#### All Options
```bash
python pi_circle_automation.py --help
```

### Parameters

- `--headless`: Run browser in headless mode (no visible window)
- `--method`: Choose drawing method (`js` or `mouse`)
  - `js`: JavaScript drawing (default, most precise)
  - `mouse`: Mouse simulation (for games that require mouse events)
- `--radius`: Circle radius in pixels (default: 35% of canvas size)
- `--center-x`: X coordinate of circle center (default: canvas center)
- `--center-y`: Y coordinate of circle center (default: canvas center)
- `--points`: Number of points for circle (default: 200, higher = smoother)

## How It Works

### JavaScript Method (Recommended)
1. Opens the game page in Chrome
2. Finds the canvas element
3. Injects JavaScript code to draw a perfect circle directly on the canvas
4. Uses parametric equations: `x = center_x + radius * cos(θ)`, `y = center_y + radius * sin(θ)`
5. Draws a smooth, mathematically perfect circle

### Mouse Simulation Method
1. Opens the game page in Chrome
2. Calculates circle points using parametric equations
3. Simulates mouse movements by moving through each point
4. Maintains mouse button press throughout the drawing
5. Creates a smooth circle through mouse events

## Achieving S-Rank

To maximize your chances of getting an S-rank:

1. **Use JavaScript method** (default) - it's the most precise
2. **Increase point count** for smoother circles:
   ```bash
   python pi_circle_automation.py --points 300
   ```
3. **Adjust radius** to match game requirements if needed
4. **Ensure canvas is centered** - the script auto-centers by default

## Troubleshooting

### ChromeDriver Issues
If you encounter ChromeDriver errors:
```bash
pip install webdriver-manager
```
The script will automatically manage ChromeDriver if `webdriver-manager` is installed.

### Canvas Not Found
- Make sure the game URL is correct
- Wait a few seconds after the page loads
- Try running without `--headless` to see what's happening

### Circle Not Drawing
- Try the mouse simulation method: `--method mouse`
- Check that the canvas is visible and clickable
- Adjust the center coordinates if needed

### Results Not Showing
- The script waits 10 seconds for results by default
- Check the browser window for the ranking
- Some games may require manual refresh

## Technical Details

### Circle Algorithm
The program uses parametric circle equations:
- `x(θ) = center_x + radius × cos(θ)`
- `y(θ) = center_y + radius × sin(θ)`

Where θ ranges from 0 to 2π radians with evenly spaced points.

### Browser Automation
- Uses Selenium WebDriver for browser control
- Automatically hides automation indicators
- Supports both visible and headless modes

## Ethics and Terms of Service

**Please note**: Using automation tools may violate the game's terms of service. This tool is intended for:
- Educational purposes (learning about browser automation)
- Personal experimentation
- Understanding mathematical circle drawing algorithms

Use responsibly and respect the game developers' rules.

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to improve the script by:
- Adding support for other browsers
- Implementing adaptive radius detection
- Adding automatic result parsing
- Improving error handling

## Credits

Created for automating the Pi Day Challenge game at https://yage.ai/genai/pi.html

