# 🎮 Game Calculator

> A gamified desktop calculator built with Python + Tkinter — featuring particle effects, combo multipliers, a live score system, and a sleek neon dark-mode UI.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔢 **Full Calculator** | Addition, subtraction, multiplication, division, percentage, negation |
| 🎯 **Scoring System** | Earn points for every calculation — more complex expressions = more points |
| ⚡ **Combo Multiplier** | Chain calculations within 4 seconds to build up a combo (up to x10!) |
| 💥 **Particle Effects** | Animated particles burst on every button press and calculation |
| 📈 **Floating Score Text** | `+pts` and `COMBO!` text floats up after each successful evaluation |
| 📜 **History Panel** | Displays your last 5 calculations at a glance |
| ⌨️ **Keyboard Support** | Full keyboard input — numbers, operators, Enter, Escape, Backspace |
| 🌈 **Neon Dark UI** | Custom dark-mode colour palette with hover animations and a glow strip |
| 📊 **Live Stats** | Tracks total calculations done and your best combo streak |

---

## 🖼️ Preview

```
╔══════════════════════════════╗
║  GAME CALC          COMBO x3 ║
║  SCORE  1,250    Calcs: 8    ║
║         Best combo: x5       ║
╠══════════════════════════════╣
║  42 + 8 =                    ║
║                           50 ║
╠══════════════════════════════╣  <- neon glow strip
║  C    +/-   %    /           ║
║  7     8    9    *           ║
║  4     5    6    -           ║
║  1     2    3    +           ║
║  00    0    .    =           ║
╠══════════════════════════════╣
║ HISTORY                      ║
║ 42+8=50  |  10*3=30  | ...   ║
╚══════════════════════════════╝
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8 or higher** — [Download here](https://www.python.org/downloads/)
- `tkinter` — ships with Python on all major platforms (no extra install needed)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/PY-Calculator.git

# 2. Navigate into the project directory
cd PY-Calculator

# 3. Run the app
python game_calculator.py
```

> **Windows users**: You can also double-click `game_calculator.py` if Python is associated with `.py` files.

---

## 🎮 How to Play

1. **Enter an expression** using the on-screen buttons or your keyboard.
2. Press **`=`** (or `Enter`) to evaluate — a particle burst fires and your score updates.
3. **Chain calculations fast** (within 4 seconds) to build a combo multiplier — up to **x10**.
4. **More complex expressions** (more operators, longer inputs) yield higher base points.
5. Beat your **best combo streak** tracked in the top-right stats panel.

### Scoring Formula

```
Points = (num_operators x 25 + expression_length x 2) x combo_multiplier
Minimum 10 points per calculation.
```

### Combo Colours

| Combo Level | Colour |
|---|---|
| 1-2 | Cyan |
| 3-4 | Gold |
| 5+  | Red (on fire!) |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|---|---|
| `0-9` | Input digit |
| `.` | Decimal point |
| `+` `-` `*` `/` | Operators |
| `Enter` / `Numpad Enter` | Evaluate (`=`) |
| `Escape` | Clear (`C`) |
| `Backspace` | Delete last character |

---

## 🗂️ Project Structure

```
PY-Calculator/
├── game_calculator.py   # Main application — all UI, logic, and effects
└── README.md            # Project documentation (you are here)
```

### Key Classes

| Class | Responsibility |
|---|---|
| `GameCalculator` | Root application class — builds the UI, handles button logic, scoring, history, and animation loop |
| `Particle` | Animated confetti particle rendered on the canvas; fades and falls under simulated gravity |
| `FloatingText` | Floating score/combo label that drifts upward and fades out after each calculation |

---

## 🎨 Colour Palette

| Token | Hex | Usage |
|---|---|---|
| `BG` | `#0d0d1a` | App background |
| `PANEL` | `#12122a` | Score bar & history panel |
| `CARD` | `#1a1a35` | Default button face |
| `ACCENT` | `#7c3aed` | `=` button & glow strip |
| `ACCENT2` | `#06b6d4` | Operator buttons |
| `GOLD` | `#f59e0b` | Score label & combo text |
| `RED` | `#ef4444` | Error state |
| `GREEN` | `#10b981` | Success state |
| `NEON_GLOW` | `#a78bfa` | Hover highlight |
| `DISPLAY_BG` | `#0a0a1f` | Calculator display canvas |

---

## 🔧 Configuration (source-level)

All visual constants are declared at the top of `game_calculator.py` and can be freely changed:

```python
ACCENT  = "#7c3aed"   # change to your favourite accent colour
GOLD    = "#f59e0b"   # score / combo colour
```

Animation speed is controlled by the frame-rate constant in `_animate_loop`:

```python
self.root.after(16, self._animate_loop)   # ~60 fps — increase value for slower animations
```

Combo window (seconds between chained calculations):

```python
if now - self.last_correct < 4:   # change 4 to adjust combo time window
```

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- 🔊 Sound effects on button press / combo
- 💾 Persistent high-score saving (JSON / SQLite)
- 🧮 Scientific mode (sin, cos, log, sqrt ...)
- 🏆 Leaderboard screen
- 🖥️ Fullscreen / resizable layout

**Steps:**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your fork: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

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

## 👤 Author

**Olude Adeola**
- Email: oludeadeola67@gmail.com

---

<p align="center">Made with love and Python</p>
