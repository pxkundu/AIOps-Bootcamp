# Week 3 Day 5 Quiz: Evaluation & AutoML

## 🧠 Test Your Knowledge

### Question 1: Cross-Validation
You are building an AIOps model to predict server crashes occurring on Fridays based on logs from Monday-Thursday. You use standard `KFold(shuffle=True)` cross-validation and get 99% accuracy.
Why is this likely a mistake?
- [ ] It's not a mistake; general AI works this way.
- [ ] You are leaking future information (training on next Friday to predict this Friday).
- [ ] You should have used `LeaveOneOut`.

<details>
<summary>Click for Answer</summary>
**Answer: You are leaking future information.**
Logs are time-series data. If you shuffle, you might train on a log from Dec 20 to predict a failure on Dec 10. This is impossible in production. Use <code>TimeSeriesSplit</code>.
</details>

---

### Question 2: Imbalanced Metrics
Your dataset has 99,000 normal events and 1,000 failures. Your model predicts "Normal" for everything.
What is the Accuracy? What is the Recall?
- [ ] Accuracy: 10%, Recall: 99%
- [ ] Accuracy: 99%, Recall: 0%
- [ ] Accuracy: 50%, Recall: 50%

<details>
<summary>Click for Answer</summary>
**Answer: Accuracy: 99%, Recall: 0%**
This is the "Accuracy Trap". The model is useless despite high accuracy because it missed every single failure.
</details>

---

### Question 3: Tuning
Which tuning method guarantees finding the *absolute best* hyperparameters if given infinite time?
- [ ] Random Search
- [ ] Grid Search
- [ ] Optuna

<details>
<summary>Click for Answer</summary>
**Answer: Grid Search**
Grid Search tries *every* combination defined. Random Search and Optuna are approximations (though Optuna is usually much more efficient for practical time limits).
</details>

---

### Question 4: SHAP
In a SHAP summary plot, a feature has a long tail of red dots extending to the right. What does this mean?
- [ ] High values of this feature push the model prediction lower.
- [ ] High values of this feature push the model prediction higher (more likely to be Class 1).
- [ ] The feature is irrelevant.

<details>
<summary>Click for Answer</summary>
**Answer: High values push prediction higher.**
Red typically denotes "High Feature Value". Moving to the right on the x-axis means "Positive impact on model output".
</details>
