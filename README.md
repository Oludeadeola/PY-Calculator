# Game Calculator

A gamified desktop and browser calculator built with Python (Tkinter) and HTML/CSS/JavaScript.
Enter calculations, chain them fast to build combo multipliers, earn points, and watch particle effects burst on every result.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Desktop Version (Python)](#desktop-version-python)
  - [Web Version (Browser)](#web-version-browser)
- [How to Play](#how-to-play)
- [Scoring](#scoring)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

Game Calculator turns everyday arithmetic into a game. Every calculation you evaluate earns you points. Chain multiple calculations quickly to activate a combo multiplier (up to x10). The more complex your expression, the higher your score.

The project ships in two forms:

- **Desktop version** — a standalone Python app using Tkinter, no dependencies required beyond the Python standard library.
- **Web version** — a pure HTML, CSS, and JavaScript implementation that runs directly in any modern browser.

---

## Project Structure

```
PY-Calculator/
│
├── src/
│   └── game_calculator.py    # Desktop app (Python + Tkinter)
│
├── web/
│   ├── index.html            # Web app entry point
│   ├── style.css             # Styles and dark theme
│   └── script.js             # Game logic, particles, scoring
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Features

- Standard calculator operations: addition, subtraction, multiplication, division, percentage, and negation
- Scoring system that rewards complexity — more operators and longer expressions earn more points
- Combo multiplier that grows when you chain calculations within 4 seconds (up to x10)
- Particle burst animation on every button press and result
- Floating score labels that appear after each successful evaluation
- History panel showing the last 5 calculations
- Full keyboard support in both versions
- Neon dark UI with hover effects and a colour-coded glow strip

---

## Getting Started

### Desktop Version (Python)

**Requirements**

- Python 3.8 or higher
- `tkinter` (included with Python on Windows, macOS, and most Linux distributions)

**Run**

```bash
python src/game_calculator.py
```

On Windows, you can also double-click the file if Python is associated with `.py` files.

---

### Web Version (Browser)

No installation or server required. Open the file directly in your browser:

```
web/index.html
```

Or right-click `index.html` and choose "Open with" your browser of choice.

---

## How to Play

1. Enter a number or expression using the buttons or your keyboard.
2. Press `=` or `Enter` to evaluate.
3. A particle burst fires and your score updates.
4. Keep evaluating within 4 seconds to build your combo multiplier.
5. The combo badge and glow strip change colour as your streak grows.
6. An error (syntax or divide-by-zero) resets your combo to 1.

---

## Scoring

Points are calculated per evaluation using the following formula:

```
base_points = (number_of_operators x 25) + (expression_length x 2)
final_points = max(10, base_points) x combo_multiplier
```

The combo multiplier increases by 1 for each successive calculation completed within 4 seconds, capped at x10.

**Combo colour indicators**

| Streak | Colour |
|--------|--------|
| 1 to 2 | Cyan   |
| 3 to 4 | Gold   |
| 5 or more | Red |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| 0 through 9 | Enter digits |
| . | Decimal point |
| + - * / | Operators |
| Enter or Numpad Enter | Evaluate |
| Escape | Clear |
| Backspace | Delete last character |

---

## Configuration

### Desktop (Python)

All colour constants are defined at the top of `src/game_calculator.py` and can be changed freely:

```python
ACCENT  = "#7c3aed"    # primary accent colour
GOLD    = "#f59e0b"    # score and combo label colour
```

The animation frame rate is set in `_animate_loop`:

```python
self.root.after(16, self._animate_loop)   # 16ms = ~60 fps
```

The combo time window (in seconds) is set in `_evaluate`:

```python
if now - self.last_correct < 4:    # change to adjust combo window
```

### Web (JavaScript)

Colours are controlled via CSS custom properties in `web/style.css`:

```css
:root {
  --accent:  #7c3aed;
  --gold:    #f59e0b;
}
```

The combo window is set in `web/script.js`:

```js
if (now - state.lastCorrect < 4) {   // seconds
```

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "feat: describe your change"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request.

**Ideas for contributions**

- Sound effects on button press and combo activation
- Persistent high-score storage using JSON or localStorage
- Scientific calculator mode (sin, cos, log, square root)
- Leaderboard or session history screen
- Responsive mobile layout improvements

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Olude Adeola

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Author

**Olude Adeola**
Email: oludeadeola67@gmail.com
GitHub: https://github.com/Oludeadeola
