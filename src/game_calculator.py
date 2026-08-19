"""
game_calculator.py
------------------
A gamified desktop calculator built with Python and Tkinter.

Features:
  - Standard arithmetic operations (add, subtract, multiply, divide, %, negate)
  - Score system with combo multiplier (up to x10)
  - Canvas-based particle effects and floating score labels
  - Calculation history panel (last 5 entries)
  - Full keyboard support
"""

import tkinter as tk
import random
import time

# ─────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────
BG         = "#0d0d1a"
PANEL      = "#12122a"
CARD       = "#1a1a35"
ACCENT     = "#7c3aed"      # purple
ACCENT2    = "#06b6d4"      # cyan
GOLD       = "#f59e0b"
RED        = "#ef4444"
GREEN      = "#10b981"
TEXT_MAIN  = "#f8fafc"
TEXT_DIM   = "#64748b"
NEON_GLOW  = "#a78bfa"
DISPLAY_BG = "#0a0a1f"

# ─────────────────────────────────────────────
#  PARTICLE ENGINE
# ─────────────────────────────────────────────
class Particle:
    def __init__(self, canvas, x, y, colour):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-6, -1)
        self.life = 1.0
        self.decay = random.uniform(0.03, 0.07)
        size = random.randint(3, 7)
        self.id = canvas.create_oval(x, y, x+size, y+size, fill=colour, outline="")
        self.alive = True

    def update(self):
        self.life -= self.decay
        if self.life <= 0:
            self.canvas.delete(self.id)
            self.alive = False
            return
        self.vy += 0.3
        self.x += self.vx
        self.y += self.vy
        self.canvas.coords(self.id,
                           self.x, self.y,
                           self.x + 6, self.y + 6)


