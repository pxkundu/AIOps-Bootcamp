# Week 3 Day 1 Resources: Statistics for Operations

> Curated materials to master the bridge between math and machine performance.

---

## 📚 Essential Reading

### Statistics & SRE
- **[How to (Not) Trust Averages](https://queue.acm.org/detail.cfm?id=3068754)** - A classic ACM Queue article on latency distributions.
- **[Statistics for Software Engineers](https://github.com/v8sl/statistics-for-software-engineers)** - An excellent GitHub curriculum for picking up the math you missed in CS.
- **[AIOps and Information Theory](https://www.scalyr.com/blog/information-theory-for-logging/)** - How Shannon's work applies to modern log aggregation.
- **[The Tyranny of the Mean](https://medium.com/@Hiren_J/the-tyranny-of-the-mean-in-sre-observability-3f7d8858d4a9)** - Why averages are dangerous for SLOs.
- **[Probability Distributions for SREs (Google)](https://sre.google/sre-book/monitoring-distributed-systems/)** - Chapter 10 of the SRE book.

---

## 🛠️ Tools & Libraries

- **[Scipy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)** - The industry standard Python library for statistical tests.
- **[Numpy Statistics Functions](https://numpy.org/doc/stable/reference/routines.statistics.html)** - Fast calculations of means, quantiles, and variances.
- **[Statsmodels](https://www.statsmodels.org/stable/index.html)** - Advanced statistical modeling (needed for Day 6 Time-Series).
- **[Pandas Profiling / YData Profiling](https://github.com/ydataai/ydata-profiling)** - One-line statistical reports for your datasets.
- **[Pingouin](https://pingouin-stats.org/)** - A simpler, more modern alternative to Scipy for statistical testing in Python.

---

## 💻 Video Tutorials

- **[Probability Distributions in Ops (Talk)](https://www.youtube.com/watch?v=R96-9t3DsbE)** - Why the Bell Curve is often your enemy in distributed systems.
- **[Entropy: The measure of uncertainty](https://www.youtube.com/watch?v=2s3aEfGUMoU)** - A visual guide to understanding Shannon Entropy.

---

## 💡 Pro-Tips for "The Alchemist"

1. **Be Afraid of Bimodality:** If your histogram has two peaks, you don't have one system; you have *two* distinct behaviors fighting for control (e.g., Cache Hits vs. Cache Misses).
2. **Standardize your Units:** Before comparing two distributions (e.g., CPU vs. Latency), use **Z-Score Normalization** so you can compare "Apples to Oranges".
3. **The Power of Logarithms:** Statistical rarity is exponential. log-transforming counts helps you see "Order of Magnitude" differences in log frequency.
