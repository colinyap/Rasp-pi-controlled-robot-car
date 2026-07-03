[Uploading linefollower-README.md…]()
# Autonomous Line-Following Robot (Raspberry Pi + YOLO)

A multiprocessing autonomous robot for the Raspberry Pi that follows a coloured or black line, recognises printed symbols with a YOLO model to trigger manoeuvres, and performs on-the-fly face recognition when it encounters a QR code or fingerprint marker. Includes a live HUD overlay, click-to-calibrate colour detection, and CSV telemetry logging.

## Overview

The robot's camera feed drives two things simultaneously: a classic PID line-follower and a YOLO symbol classifier, running in **separate processes** so heavy AI inference never blocks the tight control loop that keeps the robot on the line.

```
┌─────────────┐  shared memory   ┌───────────────────────┐
│  camera.py   │ ───────────────► │   main.py              │
│ (subprocess) │    (frame)       │  - PID line follow      │
└─────────────┘                  │  - motor control          │
                                  │  - overlay / HUD           │
┌─────────────┐  shared value(s)  │  - symbol dispatch          │
│   ai.py      │ ───────────────► │  - debug / logging           │
│ (subprocess) │  (label + conf)  └───────────────────────┘
└─────────────┘
```

- **`camera.py`** continuously captures frames from a Pi Camera and writes them into a POSIX shared-memory buffer.
- **`ai.py`** reads frames from that same buffer and runs YOLO (via `ultralytics`, NCNN-exported model) to classify track symbols, publishing the winning label/confidence through shared `multiprocessing.Value`s.
- **`main.py`** is the primary process: it reads frames, runs line detection, computes PID steering, drives the motors, polls for new AI detections, dispatches symbol behaviours, and renders the debug HUD — all in one tight loop.

This process split means the line-following control loop keeps running at full speed regardless of how long a YOLO inference pass takes.

## Features

- **Dual-mode line detection** — colour-based (red/yellow via HSV thresholding) with automatic fallback to black-line detection via adaptive thresholding, selectable at runtime.
- **PID steering** with separate gain profiles for colour vs. black-line tracking, plus a deadzone that triggers a hard turn instead of a gentle correction when the line is far off-centre.
- **Symbol-triggered behaviours** — a YOLO model classifies markers on the track (arrows, hazard signs, shapes, QR codes, etc.) and the robot executes a matching manoeuvre:
  - **Arrow Left / Arrow Right** — hard turn in that direction, spin back until the line is reacquired, then apply a steering bias for several seconds to favour that direction at forks.
  - **Hazard / Green Hand** — stop briefly.
  - **QR Code / Fingerprint** — stop and run face recognition against a small known-faces gallery.
  - **Recycle** — spin-in-place manoeuvre.
  - **Cross / Octagon / Star / Diamond / Trapezoid / Quarter Circle / Semi Circle** — brief stop-and-acknowledge (hook point for custom behaviours).
- **Click-to-calibrate colour ranges** — click on the live preview to sample HSV values under actual lighting conditions and rebuild the red/yellow detection range on the fly.
- **Live HUD overlay** — steering bar, detected line crosshair, active bias indicator, FPS counter, and an optional debug panel with raw PID terms.
- **Telemetry** — optional console logging and CSV data logging (timestamp, error, PID terms, motor speeds, FPS, contour stats) for tuning and post-run analysis.
- **Clean shutdown** — releases GPIO, shared memory, subprocesses, and OpenCV windows on exit or `Ctrl+C`.

## Hardware / Requirements

- Raspberry Pi (with Pi Camera Module) running Raspberry Pi OS
- Dual-motor chassis driven through an H-bridge (e.g. L298N) on GPIO pins (BCM `14, 15, 18` and `17, 4, 27` by default — see `config.py`)
- Python 3, with:
  - `picamera2`
  - `opencv-python`
  - `numpy`
  - `RPi.GPIO`
  - `ultralytics` (YOLO inference)
  - `simple-pid`
  - `face_recognition`
- A trained/exported YOLO symbol-detection model in NCNN format (path set via `SYMBOL_MODEL_PATH` in `config.py`)
- (Optional, for face recognition) reference photos named to match the entries in `symbols.py`'s `known_files` list

