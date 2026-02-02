# Week 3 Day 3 Resources: Supervised Learning

> Curated resources for mastering classification, handling imbalanced data, and deploying ML models.

---

## 📚 Essential Reading

### Foundational Concepts
- **[Google's Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)** - 43 best practices from Google's ML teams
- **[Scikit-learn User Guide: Supervised Learning](https://scikit-learn.org/stable/supervised_learning.html)** - Comprehensive guide to all algorithms
- **[The Unreasonable Effectiveness of Data](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35179.pdf)** - Classic paper on why more data beats better algorithms

### Handling Imbalanced Data
- **[Learning from Imbalanced Data](https://www.jair.org/index.php/jair/article/view/10302)** - Academic survey of techniques
- **[Imbalanced-learn Documentation](https://imbalanced-learn.org/stable/)** - SMOTE, undersampling, and more
- **[Precision-Recall vs ROC Curves](https://machinelearningmastery.com/roc-curves-and-precision-recall-curves-for-classification-in-python/)** - When to use which

### Evaluation Metrics
- **[Beyond Accuracy: Precision and Recall](https://towardsdatascience.com/beyond-accuracy-precision-and-recall-3da06bea9f6c)** - Visual explanations
- **[Classification Metrics Cheat Sheet](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)** - Official scikit-learn guide

---

## 🛠️ Tools & Libraries

### Core ML Libraries
- **[Scikit-learn](https://scikit-learn.org/)** - The foundation for classical ML
- **[XGBoost](https://xgboost.readthedocs.io/)** - Gradient boosting champion
- **[LightGBM](https://lightgbm.readthedocs.io/)** - Microsoft's fast gradient boosting
- **[CatBoost](https://catboost.ai/)** - Yandex's library, great for categorical features

### Imbalanced Data
- **[Imbalanced-learn](https://imbalanced-learn.org/)** - SMOTE, ADASYN, and sampling techniques
- **[SMOTE Variants](https://github.com/analyticalmindsltd/smote_variants)** - 85+ oversampling techniques

### Model Explainability
- **[SHAP](https://shap.readthedocs.io/)** - Explain any model's predictions
- **[LIME](https://github.com/marcotcr/lime)** - Local interpretable model-agnostic explanations
- **[ELI5](https://eli5.readthedocs.io/)** - Debug ML classifiers and explain predictions

### Deployment
- **[Flask](https://flask.palletsprojects.com/)** - Lightweight API framework
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast API with automatic docs
- **[BentoML](https://www.bentoml.com/)** - ML model serving framework
- **[ONNX](https://onnx.ai/)** - Open format for ML models (cross-platform)

---

## 📊 Datasets for Practice

### AIOps-Specific
- **[Backblaze Hard Drive Dataset](https://www.backblaze.com/b2/hard-drive-test-data.html)** - Predict disk failures
- **[Google Cluster Traces](https://github.com/google/cluster-data)** - Real cluster workload data
- **[Alibaba Cluster Trace](https://github.com/alibaba/clusterdata)** - Large-scale production traces

### General Imbalanced Classification
- **[Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)** - 0.17% fraud rate
- **[Network Intrusion Detection](https://www.kaggle.com/datasets/sampadab17/network-intrusion-detection)** - Detect attacks
- **[Anomaly Detection](https://odds.cs.stonybrook.edu/)** - Collection of outlier detection datasets

---

## 🎓 Courses & Tutorials

### Free Courses
- **[Andrew Ng's Machine Learning (Coursera)](https://www.coursera.org/learn/machine-learning)** - The classic introduction
- **[Fast.ai Practical Deep Learning](https://course.fast.ai/)** - Top-down learning approach
- **[Google's Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)** - 15 hours, TensorFlow-based

### Hands-On Tutorials
- **[Scikit-learn Tutorials](https://scikit-learn.org/stable/tutorial/index.html)** - Official step-by-step guides
- **[Kaggle Learn: Intro to ML](https://www.kaggle.com/learn/intro-to-machine-learning)** - Interactive notebooks
- **[Machine Learning Mastery](https://machinelearningmastery.com/start-here/)** - Practical tutorials

---

## 📖 Books

### Beginner-Friendly
- **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"** by Aurélien Géron
- **"Introduction to Machine Learning with Python"** by Andreas Müller & Sarah Guido

### Advanced
- **"The Elements of Statistical Learning"** by Hastie, Tibshirani, Friedman (free PDF available)
- **"Pattern Recognition and Machine Learning"** by Christopher Bishop

### AIOps-Specific
- **"Practical Machine Learning for Data Analysis Using Python"** by Abdulhamit Subasi
- **"Machine Learning for Cybersecurity Cookbook"** by Emmanuel Tsukerman

---

## 🔬 Research Papers

### Must-Read Classics
- **[Random Forests (2001)](https://link.springer.com/article/10.1023/A:1010933404324)** - Leo Breiman's original paper
- **[XGBoost: A Scalable Tree Boosting System (2016)](https://arxiv.org/abs/1603.02754)** - The paper behind XGBoost
- **[SMOTE: Synthetic Minority Over-sampling Technique (2002)](https://arxiv.org/abs/1106.1813)** - Original SMOTE paper

### AIOps Applications
- **[Failure Prediction in IBM BlueGene/L](https://ieeexplore.ieee.org/document/4408699)** - Early AIOps work
- **[Predicting Node Failures in an Ultra-Scale Cloud](https://www.microsoft.com/en-us/research/publication/predicting-node-failure-in-cloud-service-systems/)** - Microsoft Azure
- **[AIOps: Real-World Challenges and Research Innovations](https://arxiv.org/abs/2012.03291)** - Survey paper

---

## 🎯 Best Practices

### Feature Engineering
- **[Feature Engineering for Machine Learning](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/)** - O'Reilly book
- **[Automated Feature Engineering](https://github.com/alteryx/featuretools)** - Featuretools library
- **[Time Series Feature Extraction](https://tsfresh.readthedocs.io/)** - tsfresh library

### Model Selection
- **[Choosing the Right Estimator](https://scikit-learn.org/stable/tutorial/machine_learning_map/)** - Scikit-learn flowchart
- **[No Free Lunch Theorem](https://en.wikipedia.org/wiki/No_free_lunch_theorem)** - Why you must experiment

### Hyperparameter Tuning
- **[Optuna](https://optuna.org/)** - Automatic hyperparameter optimization
- **[Hyperopt](http://hyperopt.github.io/hyperopt/)** - Bayesian optimization
- **[Ray Tune](https://docs.ray.io/en/latest/tune/index.html)** - Scalable hyperparameter tuning

---

## 🐛 Common Pitfalls & Solutions

### Data Leakage
**Problem:** Test accuracy is 99%, production accuracy is 60%.

**Cause:** Information from the test set leaked into training (e.g., scaling before split).

**Solution:**
```python
# WRONG
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled, y)

# RIGHT
X_train, X_test, y_train, y_test = train_test_split(X, y)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same scaler!
```

**Read:** [Data Leakage in Machine Learning](https://machinelearningmastery.com/data-leakage-machine-learning/)

---

### Overfitting
**Problem:** Training accuracy 98%, test accuracy 65%.

**Cause:** Model memorized training data instead of learning patterns.

**Solutions:**
- Use cross-validation
- Reduce model complexity (`max_depth`, `n_estimators`)
- Add regularization
- Get more training data

**Read:** [Overfitting and Underfitting](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html)

---

### Class Imbalance
**Problem:** 99% accuracy but model never predicts the minority class.

**Cause:** Model learned to always predict the majority class.

**Solutions:**
- Use `class_weight='balanced'`
- Apply SMOTE or undersampling
- Use F1-score instead of accuracy
- Adjust decision threshold

**Read:** [8 Tactics to Combat Imbalanced Classes](https://machinelearningmastery.com/tactics-to-combat-imbalanced-classes-in-your-machine-learning-dataset/)

---

## 🚀 Production ML

### Model Serving
- **[TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)** - Production ML serving
- **[Seldon Core](https://www.seldon.io/tech/products/core/)** - Kubernetes-native ML deployment
- **[KServe](https://kserve.github.io/website/)** - Serverless ML inference

### Monitoring
- **[Evidently AI](https://www.evidentlyai.com/)** - ML model monitoring
- **[Whylabs](https://whylabs.ai/)** - Data and ML monitoring
- **[Arize AI](https://arize.com/)** - ML observability platform

### MLOps
- **[MLflow](https://mlflow.org/)** - Track experiments, package models
- **[Kubeflow](https://www.kubeflow.org/)** - ML workflows on Kubernetes
- **[DVC](https://dvc.org/)** - Data version control

---

## 🎬 Videos & Talks

### Conceptual
- **[StatQuest: Machine Learning](https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF)** - Clear visual explanations
- **[3Blue1Brown: Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)** - Beautiful visualizations

### Practical
- **[Kaggle Grandmaster Tips](https://www.youtube.com/watch?v=GJBOMWpLpTQ)** - Competition-winning strategies
- **[Google Cloud ML Summit](https://www.youtube.com/playlist?list=PLIivdWyY5sqJdmVMjLI8iCul14XkTRosn)** - Production ML talks

---

## 🧪 Interactive Tools

### Visualization
- **[TensorFlow Playground](https://playground.tensorflow.org/)** - Visualize neural networks
- **[Seeing Theory](https://seeing-theory.brown.edu/)** - Visual statistics
- **[Decision Tree Visualizer](https://explained.ai/decision-tree-viz/)** - Understand tree models

### Experimentation
- **[Google Colab](https://colab.research.google.com/)** - Free GPU notebooks
- **[Kaggle Notebooks](https://www.kaggle.com/code)** - Public datasets + notebooks
- **[Deepnote](https://deepnote.com/)** - Collaborative data science

---

## 📱 Communities

### Forums
- **[r/MachineLearning](https://www.reddit.com/r/MachineLearning/)** - Research discussions
- **[r/learnmachinelearning](https://www.reddit.com/r/learnmachinelearning/)** - Beginner-friendly
- **[Cross Validated (StackExchange)](https://stats.stackexchange.com/)** - Statistics Q&A

### Competitions
- **[Kaggle](https://www.kaggle.com/)** - Data science competitions
- **[DrivenData](https://www.drivendata.org/)** - Social good competitions
- **[AIcrowd](https://www.aicrowd.com/)** - Research challenges

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Scikit-learn Cheat Sheet | https://scikit-learn.org/stable/tutorial/machine_learning_map/ |
| XGBoost Parameters | https://xgboost.readthedocs.io/en/stable/parameter.html |
| SHAP Examples | https://shap.readthedocs.io/en/latest/example_notebooks.html |
| Imbalanced-learn API | https://imbalanced-learn.org/stable/references/index.html |
| Flask Quickstart | https://flask.palletsprojects.com/en/2.3.x/quickstart/ |

---

## 💡 Pro Tips

1. **Start Simple:** Always baseline with Logistic Regression before trying complex models.
2. **Cross-Validate:** Never trust a single train/test split.
3. **Feature Engineering > Algorithms:** 10 good features beat 100 mediocre ones.
4. **Monitor in Production:** Models decay over time (concept drift).
5. **Explain Your Models:** If you can't explain it, don't deploy it.

---

## 🎯 Next Steps

After mastering supervised learning:
1. Complete [Day 4: Unsupervised Learning](../day-04-unsupervised/lecture-notes.md)
2. Read [Google's Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml)
3. Enter a [Kaggle competition](https://www.kaggle.com/competitions)
4. Build your own project and deploy it!
