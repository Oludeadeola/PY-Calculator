/* ============================================================
   Game Calculator — Web Version
   script.js
   ============================================================ */

"use strict";

// ── State ──────────────────────────────────────────────────
const state = {
  expression:   "",
  resultShown:  false,
  score:        0,
  combo:        0,
  maxCombo:     0,
  calcsDone:    0,
  lastCorrect:  0,
  multiplier:   1,
  history:      [],
};

// ── DOM References ─────────────────────────────────────────
const ui = {
  displayMain:  document.getElementById("displayMain"),
  displayExpr:  document.getElementById("displayExpr"),
  scoreValue:   document.getElementById("scoreValue"),
  comboBadge:   document.getElementById("comboBadge"),
  calcsLabel:   document.getElementById("calcsLabel"),
  bestCombo:    document.getElementById("bestCombo"),
  historyText:  document.getElementById("historyText"),
  glowStrip:    document.getElementById("glowStrip"),
  canvas:       document.getElementById("particleCanvas"),
};

const ctx = ui.canvas.getContext("2d");

// ── Resize canvas to match its CSS size ───────────────────
function resizeCanvas() {
  const rect = ui.canvas.parentElement.getBoundingClientRect();
  ui.canvas.width  = rect.width;
  ui.canvas.height = rect.height;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// ── Particle System ────────────────────────────────────────
const particles = [];

class Particle {
  constructor(x, y, colour) {
    this.x    = x;
    this.y    = y;
    this.vx   = (Math.random() - 0.5) * 6;
    this.vy   = Math.random() * -6 - 1;
    this.life = 1.0;
    this.decay = 0.03 + Math.random() * 0.04;
    this.size  = 3 + Math.random() * 5;
    this.colour = colour;
  }

  update() {
    this.vy   += 0.3;
    this.x    += this.vx;
    this.y    += this.vy;
    this.life -= this.decay;
  }

  draw(ctx) {
    ctx.globalAlpha = Math.max(0, this.life);
    ctx.fillStyle   = this.colour;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size / 2, 0, Math.PI * 2);
    ctx.fill();
  }
}

function burst(x, y, colour, count = 12) {
  for (let i = 0; i < count; i++) {
    particles.push(new Particle(
      x + (Math.random() - 0.5) * 40,
      y + (Math.random() - 0.5) * 20,
      colour
    ));
  }
}

// ── Floating Score Labels ──────────────────────────────────
function floatScore(pts) {
  const colours = ["#f59e0b", "#10b981", "#06b6d4"];
  const col     = colours[Math.floor(Math.random() * colours.length)];
  spawnFloat(`+${pts} pts`, col, 0);
  if (state.multiplier > 1) {
    spawnFloat(`x${state.multiplier} COMBO!`, "#f59e0b", 40);
  }
}

function spawnFloat(text, colour, offsetX) {
  const wrap  = ui.canvas.parentElement;
  const label = document.createElement("span");
  label.className  = "float-label";
  label.textContent = text;
  label.style.color = colour;
  label.style.left  = `${50 + offsetX}%`;
  label.style.bottom = "40px";
  label.style.transform = "translateX(-50%)";
  wrap.appendChild(label);
  label.addEventListener("animationend", () => label.remove());
}

// ── Animation Loop ─────────────────────────────────────────
function animLoop() {
  ctx.clearRect(0, 0, ui.canvas.width, ui.canvas.height);

  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.update();
    p.draw(ctx);
    if (p.life <= 0) particles.splice(i, 1);
  }

  requestAnimationFrame(animLoop);
}
animLoop();

// ── Display Helpers ────────────────────────────────────────
function setDisplay(text) {
  ui.displayMain.textContent = text;
  const len = text.length;
  ui.displayMain.style.fontSize =
    len > 14 ? "1.4rem" :
    len > 10 ? "1.9rem" :
               "2.6rem";
}

function setExpr(text) {
  ui.displayExpr.textContent = text;
}

function refreshDisplay() {
  if (!state.resultShown) {
    setDisplay(state.expression || "0");
  }
}

// ── Score / Combo UI ───────────────────────────────────────
function updateScoreUI() {
  ui.scoreValue.textContent = state.score.toLocaleString();
  ui.calcsLabel.textContent = `Calcs: ${state.calcsDone}`;
  ui.bestCombo.textContent  = `Best combo: x${state.maxCombo}`;

  ui.scoreValue.classList.remove("bump");
  void ui.scoreValue.offsetWidth;          // force reflow
  ui.scoreValue.classList.add("bump");
  setTimeout(() => ui.scoreValue.classList.remove("bump"), 150);
}

function updateComboUI() {
  const colour =
    state.combo >= 5 ? "#ef4444" :
    state.combo >= 3 ? "#f59e0b" :
                       "#06b6d4";
  ui.comboBadge.textContent = `COMBO x${state.multiplier}`;
  ui.comboBadge.style.color = colour;
}

