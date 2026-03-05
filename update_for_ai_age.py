import json
import os
import urllib.request
import urllib.error
import time

TOKEN = os.environ["NOTION_TOKEN"]
PARENT_ID = os.environ.get("NOTION_PARENT_PAGE_ID", "311b3490-e35a-80bb-afcf-fb14f5a27feb")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def api(method, path, data=None):
    url = f"https://api.notion.com/v1{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  Error {e.code}: {e.read().decode()[:200]}")
        return None

def get_children(block_id):
    result = api("GET", f"/blocks/{block_id}/children?page_size=100")
    blocks = result.get("results", []) if result else []
    while result and result.get("has_more"):
        cursor = result.get("next_cursor")
        result = api("GET", f"/blocks/{block_id}/children?page_size=100&start_cursor={cursor}")
        if result:
            blocks.extend(result.get("results", []))
    return blocks

def append_blocks(block_id, blocks):
    # Chunk into 100
    for i in range(0, len(blocks), 100):
        api("PATCH", f"/blocks/{block_id}/children", {"children": blocks[i:i+100]})
        time.sleep(0.3)

def text(content, bold=False):
    t = {"type": "text", "text": {"content": content}}
    if bold:
        t["annotations"] = {"bold": True}
    return t

def link_text(content, url):
    return {"type": "text", "text": {"content": content, "link": {"url": url}}}

def h1(content): return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [text(content)]}}
def h2(content): return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [text(content)]}}
def h3(content): return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [text(content)]}}
def para(content): return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text(content)] if isinstance(content, str) else content}}
def bullet(content): return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [text(content)] if isinstance(content, str) else content}}
def numbered(content): return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [text(content)]}}
def callout(content, emoji="💡"): return {"object": "block", "type": "callout", "callout": {"rich_text": [text(content)], "icon": {"type": "emoji", "emoji": emoji}}}
def quote(content): return {"object": "block", "type": "quote", "quote": {"rich_text": [text(content)]}}
def divider(): return {"object": "block", "type": "divider", "divider": {}}
def toggle(title, children=None): return {"object": "block", "type": "toggle", "toggle": {"rich_text": [text(title)], "children": children or []}}

def table(rows):
    width = len(rows[0])
    return {
        "object": "block", "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                {"object": "block", "type": "table_row",
                 "table_row": {"cells": [[{"type": "text", "text": {"content": cell}}] for cell in row]}}
                for row in rows
            ]
        }
    }

def table_with_links(rows, link_col=0, urls=None):
    """Table where first column cells can be links"""
    urls = urls or {}
    width = len(rows[0])
    def make_cell(i, val):
        if i == link_col and val in urls:
            return [{"type": "text", "text": {"content": val, "link": {"url": urls[val]}}}]
        return [{"type": "text", "text": {"content": val}}]
    return {
        "object": "block", "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                {"object": "block", "type": "table_row",
                 "table_row": {"cells": [make_cell(i, cell) for i, cell in enumerate(row)]}}
                for row in rows
            ]
        }
    }

