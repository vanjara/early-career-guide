> ℹ️ This guide is maintained by volunteers and reflects our best understanding of the job market. Company hiring practices, visa rules, and market conditions change. Cross-check anything critical — visa rules, hiring timelines, salary ranges — against primary sources before acting. Last updated: March 2026.

> 💡 Knowing the structure removes the anxiety of not knowing what's coming. Most companies run the same 4–5 step process.

---

## What interviewers are actually evaluating

Interviewers aren’t just checking whether you got the right answer. They’re reading signals.

| **Round** | **What they’re actually evaluating** |
|---|---|
| Recruiter screen | Whether the process should continue |
| Technical interview | How you think — problem decomposition, communication, edge cases |
| Behavioral interview | How you work — ownership, self-awareness, collaboration |
| Hiring manager screen | Whether you’d be good to work with |

Understanding this changes how you prepare. A technical question where you arrive at the wrong answer but communicate clearly, catch your own mistakes, and ask good clarifying questions will often score better than a silent correct solution.

---

## How hiring interviews actually work

| Round | What it is | What they're checking |
|---|---|---|
| Recruiter screen | 15–20 min phone call | Fit, basics, salary expectations |
| Hiring manager screen | 30 min | Your background and genuine interest |
| Technical / case round | 45–60 min | Role-specific skills (see tracks below) |
| Final round / onsite | 3–5 back-to-back interviews | Deep fit + technical |
| Offer | — | — |

---

## The recruiter screen

They're checking three things:

- Can you talk about yourself clearly?
- Do your background and expectations match the role?
- Are you a reasonable human being?
### 'Tell me about yourself' — 90-second answer

> "I'm a recent Data Analytics grad from [University] where I focused on SQL and Python for business problems. During my internship at [Company] I built dashboards the sales team used daily. I'm now looking for an analyst role where I can work on real business problems with data — which is why this role caught my attention."

### 'What are your salary expectations?'

Never give a number first if you can avoid it.

> "I'm still learning about the full scope of the role. What's the budgeted range for this position?"

If they push: give a range based on Levels.fyi (tech) or Glassdoor/WSO (finance). Anchor slightly high.

---

## Behavioral interviews — every role, every company

### The STAR method

| Letter | What it means | Tips |
|---|---|---|
| S — Situation | Set the context briefly | 1–2 sentences max |
| T — Task | What were you responsible for | Be specific about your role |
| A — Action | What YOU specifically did | Not 'we' — what did you do |
| R — Result | What happened | Quantify if possible |

### Common questions

| Question | What they want to see |
|---|---|
| Tell me about a time you faced a challenge | Resilience, problem-solving |
| Tell me about a time you worked with a difficult person | Maturity, communication |
| Tell me about a project you're proud of | Ownership, impact |
| Tell me about a time you failed | Self-awareness, learning |
| Tell me about a time you led something | Initiative, leadership |

> 💡 Prepare 5–6 strong stories from your experience. Internships, class projects, part-time jobs, student orgs all count. One strong story beats ten weak ones.

---

---

## Beyond STAR — other frameworks worth knowing

> 💡 STAR works for 90% of behavioral questions. These frameworks are worth knowing for specific situations.

| Framework | Stands for | When to use it |
|---|---|---|
| STAR | Situation, Task, Action, Result | Default — most behavioral questions |
| STARR | Situation, Task, Action, Result, Reflection | When growth mindset matters — add what you learned and would do differently |
| SOAR | Situation, Obstacle, Action, Result | When the difficulty is the point — turnarounds, hard deadlines, conflict |
| CAR | Context, Action, Result | Concise answers where the context is simple — keeps you from over-explaining setup |
| PARADE | Problem, Anticipated outcome, Role, Action, Decision, End result | Consulting interviews — McKinsey, BCG. Forces you to show judgment vs. what you expected |
| DIGS | Dilemma, Insight, Growth, Success | Failure and weakness questions — STAR produces flat answers here, DIGS forces reflection |

### How to pick the right one

- Default to **STAR** — it's what interviewers are trained to evaluate against
- Use **SOAR** when the obstacle or conflict is central to the story
- Use **PARADE** if interviewing at a consulting firm — it signals you understand their evaluation style
- Use **DIGS** for 'tell me about a failure' or 'what's your biggest weakness' — STAR makes these feel like you're avoiding the question
- Use **STARR** when you want to show self-awareness and growth — good for culture-fit focused companies

> 💡 The framework matters less than the story. Pick the one that makes your answer clearest — don't force a story into a framework that doesn't fit.

## Technical prep — by track

### 💻 Tech (SWE, Data Engineering, Data Science)

LeetCode-style coding problems, 1–2 per round, 45 minutes, talking through your thinking.

| Priority | Topics |
|---|---|
| Must know | Arrays, strings, hashmaps, two pointers, sliding window |
| Should know | Trees, graphs, BFS/DFS, recursion |
| Good to have | Dynamic programming, heaps, tries |

Resources:

