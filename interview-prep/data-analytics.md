# Interview Prep — Data Analytics Track

## What to expect

A mix of SQL, a take-home or case, and behavioral. Some companies add a presentation round.

```
Round 1    Recruiter screen
Round 2    SQL / technical screen (30-45 min)
Round 3    Take-home case or live case (1-3 days for take-home)
Round 4    Final round — stakeholder interviews + present your case
```

---

## SQL — know this cold

SQL is non-negotiable for data analyst roles. Every company tests it.

**Must know:**
- JOINs (INNER, LEFT, RIGHT, FULL OUTER) — and when to use each
- GROUP BY, HAVING, WHERE — and the difference
- Window functions — ROW_NUMBER, RANK, LAG, LEAD, SUM OVER, AVG OVER
- Subqueries and CTEs
- Aggregations — COUNT, SUM, AVG, MIN, MAX
- CASE WHEN statements
- Date functions

**Practice resources:**
- **DataLemur** — real interview questions from Meta, Amazon, Google, etc.
- **StrataScratch** — company-specific SQL problems
- **Mode Analytics SQL Tutorial** — free, covers everything from basics to window functions

---

## Python / pandas (for more technical DA roles)

Not every analyst role requires Python — but knowing it separates you.

What to know:
- Reading and manipulating DataFrames (filtering, grouping, merging)
- Basic data cleaning (handling nulls, type conversion, deduplication)
- Simple visualizations (matplotlib, seaborn)

You don't need to know ML. Know pandas well.

---

## Statistics concepts you'll be asked about

Companies test whether you can think statistically, not just query data.

**Know these:**
- A/B testing — what it is, when to use it, how to interpret results
- p-value — what it means in plain English (not the textbook definition)
- Statistical significance vs. practical significance
- Correlation vs. causation
- Normal distribution, mean, median, mode, standard deviation
- Confidence intervals

**Common question format:**
> *"We ran an A/B test. Treatment group had a 5% higher conversion rate with p=0.03. What do you conclude?"*

Be ready to discuss: sample size, test duration, what else you'd want to know before acting on results.

---

## The take-home case

They give you a dataset. You analyze it and present findings. Usually 1-3 days.

**Structure your output as a business story, not a data dump:**

```
1. What question are you answering?
2. What did you find? (key insight first, not methodology first)
3. What does it mean for the business?
4. What would you recommend?
5. What are the limitations / what would you do with more time?
```

**Tips:**
- State your assumptions clearly upfront
- One clear recommendation at the end — don't hedge everything
- Visualizations should be simple and readable, not impressive
- The analysis is table stakes — your ability to tell a story with it is what gets you the offer

---

## Tools to know

| Tool | Priority |
|---|---|
| SQL | Must have |
| Excel / Google Sheets | Must have (pivot tables, VLOOKUP/INDEX MATCH) |
| Tableau or Power BI | Strong plus |
| Python (pandas) | Plus for technical roles |
| dbt | Plus for data-forward companies |

---

## Behavioral questions specific to analytics

> *"Tell me about a time you found an insight in data that changed a business decision."*
> *"Tell me about a time a stakeholder disagreed with your analysis."*
> *"How do you prioritize competing requests from different teams?"*
> *"Tell me about a time your analysis was wrong."*

The last one matters. Interviewers want to see that you catch your own mistakes, not that you're perfect.
