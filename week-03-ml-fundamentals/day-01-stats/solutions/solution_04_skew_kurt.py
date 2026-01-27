import numpy as np
from scipy import stats

np.random.seed(42)

# 1. Normal Dataset
normal_data = np.random.normal(100, 10, 1000)

# 2. Outlier Heavy Dataset (Right Skewed)
# Normal data + 50 points ranging from 500ms to 2000ms
outliers = np.random.uniform(500, 2000, 50)
outlier_heavy_data = np.concatenate([normal_data, outliers])

def analyze_shape(name, data):
    print(f"--- Dataset: {name} ---")
    print(f"Mean:      {np.mean(data):.2f}")
    print(f"Median:    {np.median(data):.2f}")
    print(f"Std Dev:   {np.std(data):.2f}")
    print(f"Skewness:  {stats.skew(data):.2f}")
    print(f"Kurtosis:  {stats.kurtosis(data):.4f}\n")

analyze_shape("Normal (Stable System)", normal_data)
analyze_shape("Outlier Heavy (Unstable System)", outlier_heavy_data)

print("--- Discussion ---")
print("1. Why did Mean jump significantly (100 -> 145) while Median stayed the same?")
print("   Answer: Mean is highly sensitive to outliers. Median is robust.")
print("2. Why does Skewness > 0 in the heavy dataset?")
print("   Answer: It indicates the distribution is pulled to the right by slow requests (The Tail).")
print("3. Why is high Kurtosis a warning sign for AIOps?")
print("   Answer: It means you have a 'Leptokurtic' distribution—meaning outliers happen far more frequently")
print("   than predicted by a Normal model. This causes False Negatives in simple '3-sigma' alerts.")
