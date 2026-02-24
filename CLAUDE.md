# Early Career Guide — Project Context

## What this is
A free resource hub for new grads, early career professionals, and F-1/OPT candidates navigating the US job search. Built for friends and contacts.

## Tracks covered
- Tech (SWE, Data Engineering, Data Science)
- Data Analytics
- Finance / Consulting
- Visa / OPT
- DevOps / SRE / Platform Engineering / Infrastructure
- MS students (covered within existing tracks)

## Content standards

### Verify before writing
**This is the most important rule.** We only write things we can verify. Before adding any claim about:
- Company hiring practices ("Company X hires new grad SREs") — verify on their careers page or via credible source
- Timelines ("process takes N weeks") — verify or hedge with "typically" / "often"
- Salary ranges — use Levels.fyi, Glassdoor, or BLS data; note the source
- Certification value ("cert X is respected") — verify from hiring manager perspectives, not cert providers
- People / influencers — verify their background before writing their credentials

**When uncertain:** hedge the language ("typically", "often", "at some companies") or leave it out.

### Tone
- Practical over motivational
- Honest about difficulty — don't sugarcoat timelines or competition
- No hustle content
- No affiliation with any paid service, course, or recruiter

## Architecture
- GitHub (vanjara/early-career-guide) — source of truth, markdown files
- Notion — public-facing hub built via API

## Notion API
- Parent page ID: 311b3490-e35a-80bb-afcf-fb14f5a27feb
- Integration: Early Career Guide Builder (internal)
- Token: stored in scripts — revoke after use, do not commit to GitHub

## Key files
- `notion-import/` — clean markdown versions of all Notion pages
- `interview-prep/` — track-specific interview prep content
- `people-to-follow/README.md` — people list (markdown)
- `ai-age-job-search.md` — AI age section content
- Python scripts — one-off Notion API scripts, not a framework
