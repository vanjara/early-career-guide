# Interview Prep — Data Science Track

## What to expect

Data science interviews vary more than any other track. The format depends heavily on the type of company.

```
Startup / growth company    SQL + Python + take-home project + product sense
Big Tech (DS)               Product/metric questions + ML concepts + SQL + stats
Research-heavy (DS/ML)      ML depth + coding + research discussion
Analytics-adjacent DS       Mostly DA format — SQL, A/B testing, case study
```

Know which type you're interviewing for before you prep. Job description usually tells you — look for whether they mention "experimentation," "machine learning models," or "research."

---

## SQL — required even for DS roles

DS roles at most companies still require SQL. You won't get away with "I do Python for everything."

**Must know:**
- JOINs, GROUP BY, HAVING, WHERE
- Window functions — ROW_NUMBER, RANK, LAG, LEAD, SUM OVER
- CTEs and subqueries
- Aggregations, CASE WHEN, date functions

**Practice:** DataLemur, StrataScratch — same resources as analytics.

---

## Python

DS roles expect more than pandas. You need to be able to write clean code and work with modeling libraries.

**Know these:**
- pandas and numpy — data manipulation, array operations
- scikit-learn — fitting models, train/test split, pipelines, cross-validation
- matplotlib / seaborn — visualizing results and model diagnostics
- Writing functions and readable code (not just notebooks)

**You don't need to implement algorithms from scratch** in most interviews. But you should understand what's happening inside them.

---

## Statistics and probability — know this well

This is where DS interviews go deeper than analytics.

**Core stats:**
- Distributions — normal, binomial, Poisson, when to use each
- Central Limit Theorem — what it says and why it matters for inference
- Bayes' theorem — especially conditional probability problems (common in interviews)
- Hypothesis testing — null vs. alternative hypothesis, Type I and Type II errors
- p-value — what it means, what it doesn't mean
- Confidence intervals — construction and interpretation
- Statistical power and sample size

**A/B testing depth:**
- How to design an experiment — randomization unit, metric selection, guardrail metrics
- When to stop a test early (and why you usually shouldn't)
- Multiple testing problem (running too many variants)
- Network effects and how they violate standard A/B test assumptions

**Common probability questions:**
> *"A coin is flipped 10 times and comes up heads 8 times. What's the probability the coin is fair?"*
> *"You have two tests for a disease. One is more sensitive, one more specific. Which do you use for screening vs. confirmation?"*

Practice Bayes' theorem problems until they feel mechanical.

---

## Machine learning concepts

You need to be able to explain models and reason about when to use them — not just run sklearn.

**Concepts to know:**
- Bias-variance tradeoff — what it is, how regularization addresses variance
- Overfitting vs. underfitting — how to detect, how to fix
- Regularization — L1 (Lasso) vs. L2 (Ridge) and the intuition behind each
- Class imbalance — what it causes, how to handle it (resampling, class weights, threshold adjustment)
- Feature importance — how tree models and linear models handle it differently

**Model evaluation:**
- Classification: accuracy, precision, recall, F1, AUC-ROC — when each matters
- Regression: RMSE, MAE, R² — what each penalizes
- Cross-validation — why you do it and how k-fold works

**Algorithm intuition (know the tradeoffs, not just the name):**

| Model | Strengths | Watch out for |
|---|---|---|
| Linear/Logistic Regression | Interpretable, fast | Assumes linearity, sensitive to outliers |
| Decision Trees | Intuitive, handles non-linearity | Prone to overfitting |
| Random Forest | Robust, handles high dimensions | Slower, less interpretable |
| Gradient Boosting (XGBoost) | High accuracy on tabular data | Many hyperparameters, can overfit |
| K-Means | Simple clustering | Requires setting k, sensitive to scale |

You don't need to know everything — know 3-4 models deeply enough to discuss tradeoffs.

---

## Product and metric questions (tech company DS)

This is what separates DS interviews at product companies from everything else. You'll be asked to design metrics, define success, or diagnose a drop.

**Metric design:**
> *"How would you measure the success of a new feature in Instagram's feed?"*

Framework:
1. Clarify the goal — what is the feature trying to do?
2. Propose primary metric — tied directly to the goal
3. Add guardrail metrics — things that shouldn't get worse (session length, churn, revenue)
4. Discuss tradeoffs — what does this metric miss? What could game it?

**Metric drop diagnosis:**
> *"Daily active users dropped 10% last week. Walk me through how you'd investigate."*

Framework:
1. Scope it — is this all users or a segment? All platforms? All geographies?
2. Check the data — is this a tracking bug or a real drop?
3. Look for external causes — product change, holiday, outage
4. Segment — by acquisition channel, cohort, device, region
5. Form a hypothesis, then say what data you'd need to confirm

Practice narrating your thinking out loud. They're evaluating your debugging process, not whether you find the root cause.

---

## Resources

| Resource | What it's for |
|---|---|
| **Ace the Data Science Interview** (book) | Best single prep resource — SQL, stats, ML, product all in one |
| **StatQuest (YouTube)** | Visual explanations of ML and stats — excellent for building intuition |
| **DataLemur** | SQL and DS interview questions from real companies |
| **Kaggle** | Hands-on ML practice — competitions and notebooks |
| **3Blue1Brown (YouTube)** | Deep intuition for linear algebra and probability |

If you only have time for two: Ace the Data Science Interview + DataLemur.

---

## Behavioral questions specific to data science

> *"Tell me about a project where your model didn't perform as expected. What did you do?"*
> *"How do you communicate a complex model to a non-technical stakeholder?"*
> *"Tell me about a time you had to make a decision with incomplete or messy data."*
> *"How do you decide whether a problem needs ML or a simpler approach?"*

The last one matters. Interviewers want to see that you don't reach for ML by default. "I'd start with a simple rule-based approach to set a baseline" is a strong answer.
