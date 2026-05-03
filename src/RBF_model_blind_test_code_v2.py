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

# ================= 字体与字号控制中心 =================
FONT_NAME = 'Calibri'  # 全局字体
AXES_LABEL_SIZE = 16  # X/Y 轴标签字号
TICK_LABEL_SIZE = 14  # 刻度数字字号
LEGEND_FONT_SIZE = 14  # 图例字号

# ================= 学术级图表全局设置 (顶会 PDF 专用) =================
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
    """处理单个数据集，返回精度得分列表及平均误差指标"""
    print(f"\n{'=' * 50}")
    print(f"🚀 正在计算 [{magnet_label}] 数据集 ({n_iterations}次随机盲测)...")

    try:
        df = pd.read_excel(excel_filename)
        df = df.dropna(subset=['X(mm)', 'Y(mm)', 'Z(mm)', 'Fx', 'Fy', 'Fz'])
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 '{excel_filename}'。")
        return None, None, None, None

    X_raw = df[['X(mm)', 'Y(mm)', 'Z(mm)']].values
    Y_raw = df[['Fx', 'Fy', 'Fz']].values

    # 清洗异常值
    data_scaled = StandardScaler().fit_transform(np.column_stack((X_raw, Y_raw)))
    lof = LocalOutlierFactor(n_neighbors=10, contamination=0.01)
    good_mask = lof.fit_predict(data_scaled) == 1

    X_clean = X_raw[good_mask]
    Y_clean = Y_raw[good_mask]

    overall_scores_per_iter = []
    mae_per_iter = []
    rmse_per_iter = []

    # 真实随机波动
    for _ in tqdm(range(n_iterations), desc=f"[{magnet_label}] 进度"):
        X_train, X_test, Y_train, Y_test = train_test_split(X_clean, Y_clean, test_size=0.03)

        # 空间压缩
        Y_train_transformed = np.arcsinh(Y_train)

        # TPS 物理引擎
        rbf = RBFInterpolator(X_train, Y_train_transformed, kernel='thin_plate_spline', smoothing=0.0005)

        # 预测并解压
        Y_pred_transformed = rbf(X_test)
        Y_pred = np.sinh(Y_pred_transformed)

        # ----------------------------------------------------
        # 【关键修改】：物理防御 (量程裁剪与负分归零)
        # 将裁剪边界从原来的 [-50.0, 50.0] 更新为 [-25.0, 25.0]
        # ----------------------------------------------------
        # 物理防御 (分轴量程裁剪与负分归零)
        Y_pred[:, 0] = np.clip(Y_pred[:, 0], -10.0, 10.0)  # 裁剪 Fx
        Y_pred[:, 1] = np.clip(Y_pred[:, 1], -10.0, 10.0)  # 裁剪 Fy
        Y_pred[:, 2] = np.clip(Y_pred[:, 2], 0.0, 25.0)  # 裁剪 Fz

        # 1. 计算拟合得分 Score
        iter_score = r2_score(Y_test, Y_pred, multioutput='raw_values')
        iter_score = np.maximum(0, iter_score)
        iter_overall_acc = np.mean(iter_score) * 100
        overall_scores_per_iter.append(iter_overall_acc)

        # 2. 计算当前轮的 MAE 和 RMSE
        iter_mae = mean_absolute_error(Y_test, Y_pred)
        iter_rmse = np.sqrt(mean_squared_error(Y_test, Y_pred))
        mae_per_iter.append(iter_mae)
        rmse_per_iter.append(iter_rmse)

    final_median = np.median(overall_scores_per_iter)

    # 计算 1000 轮的平均绝对误差和均方根误差
    avg_mae = np.mean(mae_per_iter)
    avg_rmse = np.mean(rmse_per_iter)

    return overall_scores_per_iter, final_median, avg_mae, avg_rmse


# ================= 启动计算与独立绘图 =================
if __name__ == "__main__":
    datasets = [
        ('sensor_data_3mm.xlsx', '3mm'),
        ('sensor_data_2.5mm.xlsx', '2.5mm')
    ]

    print("\n🎨 正在渲染单张学术图表 (PDF矢量版) 并计算物理误差，请稍候...")

    x_axis = np.arange(1, 1001)

    for file_name, label in datasets:
        scores, median, avg_mae, avg_rmse = get_blind_test_scores(file_name, label, n_iterations=1000)

        if scores is not None:
            # ---> 终端打印核心误差数据 <---
            print(f"\n📊 [{label}] 数据集 1000次盲测结果汇总:")
            print(f"   => Median Score: {median:.2f}%")
            print(f"   => Average MAE:  {avg_mae:.4f} N")
            print(f"   => Average RMSE: {avg_rmse:.4f} N")
            print("-" * 50)

            # 为每个数据集创建一张独立的画布 (6x5 尺寸)
            fig, ax = plt.subplots(figsize=(6, 5))

            # 画散点和折线
            ax.plot(x_axis, scores, color='#1f77b4', alpha=0.3, linewidth=1, label='Single Iteration')
            ax.scatter(x_axis, scores, color='#1f77b4', alpha=0.2, s=5)

            # 画 50 轮移动平均线
            moving_avg = pd.Series(scores).rolling(window=50, min_periods=1).mean()
            ax.plot(x_axis, moving_avg, color='#ff7f0e', linewidth=2, alpha=0.9, label='Moving Average (w=50)')

            # 画红色中位准星线
            ax.axhline(y=median, color='#d62728', linestyle='--', linewidth=2,
                       label=f'Median Score: {median:.2f}%')

            # 轴标签修饰
            ax.set_xlabel('Blind Test Iteration', fontsize=AXES_LABEL_SIZE)
            ax.set_ylabel('Predictive Performance Score (%)', fontsize=AXES_LABEL_SIZE)

            ax.set_ylim(-5, 105)
            ax.set_xlim(0, 1010)
            ax.grid(True, linestyle=':', alpha=0.6)

            # 无边框图例
            ax.legend(loc='lower right', fontsize=LEGEND_FONT_SIZE, frameon=False)

            plt.tight_layout()

            output_filename = f'score_distribution_{label}_random.pdf'
            plt.savefig(output_filename, format='pdf', bbox_inches='tight')
            plt.close()

            print(f"✅ [{label}] 的独立 PDF 图表已生成: {output_filename}")
