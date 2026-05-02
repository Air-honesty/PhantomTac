import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from scipy.interpolate import RBFInterpolator
import joblib
import warnings
import os
warnings.filterwarnings('ignore')

def build_and_save_ultimate_model(excel_filename, magnet_label):
    print(f"\n{'=' * 50}")
    print(f"Building and archiving the ultimate physical engine for [{magnet_label}]...")

    # 1. Read data
    try:
        df = pd.read_excel(excel_filename)
        df = df.dropna(subset=['X(mm)', 'Y(mm)', 'Z(mm)', 'Fx', 'Fy', 'Fz'])
    except FileNotFoundError:
        print(f"Error: File '{excel_filename}' not found. Skipping current specification.")
        return False

    X_raw = df[['X(mm)', 'Y(mm)', 'Z(mm)']].values
    Y_raw = df[['Fx', 'Fy', 'Fz']].values

    # 2. Strict physical background noise cleaning (remove 1% abnormal glitches)
    data_scaled = StandardScaler().fit_transform(np.column_stack((X_raw, Y_raw)))
    lof = LocalOutlierFactor(n_neighbors=10, contamination=0.01)
    good_mask = lof.fit_predict(data_scaled) == 1

    X_clean = X_raw[good_mask]
    Y_clean = Y_raw[good_mask]

    print(f"Data cleaning completed: Original points {len(X_raw)} -> Valid points {len(X_clean)}")
    print(f"Using 100% of valid data for full-scale fitting...")

    # 3. Core mathematical transformation: inverse hyperbolic sine (arcsinh) space compression on real force field
    Y_clean_transformed = np.arcsinh(Y_clean)

    # 4. Ultimate model construction (TPS kernel + extreme smoothness)
    # No longer split training/test sets here, feed all valid points to the algorithm
    final_rbf_engine = RBFInterpolator(
        X_clean,
        Y_clean_transformed,
        kernel='thin_plate_spline',
        smoothing=0.0005
    )

    # 5. Model archiving and persistence
    model_filename = f"ultimate_rbf_engine_{magnet_label}.pkl"
    joblib.dump(final_rbf_engine, model_filename)

    print(f"Ultimate digital twin model has been successfully archived to: {model_filename}")
    return True


# ================= Start batch generation program =================
if __name__ == "__main__":
    # Configure your 3 sets of data list
    datasets = [
        ('sensor_data_3mm_S.xlsx', '3mm'),
        ('sensor_data_2.5mm_S.xlsx', '2.5mm'),
    ]
    success_count = 0
    for file_name, label in datasets:
        if build_and_save_ultimate_model(file_name, label):
            success_count += 1