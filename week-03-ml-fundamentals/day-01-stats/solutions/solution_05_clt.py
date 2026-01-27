import numpy as np
import matplotlib.pyplot as plt

# 1. Create a highly non-normal population (Pareto / Power Law)
# This represents a system where 99% are small and a few are HUGE
population = np.random.pareto(a=2, size=100000)

# 2. Simulation: Central Limit Theorem
sample_size = 50
num_samples = 2000

sample_means = []
for _ in range(num_samples):
    sample = np.random.choice(population, size=sample_size)
    sample_means.append(np.mean(sample))

# 3. Visualization
plt.figure(figsize=(12, 5))

# Subplot 1: Raw Data
plt.subplot(1, 2, 1)
plt.hist(population, bins=100, range=(0, 10), color='salmon', alpha=0.7)
plt.title("Raw Metric Population (Chaotic)")
plt.xlabel("Value")
plt.ylabel("Frequency")

# Subplot 2: Sample Means
plt.subplot(1, 2, 2)
plt.hist(sample_means, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.title(f"Histogram of {num_samples} Sample Means (n={sample_size})")
plt.xlabel("Mean Value")
plt.ylabel("Frequency")

plt.tight_layout()
print("Simulation complete. Showing plots...")
plt.show()

print("\n--- AIOps Insight: Central Limit Theorem ---")
print("1. Observation: Despite the raw data being highly skewed, the histogram of MEANS looks like a normal curve.")
print("2. Monitoring Application: This is why metrics platforms can aggregate 1-sec samples into 1-min averages.")
print("   The average of a sample is more mathematically predictable than the raw event.")
print("3. Alerting: We set alert thresholds on These Aggregated Averages because they are stable.")
