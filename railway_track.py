import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def project(x, y, z, f=2.0):
    """3D to 2D projection."""
    if z <= 0.1: return None, None
    factor = f / z
    return x * factor, y * factor

def create_quad(ax, x, y, z, w, h, color, f=2.0):
    """Creates a 2D polygon from 3D rectangle coordinates on the given axes."""
    points = [
        project(x - w/2, y, z, f), project(x + w/2, y, z, f),
        project(x + w/2, y + h, z, f), project(x - w/2, y + h, z, f)
    ]
    if any(p[0] is None for p in points): return None
    poly = patches.Polygon(points, closed=True, color=color, ec='#333', lw=0.5)
    ax.add_patch(poly)
    return poly

def main():
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

    # Tracks (Two parallel lines)
    focal_length = 2.0
    rail_z = np.linspace(1, 40, 50)
    for dx in [-0.5, 0.5]:
        pts = [project(dx, -1, z, focal_length) for z in rail_z]
        valid_pts = [p for p in pts if p[0] is not None]
        if valid_pts:
            xs, ys = zip(*valid_pts)
            ax.plot(xs, ys, color='#9E9E9E', linewidth=3, solid_capstyle='round')

    # Sleepers (Crossbeams)
    for z in range(1, 40, 2):
        p1 = project(-0.7, -1, z, focal_length)
        p2 = project( 0.7, -1, z, focal_length)
        if p1[0] and p2[0]:
            lw = max(1, 4 / z) # Thicker sleepers up close
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#795548', linewidth=lw, solid_capstyle='round')

    # Pine Trees (Layered triangles)
    for z in range(5, 40, 6):
        for x in [-2.5, 2.5]:
            # Trunk
            create_quad(ax, x, -1, z, 0.2, 0.5, '#5D4037', f=focal_length)
            
            # 3 layers of leaves for a nicer pine tree look
            for y_off, w_mult in [(0, 1.2), (0.4, 0.9), (0.8, 0.6)]:
                p_left = project(x - 0.5*w_mult, -0.5 + y_off, z, focal_length)
                p_right = project(x + 0.5*w_mult, -0.5 + y_off, z, focal_length)
                p_top = project(x, -0.5 + y_off + 0.8, z, focal_length)
                if all(p[0] is not None for p in [p_left, p_right, p_top]):
                    leaves = patches.Polygon([p_left, p_right, p_top], color='#2E7D32', ec='#1B5E20', lw=0.5)
                    ax.add_patch(leaves)

    # Save the plot
    output_file = 'railway_track.png'
    # Use bbox_inches='tight' with no empty borders and set background to matched facecolor
    plt.savefig(output_file, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0.1)
    print(f"Visualization saved to {output_file}")
    
if __name__ == "__main__":
    main()
