import numpy as np
import matplotlib.pyplot as plt
import joblib
import warnings

warnings.filterwarnings('ignore')

# ================= Font and Font Size Control Center =================
FONT_NAME = 'Arial'  # Use Arial to ensure smooth lines
AXIS_LABEL_SIZE = 22  # Axis label font size
TICK_LABEL_SIZE = 18  # Tick number font size
COLORBAR_LABEL_SIZE = 22  # Colorbar label font size

# ================= Global Settings for Academic Plots =================
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [FONT_NAME]
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['svg.fonttype'] = 'path'

def plot_for_ppt_clean():
    print("\nGenerating 'path-based' unbolded SVG, adapting to PPT proportions...")
    FIXED_Z = 0.2

    try:
        engine = joblib.load('ultimate_rbf_engine_3mm.pkl')
    except:
        print("Failed to load model, please check the file name.")
        return

    # Generate scanning grid
    scan_range = np.linspace(-6, 6, 200)
    X_grid, Y_grid = np.meshgrid(scan_range, scan_range)
    X_input = np.column_stack((X_grid.ravel(), Y_grid.ravel(), np.full_like(X_grid.ravel(), FIXED_Z)))

    # Inference calculation
    F_real = np.sinh(engine(X_input))
    Fx = F_real[:, 0].reshape(X_grid.shape)
    Fy = F_real[:, 1].reshape(X_grid.shape)
    Fz = F_real[:, 2].reshape(X_grid.shape)

    data_list = [('Fx', Fx), ('Fy', Fy), ('Fz', np.abs(Fz))]

    for name, data in data_list:
        # Create large-size canvas
        fig = plt.figure(figsize=(10, 8), dpi=100)
        ax = fig.add_subplot(111)

        # Draw heatmap
        surf = ax.contourf(X_grid, Y_grid, data, levels=25, cmap='jet')
        # Draw background contour lines
        ax.contour(X_grid, Y_grid, data, levels=10, colors='black', linewidths=0.5, alpha=0.3)

        # --- Axis formatting (removed fontweight='bold') ---
        ax.set_aspect('equal')
        ax.set_xlabel("X (mm)", fontsize=AXIS_LABEL_SIZE)
        ax.set_ylabel("Y (mm)", fontsize=AXIS_LABEL_SIZE)

        # Set tick number size
        ax.tick_params(axis='both', which='major', labelsize=TICK_LABEL_SIZE)

        ax.set_xticks(np.arange(-6, 7, 2))
        ax.set_yticks(np.arange(-6, 7, 2))
        ax.grid(True, linestyle=':', alpha=0.4)

        # White central reference line
        ax.axhline(0, color='white', linewidth=1, alpha=0.5)
        ax.axvline(0, color='white', linewidth=1, alpha=0.5)

        # Colorbar settings
        cbar = fig.colorbar(surf, ax=ax)
        cbar.set_label('Force (N)', size=COLORBAR_LABEL_SIZE)
        cbar.ax.tick_params(labelsize=TICK_LABEL_SIZE)

        # Save with new version filename
        save_name = f'ppt_clean_{name}_v4.svg'
        plt.savefig(save_name, format='svg', bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    plot_for_ppt_clean()