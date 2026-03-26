# CGIP Project: Perspective Railway and Animated Train

A small computer-graphics project in Python using Matplotlib and NumPy.

This repository contains:
- A static perspective railway scene renderer
- A dynamic animated train moving toward the camera in a loop
- A launcher shell script that runs the animation from a local virtual environment

## What This Project Demonstrates

- 3D-to-2D perspective projection with a focal-length model
- Primitive scene composition with Matplotlib patches
- Manual line rasterization (Bresenham) for railway geometry in the animated scene
- Frame-by-frame animation with reusable patch objects for better performance
- Simple procedural motion (train bounce) driven by a sine-based signal

## Project Structure

- `animated_train.py`: Real-time train animation with static scenery (sky, sun, clouds, trees, rails)
- `railway_track.py`: Generates a static perspective railway image and saves it as `railway_track.png`
- `start_animation.sh`: Runs `animated_train.py` using `./.venv/bin/python3`
- `CODE_EXPLANATION.md`: Detailed technical walkthrough of the animation and rendering approach

## Requirements

- macOS (or any OS with Python support)
- Python 3.9+ (3.10+ recommended)
- pip
- Python packages:
  - matplotlib
  - numpy

## Quick Start (Recommended)

### 1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install matplotlib numpy
```

### 3) Run the animation

Option A (launcher script):

```bash
chmod +x start_animation.sh
./start_animation.sh
```

Option B (direct Python command):

```bash
python3 animated_train.py
```

### 4) Generate the static railway image

```bash
python3 railway_track.py
```

Expected output file:
- `railway_track.png`

## How the Rendering Works

### 1) Perspective Projection

Both programs use a projection model:

- Input point in 3D: `(x, y, z)`
- Projection factor: `f / z`
- Screen point: `(x * f / z, y * f / z)`

As depth `z` increases, objects appear smaller and move toward the scene center, producing perspective.

### 2) Scene Composition

The scene is built from simple shapes:
- `Polygon` for train/body geometry
- `Circle` and `Ellipse` for sun/clouds
- Lines for rails and sleepers
- Triangles and quads for trees

### 3) Animation Strategy

In `animated_train.py`:
- Static background objects are created once
- Train parts are defined in a reusable blueprint list (`parts_def`)
- Patch objects are reused and updated each frame (instead of recreated)
- Train depth (`z`) decreases over time to simulate approach
- Modulo wraps depth to create an infinite loop
- Non-wheel parts receive vertical bounce for a rattling effect

### 4) Rasterized Track Lines (Animated Scene)

The animation script includes a Bresenham line implementation to generate stable point sequences for rail/sleeper rendering from projected endpoints.

## Running Notes

- The animation opens a Matplotlib window and blocks until you close it.
- If the animation window appears but does not refresh, verify your Matplotlib backend and local GUI support.
- The shell launcher expects `.venv` at the project root.

## Troubleshooting

### Script fails with "No such file or directory: ./.venv/bin/python3"

Cause:
- Virtual environment has not been created in project root.

Fix:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib numpy
```

### `ModuleNotFoundError` for `matplotlib` or `numpy`

Cause:
- Dependencies not installed in the interpreter you are using.

Fix:
```bash
source .venv/bin/activate
pip install matplotlib numpy
```

### macOS GUI/backend issues (blank or non-responsive window)

Try:
- Running from a normal terminal session (not a restricted remote shell)
- Ensuring your Python and Matplotlib are installed in the same environment
- Testing with:

```bash
python3 -c "import matplotlib; print(matplotlib.get_backend())"
```

If needed, you can set a backend explicitly in code before importing `pyplot`.

## Suggested Improvements

- Add a `requirements.txt` for one-command dependency install
- Add CLI flags for speed, focal length, and output dimensions
- Export animation as GIF/MP4 (e.g., using Matplotlib writers)
- Add unit tests for `project()` and Bresenham line logic
- Split rendering utilities into a shared module for reuse

## License

No license file is currently present. Add a `LICENSE` file if you plan to publish or share this project publicly.
