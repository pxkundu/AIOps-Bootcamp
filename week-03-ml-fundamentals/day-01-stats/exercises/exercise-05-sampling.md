# Exercise 05: The Central Limit Theorem in Monitoring

## 🎯 Objective
Understand why Prometheus and other monitoring tools use **Sampling** and why, thanks to the Central Limit Theorem (CLT), the "Average of Samples" eventually looks like a Normal Distribution, even if the raw data is chaotic.

---

## 🛠️ Step 1: The Chaotic Source
Create a population of 100,000 requests with a highly non-normal distribution (e.g., a **Uniform** distribution or a highly skewed **Pareto**).

---

## 📝 Step 2: Sampling
1.  Take 1,000 random samples of size $n=30$.
2.  Calculate the **Mean** of each sample.
3.  Plot a histogram of these **1,000 means**.

---

## 🔍 Step 3: Observation
Does the histogram of the *sample means* look like the original chaotic data? Or does it look like a Bell Curve?

---

## ✅ Deliverable
A Python script that:
1.  Plots the "Raw Data Histogram" vs the "Sample Means Histogram".
2.  Explains how many samples are needed ($n$) for the CLT to take effect in your metrics.
3.  Why is this property useful for setting "Global Alert Thresholds"?
