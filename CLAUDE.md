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
- Notion — public-facing hub, updated via scripts in scripts/
- GitHub Pages (vanjara.github.io/early-career-guide) — landing page only, links to Notion
- Sync direction: GitHub → Notion only. Never edit Notion directly — changes will be overwritten.

## Notion API
- Parent page ID: 311b3490-e35a-80bb-afcf-fb14f5a27feb
- Integration: Early Career Guide Builder (internal)
- Token: in .env as NOTION_TOKEN — never commit
- Page IDs and file mappings: scripts/pages.json
- Run scripts from project root: `set -a && source .env && set +a && python3 scripts/...`

## Notion block structure — critical
- Interview Prep tracks are TOGGLE blocks with children, not heading_2 blocks
- Always check block types before writing: `GET /blocks/{page_id}/children`
- Adding children to a heading only works if `is_toggleable: true`
- When appending to a page, blocks become direct siblings — heading_3 is NOT a child of heading_2
- Always read the existing page structure before writing anything

## Key files
- `scripts/pages.json` — Notion page IDs and markdown file mapping
- `scripts/sync_to_notion.py` — main sync script (TODO: build this)
- `interview-prep/` — track-specific interview prep content
- `people-and-resources/README.md` — pulled from Notion, reflects current state
- `ai-age-job-search.md` — AI age section content

## What still needs to be done
- Fix Interview Prep Notion page: delete malformed DevOps/DS heading blocks, re-add as toggle blocks
- Build scripts/sync_to_notion.py for GitHub → Notion sync
- Set up GitHub Actions to run sync on push to main
- Update CONTRIBUTING.md to reflect new workflow
- Commit all pending changes (nothing has been committed this session)

## Lessons from a badly run session (2026-03-06)
- Do not create throwaway scripts in /tmp — build reusable scripts in scripts/ from the start
- Do not change sync direction mid-session — decide once and commit to it
- Check Notion block types first, write second — wrong block type means rework
- Commit frequently — not one giant commit at the end of a 4-hour session
- Do not add content to Notion without checking existing page structure first
- One script that does everything > many small throwaway scripts
