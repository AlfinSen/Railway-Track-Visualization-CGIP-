# Code Explanation: Vibrant Animated Train

This document explains the updated `animated_train.py` script. The code uses Python and `matplotlib` to create a scenic 3D-like animation with pleasing visuals, without being overly complex!

## 1. The Core Logic: `project(x, y, z)`

The entire 3D perspective effect relies on one simple function that converts 3D coordinates (x, y, z) into 2D screen coordinates.

```python
def project(x, y, z):
    if z <= 0.1: return None, None  # Don't draw if behind camera
    f = FOCAL_LENGTH / z            # Calculate scaling factor
    return x * f, y * f             # Scale x and y
```

-   **High `z` (Far away)** -> Small `f` -> Object looks small.
-   **Low `z` (Close up)** -> Large `f` -> Object looks big.

## 2. Drawing Shapes: `create_quad`

Instead of writing complex code for every rectangle, we use a helper function:
`create_quad(x, y, z, width, height, color)`

This function takes the center position and size of a rectangle in 3D, projects its 4 corners using `project()`, and returns a `Polygon` that Matplotlib can draw with a clean thin dark edge (`ec='#333'`).

## 3. The World (Static Scenery)

The background is made highly scenic to build a vibrant world:
-   **Sky & Ground**: We use `set_facecolor` for a sky `#87CEEB` (Sky Blue) and `fill_between` for a lush `#4CAF50` (Green) ground.
-   **Sun & Clouds**: Fixed, static `Circle` and `Ellipse` patches are drawn in the background using loops.
-   **Tracks**: Tracks are drawn as lines extending into `z`. The crossbeam sleepters dynamically adjust their line width `max(1, 4 / z)` based on how far away they are to enhance perspective.
-   **Pine Trees**: Trees are drawn using a rectangular trunk and a loop of 3 overlapping triangles (polygons) that act as layered leaves.

## 4. The Train (Dynamic)

The classical steam train components are defined using `parts_def` using a blue cabin, red boiler body, and bright yellow roof/trim.

## 5. The Animation Loop: `update(frame)`

This function runs for every frame:
1.  **Move Forward**: Calculates the new `z` position of the train (it moves closer each frame).
2.  **Choo-Choo Bounce**: A single sine wave, `np.sin(frame * 0.5) * 0.05`, serves as a subtle vertical bounce for the train's body as it moves, simulating motion without displacing the wheels off the track.
3.  **Redraw**: Updates the positions (`set_xy`) of all `train_patches`.

## 6. Running the Animation

```python
plt.show(block=True)
```

By ensuring no title exists, the window strictly focuses on edge-to-edge landscape art while `block=True` ensures the window reliably stays open across all operating systems.
