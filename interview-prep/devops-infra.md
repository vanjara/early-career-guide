# Interview Prep — DevOps / SRE / Infrastructure

> DevOps interviews test different things than SWE interviews. Less LeetCode. More Linux, networking, systems design for reliability, and how you think through incidents.

---

## What to expect

| Round | What they test |
|---|---|
| Recruiter screen | Same as any track — background, interest, basics |
| Technical screen | Linux commands, scripting (bash/Python), basic networking |
| Systems design | Design a CI/CD pipeline, design for high availability, design a monitoring system |
| Incident response | Walk through how you'd diagnose and resolve a production issue |
| Coding (sometimes) | Light scripting problems, not full LeetCode — automate a task, parse logs |

---

## Linux fundamentals — expect these

- File permissions (chmod, chown, what 755 means)
- Process management (ps, top, kill, systemctl)
- Networking commands (netstat, ss, curl, dig, traceroute)
- Disk and memory (df, du, free, lsof)
- Log files (journalctl, /var/log, grep through logs)
- What happens when you type a URL in a browser — know this cold (DNS → TCP → TLS → HTTP → response)

---

## Networking fundamentals — expect these

- DNS: how resolution works, what a TTL is, difference between A/CNAME/MX records
- TCP vs UDP: when you'd use each
- Load balancing: L4 vs L7, round robin vs least connections
- Common ports: 22 SSH, 80 HTTP, 443 HTTPS, 5432 Postgres, 6379 Redis
- NAT, subnets, CIDR notation basics

---

## Systems design for reliability

Common prompts:
- Design a CI/CD pipeline for a web app
- How would you make this service highly available?
- Design a monitoring and alerting system
- How would you handle a database that's getting too large?

Framework for reliability design questions:
- **Single points of failure** — what breaks if X goes down?
- **Redundancy** — active-active vs active-passive
- **Observability** — metrics, logs, traces (the three pillars)
- **Deployment strategy** — blue/green, canary, rolling

---

## Incident response — how to answer these

> "Production is down. Users can't log in. Walk me through how you'd diagnose it."

As a new grad, you won't have real on-call experience — and interviewers know that. They're not testing whether you've been paged at 3am. They're testing whether you think systematically under pressure. Show your process:

Don't panic. Don't jump to solutions. Show your process:
1. What do you know? (symptoms, scope, when it started)
2. What do you check first? (dashboards, logs, recent deploys)
3. How do you narrow it down? (is it DNS? the app? the database? the network?)
4. How do you communicate while diagnosing? (who do you notify, how often)
5. How do you resolve and verify it's fixed?

The answer isn't the right diagnosis. It's showing a calm, methodical process.

---

## Portfolio — what to build

A well-documented project showing the full DevOps stack is worth more than any certification for getting your first interview.

- Deploy an app on AWS/GCP using Terraform — infrastructure defined as code, not clicked together in the console
- Set up a CI/CD pipeline with GitHub Actions — test, build, deploy on every push
- Add monitoring and alerting — Prometheus + Grafana, or a cloud-native equivalent
- Document the architecture — a README explaining design decisions, not just commands

**Cloud certifications worth pursuing** (these signal something in DevOps, unlike most SWE certs):
- AWS Solutions Architect Associate — broad cloud fundamentals, widely recognized
- CKA (Certified Kubernetes Administrator) — hands-on, practical, respected by hiring managers
- HashiCorp Terraform Associate — signals IaC proficiency

---

## Realistic entry points for new grads

Most DevOps/Platform Eng roles prefer people who've shipped software before. Realistic paths in:

- **SWE first, pivot after 1-2 years** — most common. Learn what you're building infra for, then move into platform/SRE
- **Cloud consulting** — firms like Accenture, Deloitte, Slalom cloud practices hire new grads for cloud roles. Lower comp, real experience, structured path
- **SRE new grad at companies with explicit programs** — Google has a well-known SRE campus hiring track. Check company career pages directly for "new grad SRE" or "university SRE"
- **Smaller companies** — a startup or mid-size company where "DevOps" means one person doing everything is real experience, even if the title is vague
