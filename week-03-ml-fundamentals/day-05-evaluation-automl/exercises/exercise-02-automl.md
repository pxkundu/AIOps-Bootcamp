# Exercise 02: AutoML with TPOT

## 🎯 Objective
Use **TPOT (Tree-based Pipeline Optimization Tool)** to automatically discover the best machine learning pipeline for a dataset. You will see how AutoML can try thousands of combinations (Feature Selection -> Preprocessing -> Model) that you might never think of.

---

## 📊 The Data
We will use the **Digits Dataset** (identifying hand-written numbers), but we'll add some noise to make it harder.

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import numpy as np

# Load data
digits = load_digits()
X, y = digits.data, digits.target

# Add noise to make it challenging
rng = np.random.RandomState(42)
X_noisy = X + rng.normal(0, 4, size=X.shape)

# Split
X_train, X_test, y_train, y_test = train_test_split(X_noisy, y, test_size=0.25, random_state=42)
```

---

## 🛠️ Step 1: Baseline Model
Train a standard `LogisticRegression` or `RandomForest` on `X_train` and report the accuracy on `X_test`.

```python
from sklearn.ensemble import RandomForestClassifier
# ... your code here ...
```

---

## 🛠️ Step 2: Run TPOT
Now, let the genetic algorithms take over.

```python
from tpot import TPOTClassifier

# Initialize TPOT
tpot = TPOTClassifier(
    generations=5,          # How many iterations of evolution
    population_size=20,     # How many pipelines to keep in each generation
    verbosity=2,            # Print progress
    random_state=42,
    n_jobs=-1               # Use all CPUs
)

# Fit (this mimics sklearn syntax)
tpot.fit(X_train, y_train)

# Evaluate
print(f"TPOT Score: {tpot.score(X_test, y_test)}")
```

**Note:** This might take 2-5 minutes to run. Watch the output—it will tell you which "individuals" (pipelines) are winning.

---

## 🛠️ Step 3: Export the Code
AutoML isn't a black box if it gives you the code!

```python
tpot.export('tpot_digits_pipeline.py')
```

**Task:** Open the generated `tpot_digits_pipeline.py` file.
1. What model did it choose? (SVM? KNN? XGBoost?)
2. Did it use any preprocessing? (PCA? StandardScaler?)
3. Compare this to your baseline.

---

## 📝 Submission
Submit the `tpot_digits_pipeline.py` file and a brief note on the score improvement.
