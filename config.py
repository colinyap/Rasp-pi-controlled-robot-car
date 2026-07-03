"""
All tunables, thresholds, and lookup tables.
Mutable dicts (HSV_RANGES) are modified in-place by calibration —
safe because calibration only runs in the main process.
"""

# ── Models ────────────────────────────────────────────────────────────────
SYMBOL_MODEL_PATH = "my_model_ncnn_model"
# Arrow direction is now resolved directly by the model (Arrow Left / Arrow Right).

# ── Motor tuning ──────────────────────────────────────────────────────────
BASESPEED  = 26
HARD_TURN  = 85
DEADZONE   = 80
KP_BLACK   = 0.35
KP_COLOR   = 0.85
KI         = 0
KD         = 0.05

# ── Camera / frame ────────────────────────────────────────────────────────
FRAME_W, FRAME_H = 300, 300
FRAME_BYTES      = FRAME_W * FRAME_H * 3
ROI_START        = 0.6
BLUR_K           = 5
THRESH_BLOCK     = 157
THRESH_C         = 40
MIN_AREA         = 500

# ── Symbol detection ──────────────────────────────────────────────────────
SYMBOL_CONF     = 0.6
SYMBOL_COOLDOWN = 6.0

# ── Arrow manoeuvre ───────────────────────────────────────────────────────
ARROW_HARD_TURN_TIME = 0.5    # seconds to hard-turn in arrow direction
ARROW_SEARCH_SPEED   = 85     # motor speed while spinning to find the line

# ── Arrow error bias (applied after the manoeuvre) ────────────────────────
TURN_BIAS_PX         = 45     # px bias added to the PID error
ARROW_BIAS_TIMEOUT   = 15.0   # seconds the bias stays active

# ── Colour line detection (red & yellow only) ─────────────────────────────
COLOR_PRIORITIES = ["black", "red", "yellow"]

HSV_RANGES = {
    "red":    [((0, 90, 60), (15, 255, 255)),
               ((165, 90, 60), (180, 255, 255))],
    "yellow": [((20, 100, 100), (35, 255, 255))],
}

LINE_DRAW_COLOR = {
    "black":  (0, 165, 60),
    "red":    (55, 55, 210),
    "yellow": (0, 200, 230),
}

# ── GPIO pins ─────────────────────────────────────────────────────────────
ENB, IN3, IN4 = 14, 15, 18
ENA, IN1, IN2 = 17, 4, 27
PWM_FREQ      = 1000

# ── Debug defaults ────────────────────────────────────────────────────────
DBG_CONSOLE  = False
DBG_LOG      = False
DBG_OVERLAY  = True
LOG_INTERVAL = 0.5

# ── Label maps ────────────────────────────────────────────────────────────
# The model directly classifies Arrow Left and Arrow Right.
# On detection the robot hard-turns in that direction for 0.5 s,
# then spins the opposite way until the line is reacquired,
# then applies an error bias for 15 s.
LABEL_MAP = {
    0: None,
    1: "Arrow Left",    2: "Arrow Right",
    3: "Cross",         4: "Semi Circle",    5: "Hazard",     6: "Green Hand",
    7: "Star",          8: "Diamond",         9: "QR Code",  10: "Quarter Circle",
   11: "Trapezoid",    12: "Octagon",        13: "Fingerprint", 14: "Recycle",
}
LABEL_TO_ID = {v: k for k, v in LABEL_MAP.items() if v is not None}

ARROW_SYMBOLS = {"Arrow Left", "Arrow Right"}

NON_ARROW_SYMBOLS = {
    "Cross", "Semi Circle", "Hazard", "Green Hand",
    "Star", "Diamond", "QR Code", "Quarter Circle",
    "Trapezoid", "Octagon", "Fingerprint", "Recycle",
}
