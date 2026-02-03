# Week 3 Day 5 Resources: Evaluation & AutoML

> References for robust evaluation, hyperparameter optimization, and automated machine learning.

---

## 📚 Essential Reading

### Evaluation
- **[Cross-Validation: Evaluation Models](https://scikit-learn.org/stable/modules/cross_validation.html)** - Scikit-learn guide.
- **[Time Series Nested Cross-Validation](https://towardsdatascience.com/time-series-nested-cross-validation-76adba623eb9)** - Why standard CV fails for logs.

### Tuning
- **[A Hyperparameter Optimization Framework (Optuna)](https://optuna.org/)** - Documentation for the modern standard.
- **[Random Search for Hyper-Parameter Optimization](https://www.jmlr.org/papers/volume13/bergstra12a/bergstra12a.pdf)** - The paper proving Random > Grid.

### Interpretability
- **[SHAP Documentation](https://shap.readthedocs.io/en/latest/)** - The bible of model explanation.
- **[Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/)** - Free online book analyzing all methods (LIME, SHAP, etc.).

---

## 🛠️ Tools & Libraries

### Optimization
- **[Optuna](https://github.com/optuna/optuna)** - Automatic hyperparameter optimization software framework.
- **[Hyperopt](http://hyperopt.github.io/hyperopt/)** - Older but still popular Bayesian optimizer.

### AutoML
- **[TPOT](http://epistasislab.github.io/tpot/)** - Genetic programming for pipelines.
- **[Auto-Sklearn](https://automl.github.io/auto-sklearn/master/)** - Automated scikit-learn.
- **[H2O AutoML](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html)** - Enterprise-grade AutoML.
- **[PyCaret](https://pycaret.org/)** - Low-code ML library (highly recommended for rapid prototyping).

```bash
pip install optuna shap tpot pycaret
```

---

## 💡 Best Practices

1. **Stratify, Stratify, Stratify**: In AIOps, your positive class is tiny. If you don't use Stratified CV, your results are random noise.
2. **Don't Over-tune**: Improving AUC from 0.95 to 0.951 via 100 hours of tuning is rarely worth it. Focus on better features (data quality) instead.
3. **Black Boxes are Dangerous**: If AutoML gives you a model with 99% accuracy but uses "Index" as a feature, you're doomed. Always inspect the feature importance.
4. **Leakage is Everywhere**: If you perform imputation or scaling on the *whole* dataset before CV splitting, you are cheating. Use Pipelines!

```python
# The Correct Way
pipeline = Pipeline([
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier())
])
cross_val_score(pipeline, X, y, cv=5)
```
