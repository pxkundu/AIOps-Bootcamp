# Exercise 04: Modeling the "Tail" (Skewness & Kurtosis)

## 🎯 Objective
Understand the "Shape" of your data. Most AIOps failures occur in the "Tails" of a distribution. You will learn to measure exactly how "fat" or "heavy" those tails are.

---

## 🛠️ Step 1: The Heavy Tail
Create two datasets in Python:
1.  `normal_data`: 1000 samples from a Normal distribution.
2.  `outlier_heavy_data`: 1000 samples from a Normal distribution + 50 extreme outliers (e.g., values 10x the mean).

---

## 📝 Step 2: Measuring Skewness
Skewness measures symmetry.
- If Skewness > 0: Right-tailed (typical for latency).
- If Skewness < 0: Left-tailed.

---

## 📝 Step 3: Measuring Kurtosis
Kurtosis measures the "Tailedness". 
- **High Kurtosis:** Very high peaks and fat tails (lots of outliers).
- **Low Kurtosis:** Flat peaks and thin tails.

### Task:
Use `scipy.stats.skew` and `scipy.stats.kurtosis` on both datasets.

---

## ✅ Deliverable
A comparison table showing:
| Metric | Normal Dataset | Outlier Dataset |
|--------|----------------|-----------------|
| Mean | | |
| Std Dev | | |
| Skewness | | |
| Kurtosis | | |

**Discussion:** Why does the **Standard Deviation** change so much more than the **Median** when you add outliers? How does this influence your choice of "Normal" behavior in an AIOps model?