| Resource | What it's for |
|---|---|
| [Neetcode.io](https://neetcode.io/) | Structured roadmap, video explanations — best starting point |
| [LeetCode](https://leetcode.com/) | Do Neetcode 150, not random problems |
| [interviewing.io](https://interviewing.io/) | Mock interviews with real engineers |

### 📊 Data Science

SQL + Python + stats + ML concepts + product/metric design. Format varies: Big Tech tests product sense, startups lean on take-homes, research roles go deep on ML.

| Area | What to know |
|---|---|
| SQL | JOINs, window functions, CTEs, aggregations — same depth as analytics |
| Python | pandas, numpy, scikit-learn — fitting models, train/test split, evaluation |
| Statistics | Distributions, Bayes, CLT, A/B testing design, hypothesis testing, power/sample size |
| ML concepts | Bias-variance, regularization (L1/L2), class imbalance, cross-validation, model evaluation |
| Product/metrics | Metric design and drop diagnosis — unique to DS roles at tech companies |

Resources:

| Resource | What it's for |
|---|---|
| [Ace the Data Science Interview](https://acethedatascienceinterview.com/) | Best single prep resource — SQL, stats, ML, product all in one |
| [StatQuest (YouTube)](https://www.youtube.com/@statquest) | Visual explanations of ML and stats — builds intuition |
| [DataLemur](https://datalemur.com/) | SQL and DS interview questions from real companies |
| [Kaggle](https://www.kaggle.com/) | Hands-on ML practice |

### 🔧 DevOps / SRE / Infra

Less LeetCode. More Linux, networking, systems design for reliability, and how you think through incidents.

Linux fundamentals:

| Command / concept | What to know |
|---|---|
| File permissions | chmod, chown, what 755 means |
| Process management | ps, top, kill, systemctl |
| Networking commands | netstat, ss, curl, dig, traceroute |
| Disk and memory | df, du, free, lsof |
| Log files | journalctl, /var/log, grep through logs |
| URL in browser | DNS → TCP → TLS → HTTP → response — know this cold |

Networking fundamentals:

| Topic | What to know |
|---|---|
| DNS | How resolution works, TTL, difference between A/CNAME/MX records |
| TCP vs UDP | When you'd use each |
| Load balancing | L4 vs L7, round robin vs least connections |
| Common ports | 22 SSH, 80 HTTP, 443 HTTPS, 5432 Postgres, 6379 Redis |
| Subnets | NAT, CIDR notation basics |

Systems design for reliability — common prompts: design a CI/CD pipeline, make this service highly available, design a monitoring system.

Incident response — as a new grad, you won't have real on-call experience and interviewers know that. They're testing whether you think systematically under pressure, not whether you've been paged at 3am.

Portfolio — a well-documented project showing the full DevOps stack is worth more than any certification for getting your first interview:

- Deploy an app on AWS/GCP using Terraform — infrastructure as code, not clicked in the console
- Set up a CI/CD pipeline with GitHub Actions — test, build, deploy on every push
- Add monitoring and alerting — Prometheus + Grafana, or a cloud-native equivalent
- Document the architecture — a README explaining design decisions, not just commands
Cloud certifications worth pursuing:

- AWS Solutions Architect Associate — broad cloud fundamentals, widely recognized
- CKA (Certified Kubernetes Administrator) — hands-on, practical, respected by hiring managers
- HashiCorp Terraform Associate — signals IaC proficiency
Realistic entry points for new grads: SWE first then pivot after 1-2 years (most common), cloud consulting at firms like Accenture/Deloitte/Slalom, SRE new grad programs (Google has a well-known track), or smaller companies where DevOps means one person doing everything.

### 📊 Data Analytics

Expect SQL + take-home case + behavioral.

SQL — know cold: JOINs, GROUP BY, HAVING, window functions, CTEs, CASE WHEN, date functions

Practice: DataLemur, StrataScratch (real questions from Meta, Amazon, Google)

Statistics to know: A/B testing, p-value in plain English, statistical vs practical significance, correlation vs causation

Take-home case structure:

1. What question are you answering?
1. What did you find? (key insight first, not methodology first)
1. What does it mean for the business?
1. What would you recommend?
1. What are the limitations?
### 💰 Finance & Consulting

Finance — technical questions to know cold:

| Question | Key points |
|---|---|
| Walk me through a DCF | Future free cash flows → discount at WACC → terminal value |
| Three financial statements | Net income flows to retained earnings + starts cash flow statement |
| Depreciation increases $10 | Net income -$7, cash from ops +$3, PP&E -$10, balanced |
| What is EBITDA? | Earnings before interest, taxes, depreciation, amortization |
| Enterprise vs equity value | EV = equity + debt - cash |

Resources: Mergers & Inquisitions (free), Wall Street Prep, Breaking Into Wall Street

Consulting — case interviews:

1. Clarify — ask 1–2 questions before structuring
1. Structure — lay out your framework out loud
1. Analyze — work through each area, prioritize what matters most
1. Synthesize — 'My recommendation is...'
Practice: Case in Point (book), IGotAnOffer, firm-published cases (McKinsey, BCG, Bain)

> ⚠️ Non-negotiable: practice cases out loud with a partner. Solo reading is not enough.

---

## Questions to ask the interviewer

### Good questions to ask

- 'What does success look like in this role in the first 90 days?'
- 'What's the biggest challenge the team is working through right now?'
- 'What do you like most about working here?'
- 'What are the growth paths from this role?'
> ⚠️ Always prepare 2–3 questions. 'I don't have any questions' is a red flag.

---

## After the interview

> 💡 Same day: Send a thank you email. Two sentences.

"Thanks for taking the time today — I really enjoyed learning about [specific thing]. It's made me even more excited about the role."

One follow-up if you don't hear back. Not three.

---

---