## Project Structure

Running the generator script produces the following package:

```
linefollower/
├── __init__.py        
├── __main__.py         # entry point: python -m linefollower
├── config.py           # all tunables, GPIO pins, HSV ranges, label maps
├── shm.py              # POSIX SharedMemory frame buffer helpers
├── camera.py           # camera capture subprocess
├── ai.py                # YOLO symbol-detection subprocess
├── motors.py           # GPIO setup, set_motors, stop, cleanup
├── vision.py           # find_line — colour + black-line detection, turn-bias aware
├── symbols.py          # handle_symbol dispatch + face recognition routine
├── calibration.py      # click-to-sample HSV calibration
├── overlay.py          # HUD + debug panel drawing
├── debug.py            # console telemetry + CSV logging
└── main.py             # main control loop
```

## Getting Started

### 1. Generate the package

```bash
python setup_project.py
```

This scaffolds the entire `linefollower/` package described above in the current directory.

### 2. Install dependencies

```bash
pip install opencv-python numpy RPi.GPIO ultralytics simple-pid face_recognition picamera2
```

### 3. Configure

Open `linefollower/config.py` and adjust to match your build:
- `SYMBOL_MODEL_PATH` — path to your exported YOLO model
- `ENA/IN1/IN2`, `ENB/IN3/IN4` — motor driver GPIO pins
- `BASESPEED`, `KP_BLACK`, `KP_COLOR`, `KI`, `KD` — PID/speed tuning
- `HSV_RANGES` — starting colour thresholds (refine live with the calibration tool)

### 4. Run

```bash
python -m linefollower
```

## Runtime Controls

The live OpenCV preview window accepts keyboard input:

| Key | Action |
|---|---|
| `q` | Quit |
| `s` | Save a snapshot of the current frame |
| `t` | Toggle the black/white threshold view window |
| `d` | Toggle console telemetry |
| `l` | Toggle CSV logging |
| `v` | Toggle the on-screen debug panel |
| `c` | Cycle line-detection colour priority (black → red → yellow) |
| `k` | Toggle HSV calibration mode |
| `1` / `2` | (in calibration mode) target red / yellow for the next samples |
| `a` | (in calibration mode) apply collected samples as the new HSV range |

## How Symbol Detection Feeds Into Control

1. `ai.py` runs YOLO on each frame and, once a label clears the confidence threshold and its per-label cooldown has elapsed, publishes it via shared memory.
2. `main.py` polls that shared state once per loop iteration. If a new label is present, it stops the robot and calls `handle_symbol()`, which runs the corresponding manoeuvre (blocking, since the robot's actions must complete before line-following resumes).
3. For arrow symbols specifically, after the manoeuvre finishes and the line is reacquired, a pixel-offset **steering bias** is applied to the PID error for a configurable window (`ARROW_BIAS_TIMEOUT`), nudging the robot to favour that branch at an upcoming fork rather than snapping straight back to centre.

## Tuning Reference

All of the following live in `config.py`:

| Parameter | Purpose |
|---|---|
| `BASESPEED` | Base forward motor speed (0–100) |
| `HARD_TURN` | Motor speed used when the line error exceeds the deadzone |
| `DEADZONE` | Pixel error threshold before switching from PID to hard-turn mode |
| `KP_BLACK` / `KP_COLOR` | PID proportional gain, black-line vs colour-line tracking |
| `KI` / `KD` | PID integral / derivative gains |
| `ROI_START` | Fraction of frame height where the line-detection region of interest begins |
| `MIN_AREA` | Minimum contour area to be considered a valid line segment |
| `SYMBOL_CONF` | Minimum YOLO confidence to act on a detection |
| `SYMBOL_COOLDOWN` | Minimum seconds between repeated triggers of the same symbol |
| `ARROW_HARD_TURN_TIME` / `ARROW_SEARCH_SPEED` | Arrow manoeuvre timing/speed |
| `TURN_BIAS_PX` / `ARROW_BIAS_TIMEOUT` | Post-manoeuvre steering bias magnitude and duration |

## Author

Built by Colin Yap Ren Feng as an autonomous robotics project combining classical PID control with real-time YOLO-based symbol recognition on a Raspberry Pi.