function setGlow(colour, resetDelay = 600) {
  ui.glowStrip.style.background  = colour;
  ui.glowStrip.style.boxShadow   = `0 4px 22px ${colour}99`;
  if (resetDelay) {
    setTimeout(() => {
      ui.glowStrip.style.background = "var(--accent)";
      ui.glowStrip.style.boxShadow  = "0 4px 18px rgba(124, 58, 237, 0.5)";
    }, resetDelay);
  }
}

// ── History ────────────────────────────────────────────────
function addHistory(expr, result) {
  state.history.unshift(`${expr} = ${result}`);
  state.history = state.history.slice(0, 5);
  ui.historyText.textContent = state.history.join("  |  ");
}

// ── Scoring ────────────────────────────────────────────────
function calcPoints(expr) {
  const ops = (expr.match(/[+\-*/]/g) || []).length;
  return Math.max(10, ops * 25 + expr.length * 2);
}

// ── Calculator Logic ───────────────────────────────────────
function clear() {
  state.expression  = "";
  state.resultShown = false;
  setDisplay("0");
  setExpr("");
  ui.glowStrip.style.background = "var(--accent)";
}

function negate() {
  try {
    // eslint-disable-next-line no-eval
    const val = eval(state.expression || "0");
    state.expression  = String(-val);
    state.resultShown = true;
  } catch (_) {}
}

function percent() {
  try {
    // eslint-disable-next-line no-eval
    const val = eval(state.expression || "0");
    state.expression  = String(val / 100);
    state.resultShown = true;
  } catch (_) {}
}

function appendChar(ch) {
  if (state.resultShown && !["+" , "-", "*", "/"].includes(ch)) {
    state.expression = "";
  }
  state.resultShown = false;
  state.expression += ch;
}

function evaluate() {
  if (!state.expression) return;
  try {
    const exprDisplay = state.expression.replace(/\*/g, "x");
    // eslint-disable-next-line no-eval
    const result = eval(state.expression);

    if (!isFinite(result)) throw new Error("Division by zero");

    const resultStr = Number.isInteger(result)
      ? String(result)
      : parseFloat(result.toPrecision(10)).toString();

    // Scoring
    const now = Date.now() / 1000;
    if (now - state.lastCorrect < 4) {
      state.combo++;
      state.multiplier = Math.min(state.combo + 1, 10);
    } else {
      state.combo      = 1;
      state.multiplier = 1;
    }
    state.maxCombo    = Math.max(state.maxCombo, state.combo);
    state.lastCorrect = now;

    const pts = calcPoints(state.expression) * state.multiplier;
    state.score     += pts;
    state.calcsDone++;

    addHistory(exprDisplay, resultStr);
    state.expression  = resultStr;
    state.resultShown = true;

    setExpr(`${exprDisplay} =`);
    setDisplay(resultStr);
    setGlow("#10b981");
    burst(ui.canvas.width / 2, ui.canvas.height / 2, "#10b981", 22);
    floatScore(pts);
    updateScoreUI();
    updateComboUI();

  } catch (err) {
    const msg = err.message.includes("zero") ? "DIVIDE BY 0" : "SYNTAX ERROR";
    showError(msg);
  }
}

function showError(msg) {
  setDisplay(msg);
  setExpr("");
  state.expression  = "";
  state.resultShown = false;
  state.combo       = 0;
  state.multiplier  = 1;
  setGlow("#ef4444", 800);
  burst(ui.canvas.width / 2, ui.canvas.height / 2, "#ef4444", 16);
}

function backspace() {
  if (!state.resultShown && state.expression.length > 0) {
    state.expression = state.expression.slice(0, -1);
    refreshDisplay();
  }
}

// ── Button Dispatch ────────────────────────────────────────
function handleButton(val) {
  burst(ui.canvas.width / 2, ui.canvas.height * 0.6, "#7c3aed", 6);

  switch (val) {
    case "C":   clear();       break;
    case "+/-": negate();      break;
    case "%":   percent();     break;
    case "=":   evaluate();    break;
    default:    appendChar(val); break;
  }
  refreshDisplay();
}

// ── Wire Up Buttons ────────────────────────────────────────
document.getElementById("btnGrid").addEventListener("click", (e) => {
  const btn = e.target.closest(".btn");
  if (!btn) return;
  handleButton(btn.dataset.val);
});

// ── Keyboard Support ───────────────────────────────────────
const keyMap = {
  Enter:     "=",
  Escape:    "C",
  Backspace: "__backspace__",
  "%":       "%",
};

document.addEventListener("keydown", (e) => {
  if (e.key === "Backspace") { backspace(); return; }

  const mapped = keyMap[e.key] ?? (
    "0123456789.+-*/".includes(e.key) ? e.key : null
  );
  if (mapped) handleButton(mapped);
});

// ── Live title update ──────────────────────────────────────
setInterval(() => {
  document.title = `Game Calculator | Score: ${state.score.toLocaleString()} | x${state.multiplier} Combo`;
}, 800);