def create_page(parent_id, title, emoji, blocks):
    data = {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
        "children": blocks[:100]
    }
    result = api("POST", "/pages", data)
    if result and len(blocks) > 100:
        page_id = result["id"]
        for i in range(100, len(blocks), 100):
            api("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i+100]})
            time.sleep(0.3)
    return result

# ── GET ALL CHILD PAGES ───────────────────────────────────────────────────────
children = get_children(PARENT_ID)
pages_map = {b.get("child_page", {}).get("title", ""): b["id"]
             for b in children if b.get("type") == "child_page"}
print("Found pages:", list(pages_map.keys()))

# ── 1. CREATE AI AGE PAGE ─────────────────────────────────────────────────────
print("\nCreating: 🤖 Job Search in the AI Age...")

ai_age_blocks = [
    h1("Job Search in the AI Age"),
    callout("The old playbook is broken. AI tools have flooded recruiters with applications. The candidates getting hired are not the ones applying the most — they're the ones who are most known.", "🤖"),
    divider(),

    h2("What has changed"),
    para("AI tools have made it trivially easy to apply to hundreds of jobs. Everyone is doing it. Companies now receive 1,000–2,000 applications for roles that used to get 200. Entry-level roles are the hardest hit — AI has compressed a lot of what new grads used to be hired to do."),
    callout("The old model: optimize resume → apply broadly → get interviews → convert.\n\nThe new model: build presence → get found → apply selectively → convert.", "💡"),
    divider(),

    h2("The honest timeline"),
    quote("Strong candidate, doing everything right: 3–6 months\nAverage candidate, spray and pray: 6–12 months, no guarantee\nOPT candidates: Start 6 months before graduation — not 60 days"),
    divider(),

    h2("What actually works now"),

    h3("1. Build presence — be findable, not just searchable"),
    para("A recruiter or hiring manager who finds you is worth more than 50 applications you send."),
    toggle("💻 Tech (SWE, Data Engineering, Data Science)", [
        bullet("GitHub with real projects — not tutorials, things you actually built"),
        bullet("READMEs that explain your thinking, not just your code"),
        bullet("Contributions to open source — even small ones signal you can work in a real codebase"),
        bullet("Portfolio site if you have projects worth showing"),
    ]),
    toggle("📊 Data Analytics", [
        bullet("Published analyses on Kaggle, GitHub, or a personal site"),
        bullet("Show: business question → approach → answer → what you'd do differently"),
        bullet("Not 'I analyzed this dataset' — 'here's what I found and why it matters'"),
    ]),
    toggle("💰 Finance / Consulting", [
        bullet("Write about a company you've analyzed — what's their problem, what would you do"),
        bullet("Post your take on a deal, earnings report, or market trend"),
        bullet("One good piece of public thinking beats 50 anonymous applications"),
    ]),
    toggle("All tracks — LinkedIn content", [
        bullet("One post per week about something you learned, built, or figured out is enough"),
        bullet("Write about problems you solved, not just positions you've held"),
        bullet("Recruiters search LinkedIn by skill and keyword — your content indexes you"),
    ]),
    divider(),

    h3("2. Use AI to research and prepare — not to mass-apply"),
    callout("Most candidates use AI to write generic cover letters at scale. Use it differently.", "💡"),
    toggle("For company research", [
        para("Use ChatGPT or Perplexity to summarize a company's recent earnings, strategy, challenges, and competitive position before every interview and targeted application."),
    ]),
    toggle("For interview prep", [
        para("Simulate interviews with AI. Give it the job description and ask it to interview you. Ask it to push back on your answers. More effective than reading prep guides."),
    ]),
    toggle("For resume tailoring", [
        para("Paste the job description and your resume. Ask AI to identify gaps and suggest specific language. Do this for every application — not the cover letter, the resume keywords."),
    ]),
    toggle("For networking prep", [
        para("Ask AI to help you understand someone's background before a call. 'This person worked at X and Y, transitioned from A to B — what questions should I ask?' Preparation makes every conversation better."),
    ]),
    divider(),

    h3("3. Referrals are now the primary channel — not a supplement"),
    para("In the current market, for competitive roles, a referral is often the only way your resume gets seen by a human."),
    quote("Old approach: find 30 companies with open roles → apply\n\nNew approach: find 30 companies you want to work at → find someone who works there → have a conversation → apply with a referral → repeat\n\nThe application is the last step, not the first."),
    divider(),

    h3("4. Apply to fewer companies, with more depth"),
    para("Instead of 10–15 applications per week, think 3–5 — with genuine research behind each one."),
    para("For every targeted application:"),
    bullet("Read their recent news, earnings, or product updates"),
    bullet("Understand what the team is working on"),
    bullet("Tailor your resume to mirror their exact language"),
    bullet("Reference something specific in your outreach"),
    callout("Depth is the differentiator in a market where everyone is applying everywhere.", "💡"),
    divider(),

    h3("5. Skills that stand out in an AI market"),
    para("AI can generate code, run queries, and write first drafts. It cannot own outcomes, navigate ambiguity, or build relationships."),
    table([
        ["Track", "What stands out now"],
        ["Tech", "System design, debugging complex problems, owning a project end-to-end, clear technical communication"],
        ["Data", "Framing the right business question, communicating findings to non-technical stakeholders, judgment about what to measure"],
        ["Finance", "Client relationships, judgment in ambiguous situations, synthesizing qualitative and quantitative signals"],
        ["All tracks", "Written communication, structured thinking, ability to learn fast"],
    ]),
    divider(),

    h2("AI tools that actually help"),
    table_with_links([
        ["Tool", "How to use it"],
        ["ChatGPT / Claude", "Company research, interview simulation, resume tailoring, outreach drafts"],
        ["Perplexity", "Real-time company and industry research before interviews"],
        ["LinkedIn (search, not feed)", "Find people to reach out to, research hiring managers"],
        ["Simplify.jobs", "Track applications and auto-fill forms — not to apply to 100 jobs, but to stay organized"],
        ["GitHub Copilot", "Build better portfolio projects faster"],
        ["Glassdoor / Blind", "Research interview processes and culture before applying"],
    ], link_col=0, urls={
        "ChatGPT / Claude": "https://chatgpt.com",
        "Perplexity": "https://www.perplexity.ai",
        "Simplify.jobs": "https://simplify.jobs",
        "GitHub Copilot": "https://github.com/features/copilot",
        "Glassdoor / Blind": "https://www.glassdoor.com",
    }),
    divider(),

    h2("What to stop doing"),
    callout("Stop doing these — they feel productive but don't convert.", "⚠️"),
    bullet("Auto-applying to 50+ jobs per week — signal-to-noise ratio is near zero"),
    bullet("Generic cover letters — if it could apply to any company, it adds no value"),
    bullet("Easy Apply for competitive roles — treat it as a last resort, not a strategy"),
    bullet("Spending weeks perfecting your resume before applying — good enough and out the door beats perfect and waiting"),
    bullet("Following up more than once after applying — it doesn't help and damages the relationship"),
    divider(),

    h2("The reframe"),
    callout("You are no longer competing on applications. You are competing on signal — the quality of your relationships, the visibility of your skills, and the specificity of your preparation.\n\nBuild presence. Build relationships. Apply selectively. That's the job search now.", "🤖"),
]

result = create_page(PARENT_ID, "Job Search in the AI Age", "🤖", ai_age_blocks)
if result:
    print("  ✓ AI Age page created")
else:
    print("  ✗ Failed")

# ── 2. UPDATE START HERE — TIMELINE ──────────────────────────────────────────
print("\nUpdating Start Here — timeline and AI callout...")

start_here_id = pages_map.get("Start Here")
if start_here_id:
    blocks = get_children(start_here_id)

    # Find and delete the old quote block (timeline), replace with new one
    for block in blocks:
        if block.get("type") == "quote":
            old_text = "".join(rt.get("text", {}).get("content", "")
                               for rt in block.get("quote", {}).get("rich_text", []))
            if "8" in old_text or "weeks" in old_text:
                # Update this block
                api("PATCH", f"/blocks/{block['id']}", {
                    "quote": {"rich_text": [{"type": "text", "text": {"content":
                        "Strong candidate, doing everything right: 3–6 months\n"
                        "Average candidate, spray and pray: 6–12 months, no guarantee\n"
                        "OPT candidates: Start 6 months before graduation — not 60 days\n\n"
                        "If you're in month 2 and discouraged — that's normal.\n"
                        "If you're in month 5 with no traction — something in your system needs to change."
                    }}]}
                })
                print("  ✓ Timeline updated")
                break

    # Add AI callout at the top (after H1)
    for i, block in enumerate(blocks):
        if block.get("type") == "heading_1":
            # Add a callout right after H1
            append_blocks(start_here_id, [
                callout("The job search has changed. AI has flooded recruiters with applications. Read the AI Age section before you start. The timeline and strategy here reflect the current market — not 2022.", "🤖"),
            ])
            print("  ✓ AI callout added to Start Here")
            break

# ── 3. UPDATE JOB SEARCH STRATEGY — ADD AI CONTEXT ───────────────────────────
print("\nUpdating Job Search Strategy — adding AI market context...")

strategy_id = pages_map.get("Job Search Strategy")
if strategy_id:
    # Add a callout at the top about the AI market
    strategy_blocks = get_children(strategy_id)
    for block in strategy_blocks:
        if block.get("type") == "heading_1":
            append_blocks(strategy_id, [
                callout("In 2025+, Easy Apply is even less effective than it used to be. AI auto-apply tools mean companies receive 1,000–2,000 applications for roles that used to get 200. The approach below matters more than ever — but the primary strategy has shifted to building presence and referrals. See the AI Age section.", "🤖"),
            ])
            print("  ✓ AI context added to Job Search Strategy")
            break

# ── 4. ADD AI INFLUENCERS TO PEOPLE TO FOLLOW ─────────────────────────────────
print("\nAdding AI influencers to People to Follow...")

people_id = pages_map.get("People to Follow")
if people_id:
    # Add a new AI section at the end
    append_blocks(people_id, [
        divider(),
        h2("AI & Tech Tools Track"),
        para("Follow these for staying current on AI tools, workflows, and how AI is changing careers and work."),
        table_with_links([
            ["Person", "Platform", "Why follow"],
            ["Ruben Hassid", "LinkedIn + YouTube", "One of the most followed AI content creators. Practical AI tools and workflows for productivity and job search. Very hands-on."],
            ["Boris Cherny", "LinkedIn + Substack", "Creator of Claude Code and Head of Claude Code at Anthropic. Shares how AI is changing software development and what developers should be building toward. Essential if you're going into SWE or AI."],
            ["Owain Lewis", "LinkedIn + Substack", "AI Engineer and writer of the Leverage AI newsletter. Practical content on how to use AI to automate work, build systems, and create leverage as an individual contributor."],
            ["Andrej Karpathy", "X (Twitter) + YouTube", "Ex-Tesla AI director, ex-OpenAI. Best explainer of how AI/ML actually works. Essential for anyone in AI/ML roles."],
            ["Ethan Mollick", "Substack (One Useful Thing)", "Wharton professor researching AI in the workplace. Most credible voice on how AI changes work, hiring, and careers. Read before every interview at an AI-adjacent company."],
            ["Simon Willison", "Blog + X (Twitter)", "Creator of Datasette, prolific AI tools researcher. Best for understanding what AI tools can actually do vs. the hype."],
            ["Lenny Rachitsky", "Substack + YouTube", "Product and growth careers, increasingly AI-focused. Best for anyone pursuing PM or growth roles at tech companies."],
        ], link_col=0, urls={
            "Ruben Hassid": "https://www.linkedin.com/in/rubenhassid/",
            "Boris Cherny": "https://www.linkedin.com/in/bcherny/",
            "Owain Lewis": "https://www.linkedin.com/in/theowainlewis/",
            "Andrej Karpathy": "https://www.youtube.com/@AndrejKarpathy",
            "Ethan Mollick": "https://www.oneusefulthing.org",
            "Simon Willison": "https://simonwillison.net",
            "Lenny Rachitsky": "https://www.lennysnewsletter.com",
        }),
    ])
    print("  ✓ AI influencers section added")

# ── 5. UPDATE TABLE OF CONTENTS IN START HERE ─────────────────────────────────
print("\nUpdating Start Here table of contents...")

if start_here_id:
    blocks = get_children(start_here_id)
    for block in blocks:
        if block.get("type") == "table":
            rows = get_children(block["id"])
            if len(rows) > 1:
                # Add new row for AI Age
                api("PATCH", f"/blocks/{block['id']}/children", {"children": [
                    {"object": "block", "type": "table_row",
                     "table_row": {"cells": [
                         [{"type": "text", "text": {"content": "🤖 Job Search in the AI Age"}}],
                         [{"type": "text", "text": {"content": "New market reality, AI tools, building presence, honest timeline"}}],
                     ]}}
                ]})
                print("  ✓ AI Age added to Start Here table of contents")
                break

print("\n✓ All updates complete.")
