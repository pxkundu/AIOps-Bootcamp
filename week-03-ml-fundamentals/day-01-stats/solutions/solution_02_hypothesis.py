import numpy as np
from scipy import stats

np.random.seed(42)
# Version A (Baseline)
version_a = np.random.normal(100, 10, 100)
# Version B (Candidate)
version_b = np.random.normal(105, 12, 100)

print("--- Step 1: Normality Check ---")
# Shapiro-Wilk Test
_, p_a = stats.shapiro(version_a)
_, p_b = stats.shapiro(version_b)

print(f"Normality p-value (A): {p_a:.4f}")
print(f"Normality p-value (B): {p_b:.4f}")

if p_a > 0.05 and p_b > 0.05:
    print("Decision: Data is Normal. T-Test is appropriate.\n")
else:
    print("Decision: Data is NOT Normal. Mann-Whitney U is better.\n")


print("--- Step 2: Hypothesis Testing ---")
# Parametric Test
t_stat, t_pval = stats.ttest_ind(version_a, version_b)
# Non-Parametric Test
u_stat, u_pval = stats.mannwhitneyu(version_a, version_b)

print(f"Student's T-Test p-value: {t_pval:.4f}")
print(f"Mann-Whitney U p-value:   {u_pval:.4f}")

alpha = 0.05
if t_pval < alpha:
    print("\nRESULT: Statistically Significant! Version B is different.")
else:
    print("\nRESULT: Not Significant. The difference could be noise.")

print("\n--- AIOps Context ---")
print("1. Why Mann-Whitney U? Production latency is rarely normal. It has long tails.")
print("   Mann-Whitney works on 'Ranks' rather than raw values, making it robust to extreme outliers.")
print("2. P-Value = 0.08? We usually DON'T roll back for 'maybe' differences, but we stay on alert.")
print("   In AIOps, we often use more strict significance (0.01) for automated rollbacks to avoid 'flapping'.")
