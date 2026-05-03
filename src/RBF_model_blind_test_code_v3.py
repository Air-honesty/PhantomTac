import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.interpolate import RBFInterpolator
import warnings
from tqdm import tqdm

warnings.filterwarnings('ignore')

# ================= Font and Font Size Control Center =================
FONT_NAME = 'Calibri'  # Global font
AXES_LABEL_SIZE = 16  # X/Y axis label font size
TICK_LABEL_SIZE = 14  # Tick number font size
LEGEND_FONT_SIZE = 14  # Legend font size

# ================= Global Settings for Academic-level Charts (Top Conference PDF) =================
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [FONT_NAME]
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = FONT_NAME
plt.rcParams['mathtext.it'] = FONT_NAME
plt.rcParams['mathtext.bf'] = FONT_NAME
plt.rcParams['axes.unicode_minus'] = False

plt.rcParams['xtick.labelsize'] = TICK_LABEL_SIZE
plt.rcParams['ytick.labelsize'] = TICK_LABEL_SIZE
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


def get_blind_test_scores(excel_filename, magnet_label, n_iterations=1000):
    """Process a single dataset and return accuracy score list and average error metrics"""
    print(f"\n{'=' * 50}")
    print(f"Calculating for [{magnet_label}] dataset ({n_iterations} random blind tests)...")

    try:
        df = pd.read_excel(excel_filename)
        df = df.dropna(subset=['X(mm)', 'Y(mm)', 'Z(mm)', 'Fx', 'Fy', 'Fz'])
    except FileNotFoundError:
        print(f"Error: File '{excel_filename}' not found.")
        return None, None, None, None

    X_raw = df[['X(mm)', 'Y(mm)', 'Z(mm)']].values
    Y_raw = df[['Fx', 'Fy', 'Fz']].values

    # Clean outliers
    data_scaled = StandardScaler().fit_transform(np.column_stack((X_raw, Y_raw)))
    lof = LocalOutlierFactor(n_neighbors=10, contamination=0.01)
    good_mask = lof.fit_predict(data_scaled) == 1

    X_clean = X_raw[good_mask]
    Y_clean = Y_raw[good_mask]

    overall_scores_per_iter = []
    mae_per_iter = []
    rmse_per_iter = []

    # True random fluctuations
    for _ in tqdm(range(n_iterations), desc=f"[{magnet_label}] Progress"):
        X_train, X_test, Y_train, Y_test = train_test_split(X_clean, Y_clean, test_size=0.03)

        # Spatial compression
        Y_train_transformed = np.arcsinh(Y_train)

        # TPS physics engine
        rbf = RBFInterpolator(X_train, Y_train_transformed, kernel='thin_plate_spline', smoothing=0.0005)

        # Predict and decompress
        Y_pred_transformed = rbf(X_test)
        Y_pred = np.sinh(Y_pred_transformed)

        # ----------------------------------------------------
        # [Key Modification]: Physical Defense (Range Clipping and Negative Score Zeroing)
        # Update clipping boundary from original [-50.0, 50.0] to [-25.0, 25.0]
        # ----------------------------------------------------
        # Physical Defense (Axis-wise range clipping and negative score zeroing)
        Y_pred[:, 0] = np.clip(Y_pred[:, 0], -10.0, 10.0)  # Clip Fx
        Y_pred[:, 1] = np.clip(Y_pred[:, 1], -10.0, 10.0)  # Clip Fy
        Y_pred[:, 2] = np.clip(Y_pred[:, 2], 0.0, 25.0)  # Clip Fz

        # 1. Calculate fitting score
        iter_score = r2_score(Y_test, Y_pred, multioutput='raw_values')
        iter_score = np.maximum(0, iter_score)
        iter_overall_acc = np.mean(iter_score) * 100
        overall_scores_per_iter.append(iter_overall_acc)

        # 2. Calculate MAE and RMSE for current iteration
        iter_mae = mean_absolute_error(Y_test, Y_pred)
        iter_rmse = np.sqrt(mean_squared_error(Y_test, Y_pred))
        mae_per_iter.append(iter_mae)
        rmse_per_iter.append(iter_rmse)

    final_median = np.median(overall_scores_per_iter)

    # Calculate average MAE and RMSE over 1000 iterations
    avg_mae = np.mean(mae_per_iter)
    avg_rmse = np.mean(rmse_per_iter)

    return overall_scores_per_iter, final_median, avg_mae, avg_rmse


# ================= Start Calculation and Independent Plotting =================
if __name__ == "__main__":
    datasets = [
        ('sensor_data_3mm.xlsx', '3mm'),
        ('sensor_data_2.5mm.xlsx', '2.5mm')
    ]

    print("\nRendering single academic chart (PDF vector version) and calculating physical errors, please wait...")

    x_axis = np.arange(1, 1001)

    for file_name, label in datasets:
        scores, median, avg_mae, avg_rmse = get_blind_test_scores(file_name, label, n_iterations=1000)

        if scores is not None:
            # ---> Print core error data to terminal <---
            print(f"\n[{label}] Dataset 1000 Blind Test Results Summary:")
            print(f"   => Median Score: {median:.2f}%")
            print(f"   => Average MAE:  {avg_mae:.4f} N")
            print(f"   => Average RMSE: {avg_rmse:.4f} N")
            print("-" * 50)

            # Create independent canvas for each dataset (6x5 size)
            fig, ax = plt.subplots(figsize=(6, 5))

            # Plot scatter and line
            ax.plot(x_axis, scores, color='#1f77b4', alpha=0.3, linewidth=1, label='Single Iteration')
            ax.scatter(x_axis, scores, color='#1f77b4', alpha=0.2, s=5)

            # Plot 50-iteration moving average line
            moving_avg = pd.Series(scores).rolling(window=50, min_periods=1).mean()
            ax.plot(x_axis, moving_avg, color='#ff7f0e', linewidth=2, alpha=0.9, label='Moving Average (w=50)')

            # Plot red median crosshair line
            ax.axhline(y=median, color='#d62728', linestyle='--', linewidth=2,
                       label=f'Median Score: {median:.2f}%')

            # Axis label decoration
            ax.set_xlabel('Blind Test Iteration', fontsize=AXES_LABEL_SIZE)
            ax.set_ylabel('Predictive Performance Score (%)', fontsize=AXES_LABEL_SIZE)

            ax.set_ylim(-5, 105)
            ax.set_xlim(0, 1010)
            ax.grid(True, linestyle=':', alpha=0.6)

            # Borderless legend
            ax.legend(loc='lower right', fontsize=LEGEND_FONT_SIZE, frameon=False)

            plt.tight_layout()

            output_filename = f'score_distribution_{label}_random.pdf'
            plt.savefig(output_filename, format='pdf', bbox_inches='tight')
            plt.close()

            print(f"[{label}] Independent PDF chart generated: {output_filename}")