# ─────────────────────────────────────────────
#  FLOATING SCORE TEXT
# ─────────────────────────────────────────────
class FloatingText:
    def __init__(self, canvas, x, y, text, colour):
        self.canvas = canvas
        self.y = y
        self.vy = -2
        self.life = 1.0
        self.decay = 0.025
        self.id = canvas.create_text(x, y, text=text, fill=colour,
                                     font=("Segoe UI", 16, "bold"))
        self.alive = True

    def update(self):
        self.life -= self.decay
        if self.life <= 0:
            self.canvas.delete(self.id)
            self.alive = False
            return
        self.y += self.vy
        self.canvas.coords(self.id, self.canvas.coords(self.id)[0], self.y)


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class GameCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Calculator")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ── State ──────────────────────────────
        self.expression    = ""
        self.result_shown  = False
        self.score         = 0
        self.combo         = 0
        self.max_combo     = 0
        self.calcs_done    = 0
        self.last_correct  = 0
        self.multiplier    = 1
        self.particles     = []
        self.floaters      = []
        self._animating    = True

        # ── History ────────────────────────────
        self.history = []

        self._build_ui()
        self._animate_loop()

    # ══════════════════════════════════════════
    #  UI CONSTRUCTION
    # ══════════════════════════════════════════
    def _build_ui(self):
        W = 460

        # ── Header ────────────────────────────
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=(18, 0))

        tk.Label(header, text="GAME CALC", fg=NEON_GLOW, bg=BG,
                 font=("Segoe UI", 20, "bold")).pack(side="left")

        right_hdr = tk.Frame(header, bg=BG)
        right_hdr.pack(side="right")

        self.combo_lbl = tk.Label(right_hdr, text="COMBO x1",
                                  fg=GOLD, bg=BG, font=("Segoe UI", 11, "bold"))
        self.combo_lbl.pack(side="right", padx=(10, 0))

        # ── Score bar ─────────────────────────
        score_frame = tk.Frame(self.root, bg=PANEL, bd=0)
        score_frame.pack(fill="x", padx=18, pady=(8, 4))

        tk.Label(score_frame, text="SCORE", fg=TEXT_DIM, bg=PANEL,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=10, pady=6)

        self.score_lbl = tk.Label(score_frame, text="0", fg=GOLD, bg=PANEL,
                                  font=("Segoe UI", 18, "bold"))
        self.score_lbl.pack(side="left", padx=4)

        stats_frame = tk.Frame(score_frame, bg=PANEL)
        stats_frame.pack(side="right", padx=10)

        self.calcs_lbl = tk.Label(stats_frame, text="Calcs: 0",
                                  fg=TEXT_DIM, bg=PANEL, font=("Segoe UI", 9))
        self.calcs_lbl.pack(anchor="e")

        self.best_lbl = tk.Label(stats_frame, text="Best combo: x1",
                                 fg=TEXT_DIM, bg=PANEL, font=("Segoe UI", 9))
        self.best_lbl.pack(anchor="e")

        # ── Particle canvas (lives behind display) ─
        self.canvas = tk.Canvas(self.root, width=W, height=90,
                                bg=DISPLAY_BG, highlightthickness=0)
        self.canvas.pack(padx=18, pady=(4, 0))

        # Display text items on canvas
        self.expr_id = self.canvas.create_text(W-14, 28, anchor="e",
                                               text="", fill=TEXT_DIM,
                                               font=("Segoe UI", 14))
        self.disp_id = self.canvas.create_text(W-14, 68, anchor="e",
                                               text="0", fill=TEXT_MAIN,
                                               font=("Segoe UI", 34, "bold"))

        # ── Operator glow strip ───────────────
        self.glow_strip = tk.Frame(self.root, bg=ACCENT, height=8)
        self.glow_strip.pack(fill="x", padx=18)

        # ── Buttons ───────────────────────────
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(padx=18, pady=10)

        layout = [
            ["C",   "+/-",  "%",  "/"],
            ["7",   "8",  "9",  "*"],
            ["4",   "5",  "6",  "-"],
            ["1",   "2",  "3",  "+"],
            ["00",  "0",  ".",  "="],
        ]

        for r, row in enumerate(layout):
            for c, lbl in enumerate(row):
                self._make_btn(btn_frame, lbl, r, c)

        # ── History panel ─────────────────────
        hist_outer = tk.Frame(self.root, bg=PANEL)
        hist_outer.pack(fill="x", padx=18, pady=(0, 14))

        tk.Label(hist_outer, text="HISTORY", fg=TEXT_DIM, bg=PANEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=10, pady=(6, 0))

        self.hist_lbl = tk.Label(hist_outer, text="--", fg=ACCENT2,
                                 bg=PANEL, font=("Segoe UI", 9),
                                 wraplength=400, justify="left")
        self.hist_lbl.pack(anchor="w", padx=10, pady=(2, 8))

    # ══════════════════════════════════════════
    #  BUTTON FACTORY
    # ══════════════════════════════════════════
    def _btn_colours(self, lbl):
        if lbl == "=":
            return ACCENT, TEXT_MAIN
        if lbl in ("/", "*", "-", "+"):
            return ACCENT2, "#0d0d1a"
        if lbl in ("C", "+/-", "%"):
            return "#2d2d55", TEXT_MAIN
        return CARD, TEXT_MAIN

    def _make_btn(self, parent, lbl, row, col):
        bg, fg = self._btn_colours(lbl)
        padx = 5
        pady = 4

        outer = tk.Frame(parent, bg=BG)
        outer.grid(row=row, column=col, padx=padx, pady=pady)

        btn = tk.Button(
            outer, text=lbl, width=5, height=2,
            bg=bg, fg=fg, activebackground=NEON_GLOW,
            activeforeground=BG,
            font=("Segoe UI", 15, "bold"),
            relief="flat", cursor="hand2",
            command=lambda l=lbl: self._btn_press(l)
        )
        btn.pack()

        # Hover animation
        def on_enter(e, b=btn, orig=bg, o_lbl=lbl):
            b.configure(bg=NEON_GLOW if o_lbl == "=" else ACCENT, fg=BG)

        def on_leave(e, b=btn, orig=bg, ofg=fg):
            b.configure(bg=orig, fg=ofg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # ══════════════════════════════════════════
    #  BUTTON LOGIC
    # ══════════════════════════════════════════
    def _btn_press(self, lbl):
        # Spawn press particles
        self._burst_at(230, 45, ACCENT, count=6)

        if lbl == "C":
            self._clear()
        elif lbl == "+/-":
            self._negate()
        elif lbl == "%":
            self._percent()
        elif lbl == "=":
            self._evaluate()
        else:
            self._append(lbl)

        self._refresh_display()

    def _clear(self):
        self.expression   = ""
        self.result_shown = False
        self._set_display("0")
        self._set_expr("")
        self.glow_strip.configure(bg=ACCENT)

    def _negate(self):
        try:
            val = eval(self.expression or "0")
            self.expression = str(-val)
            self.result_shown = True
        except Exception:
            pass

    def _percent(self):
        try:
            val = eval(self.expression or "0")
            self.expression = str(val / 100)
            self.result_shown = True
        except Exception:
            pass

    def _append(self, ch):
        if self.result_shown and ch not in "+-*/":
            self.expression = ""
        self.result_shown = False
        self.expression += ch

    def _evaluate(self):
        if not self.expression:
            return
        try:
            expr_display = (self.expression
                            .replace("*", "x")
                            .replace("/", "/"))
            result = eval(self.expression)

            # Format result
            if isinstance(result, float) and result.is_integer():
                result_str = str(int(result))
            else:
                result_str = f"{result:.8g}"

            # ── Scoring ───────────────────────
            now = time.time()
            if now - self.last_correct < 4:
                self.combo    += 1
                self.multiplier = min(self.combo + 1, 10)
            else:
                self.combo    = 1
                self.multiplier = 1

            self.max_combo = max(self.max_combo, self.combo)
            self.last_correct = now

            pts = self._calc_points(self.expression) * self.multiplier
            self.score     += pts
            self.calcs_done += 1

            self._add_history(expr_display, result_str)
            self.expression   = result_str
            self.result_shown = True

            self._set_expr(f"{expr_display} =")
            self._set_display(result_str)
            self.glow_strip.configure(bg=GREEN)

            # Visual effects
            self._burst_at(230, 60, GREEN, count=20)
            self._float_score(pts)
            self._update_score_ui()
            self._update_combo_ui()

            # Reset glow after delay
            self.root.after(600, lambda: self.glow_strip.configure(bg=ACCENT))

        except ZeroDivisionError:
            self._show_error("DIVIDE BY 0!")
        except Exception:
            self._show_error("SYNTAX ERR")

    def _calc_points(self, expr):
        """Points based on complexity of expression."""
        ops = sum(expr.count(op) for op in "+-*/")
        length = len(expr)
        return max(10, ops * 25 + length * 2)

    def _show_error(self, msg):
        self._set_display(msg)
        self._set_expr("")
        self.expression   = ""
        self.result_shown = False
        self.combo        = 0
        self.multiplier   = 1
        self.glow_strip.configure(bg=RED)
        self._burst_at(230, 60, RED, count=15)
        self.root.after(800, lambda: self.glow_strip.configure(bg=ACCENT))

    # ══════════════════════════════════════════
    #  DISPLAY HELPERS
    # ══════════════════════════════════════════
    def _refresh_display(self):
        if not self.result_shown:
            disp = self.expression or "0"
            self._set_display(disp)

    def _set_display(self, text):
        # Shrink font for long numbers
        if len(text) > 12:
            fnt = ("Segoe UI", 20, "bold")
        elif len(text) > 8:
            fnt = ("Segoe UI", 27, "bold")
        else:
            fnt = ("Segoe UI", 34, "bold")
        self.canvas.itemconfigure(self.disp_id, text=text, font=fnt)

    def _set_expr(self, text):
        self.canvas.itemconfigure(self.expr_id, text=text)

    def _update_score_ui(self):
        self.score_lbl.configure(text=f"{self.score:,}")
        self.calcs_lbl.configure(text=f"Calcs: {self.calcs_done}")
        self.best_lbl.configure(text=f"Best combo: x{self.max_combo}")

    def _update_combo_ui(self):
        if self.combo >= 5:
            colour = RED
        elif self.combo >= 3:
            colour = GOLD
        else:
            colour = ACCENT2
        self.combo_lbl.configure(
            text=f"COMBO x{self.multiplier}",
            fg=colour
        )

    def _add_history(self, expr, result):
        entry = f"{expr} = {result}"
        self.history.insert(0, entry)
        self.history = self.history[:5]
        self.hist_lbl.configure(text="  |  ".join(self.history))

    # ══════════════════════════════════════════
    #  PARTICLE EFFECTS
    # ══════════════════════════════════════════
    def _burst_at(self, x, y, colour, count=12):
        for _ in range(count):
            px = x + random.randint(-20, 20)
            py = y + random.randint(-10, 10)
            self.particles.append(Particle(self.canvas, px, py, colour))

    def _float_score(self, pts):
        colours = [GOLD, GREEN, ACCENT2]
        col = random.choice(colours)
        cx = 230
        cy = 50
        self.floaters.append(FloatingText(self.canvas, cx, cy,
                                          f"+{pts} pts", col))
        if self.multiplier > 1:
            self.floaters.append(FloatingText(
                self.canvas, cx + 60, cy + 10,
                f"x{self.multiplier} COMBO!", GOLD))

    def _animate_loop(self):
        if not self._animating:
            return
        # Update particles
        alive = []
        for p in self.particles:
            p.update()
            if p.alive:
                alive.append(p)
        self.particles = alive

        # Update floaters
        falive = []
        for f in self.floaters:
            f.update()
            if f.alive:
                falive.append(f)
        self.floaters = falive

        self.root.after(16, self._animate_loop)   # ~60 fps

    # ══════════════════════════════════════════
    #  KEYBOARD SUPPORT
    # ══════════════════════════════════════════
    def bind_keys(self):
        self.root.bind("<Return>",    lambda e: self._btn_press("="))
        self.root.bind("<KP_Enter>",  lambda e: self._btn_press("="))
        self.root.bind("<Escape>",    lambda e: self._btn_press("C"))
        self.root.bind("<BackSpace>", self._backspace)

        for ch in "0123456789.+-*/":
            self.root.bind(ch, lambda e, c=ch: self._btn_press(c))

    def _backspace(self, event=None):
        if not self.result_shown and self.expression:
            self.expression = self.expression[:-1]
            self._refresh_display()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main():
    root = tk.Tk()

    # Centre window
    W, H = 498, 680
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

    app = GameCalculator(root)
    app.bind_keys()

    # Pulsing title update
    def pulse():
        root.title(f"Game Calculator  |  Score: {app.score:,}  |  x{app.multiplier} Combo")
        root.after(800, pulse)
    pulse()

    root.mainloop()


if __name__ == "__main__":
    main()
