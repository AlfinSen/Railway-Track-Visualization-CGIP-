import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# --- 1. Setup & Functions ---
FOCAL_LENGTH = 2.0
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#87CEEB') # Outer background matches sky
ax.set_xlim(-2, 2); ax.set_ylim(-1, 2); ax.set_aspect('equal')
ax.axis('off')

# Sky and Ground with vibrant colors
ax.set_facecolor('#87CEEB') # Sky Blue
ax.fill_between([-3, 3], -2, 0, color='#4CAF50') # Lush Green Ground

# Sun & Clouds (Static Scenery)
ax.add_patch(patches.Circle((1.2, 1.5), 0.3, color='#FFD700', alpha=0.9)) # Sun
cloud_data = [(-1, 1.3, 0.4, 0.2), (-0.8, 1.4, 0.3, 0.15), (-1.2, 1.4, 0.3, 0.15),
              (1.5, 0.8, 0.5, 0.2), (1.2, 0.9, 0.3, 0.15), (1.7, 0.9, 0.3, 0.15)]
for cx, cy, rx, ry in cloud_data:
    ax.add_patch(patches.Ellipse((cx, cy), rx*2, ry*2, color='white', alpha=0.8))

def project(x, y, z):
    if z <= 0.1: return None, None
    f = FOCAL_LENGTH / z
    return x * f, y * f

def create_quad(x, y, z, w, h, color):
    # Vertices: bottom-left, bottom-right, top-right, top-left
    points = [
        project(x - w/2, y, z), project(x + w/2, y, z),
        project(x + w/2, y + h, z), project(x - w/2, y + h, z)
    ]
    if any(p[0] is None for p in points): return None
    return patches.Polygon(points, closed=True, color=color, ec='#333', lw=0.5)

# --- 2. Static World (Tracks & Trees) ---
# Tracks (Two parallel lines)
rail_z = np.linspace(1, 40, 50)
for dx in [-0.5, 0.5]:
    pts = [project(dx, -1, z) for z in rail_z]
    valid_pts = [p for p in pts if p[0] is not None]
    if valid_pts:
        xs, ys = zip(*valid_pts)
        ax.plot(xs, ys, color='#9E9E9E', linewidth=3, solid_capstyle='round')

# Sleepers (Crossbeams)
for z in range(1, 40, 2):
    p1 = project(-0.7, -1, z)
    p2 = project( 0.7, -1, z)
    if p1[0] and p2[0]:
        lw = max(1, 4 / z) # Thicker sleepers up close
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#795548', linewidth=lw, solid_capstyle='round')

# Pine Trees (Layered triangles)
for z in range(5, 40, 6):
    for x in [-2.5, 2.5]:
        trunk = create_quad(x, -1, z, 0.2, 0.5, '#5D4037')
        if trunk: ax.add_patch(trunk)
        
        # 3 layers of leaves for a nicer pine tree look
        for y_off, w_mult in [(0, 1.2), (0.4, 0.9), (0.8, 0.6)]:
            p_left = project(x - 0.5*w_mult, -0.5 + y_off, z)
            p_right = project(x + 0.5*w_mult, -0.5 + y_off, z)
            p_top = project(x, -0.5 + y_off + 0.8, z)
            if all(p[0] is not None for p in [p_left, p_right, p_top]):
                leaves = patches.Polygon([p_left, p_right, p_top], color='#2E7D32', ec='#1B5E20', lw=0.5)
                ax.add_patch(leaves)

# --- 3. Dynamic Train ---
# Format: (label, x_offset, y_offset, z_offset, width, height, color)
parts_def = [
    ('cabin',     0,   0,   0.5,  1.0, 1.2, '#1565C0'), # Blue Cabin
    ('roof',      0,   1.2, 0.5,  1.1, 0.1, '#FFC107'), # Yellow Roof
    ('body',      0,   0.1, 0,    0.8, 0.8, '#D32F2F'), # Red Boiler Body
    ('boiler',    0,   0.9, 0,    0.8, 0.1, '#FFC107'), # Yellow Trim
    ('chimney',   0,   0.9, -0.3, 0.25, 0.5, '#424242'), # Grey Chimney
    ('smoke_ring',0,   1.3, -0.3, 0.35, 0.1, '#FFC107'), # Yellow Chimney Tip
    ('light',     0,   0.5, -0.45,0.3, 0.3, '#FFF176'), # Bright light
    ('grill',     0,   0.1, -0.45,0.6, 0.3, '#757575'), # Grey grill
    ('wheel_fl', -0.45,-0.1, -0.2, 0.15, 0.35, '#212121'),
    ('wheel_fr',  0.45,-0.1, -0.2, 0.15, 0.35, '#212121'),
    ('wheel_bl', -0.45,-0.1,  0.3, 0.15, 0.35, '#212121'),
    ('wheel_br',  0.45,-0.1,  0.3, 0.15, 0.35, '#212121'),
]

train_patches = {}
for name, *_ in parts_def:
    p = patches.Polygon([[0,0]], color='white') # Placeholder
    ax.add_patch(p)
    train_patches[name] = p

def update(frame):
    # Move train from z=30 to z=2
    z_pos = 30.0 - (frame * 0.25) % 28.0
    
    # Add a slight bounce to the train body (but not the wheels)
    bounce = abs(np.sin(frame * 0.5)) * 0.05
    
    for name, dx, dy, dz, w, h, color in parts_def:
        # Apply bounce only to non-wheel parts
        actual_dy = dy + (bounce if 'wheel' not in name else 0)
        
        poly = create_quad(dx, -1 + actual_dy, z_pos + dz, w, h, color)
        patch = train_patches[name]
        
        if poly:
            patch.set_visible(True)
            patch.set_xy(poly.get_xy())
            patch.set_color(color)
            if name != 'light':
                patch.set_edgecolor('#111')
                patch.set_linewidth(1.0 if 'wheel' in name else 0.5)
            else:
                patch.set_edgecolor('none')
        else:
            patch.set_visible(False)
            
    return list(train_patches.values())

ani = animation.FuncAnimation(fig, update, frames=150, interval=40, blit=True)
print("Animation running... Close window to exit.")
plt.show(block=True)
