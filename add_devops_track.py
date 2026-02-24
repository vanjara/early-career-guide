import json
import urllib.request
import urllib.error
import time

TOKEN = "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"
PARENT_ID = "311b3490-e35a-80bb-afcf-fb14f5a27feb"
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
        print(f"  Error {e.code}: {e.read().decode()[:300]}")
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

def rt(content, bold=False):
    t = {"type": "text", "text": {"content": content}}
    if bold:
        t["annotations"] = {"bold": True}
    return t

def h2(content):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [rt(content)]}}

def h3(content):
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [rt(content)]}}

def para(content):
    parts = [rt(content)] if isinstance(content, str) else content
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": parts}}

def bullet(content):
    parts = [rt(content)] if isinstance(content, str) else content
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": parts}}

def callout(content, emoji="💡"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [rt(content)], "icon": {"type": "emoji", "emoji": emoji}}}

def quote(content):
    return {"object": "block", "type": "quote", "quote": {"rich_text": [rt(content)]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def toggle(title, children):
    return {"object": "block", "type": "toggle",
            "toggle": {"rich_text": [rt(title)], "children": children}}

def table(rows, has_header=True):
    return {
        "object": "block", "type": "table",
        "table": {
            "table_width": len(rows[0]),
            "has_column_header": has_header,
            "has_row_header": False,
            "children": [
                {"object": "block", "type": "table_row",
                 "table_row": {"cells": [[{"type": "text", "text": {"content": cell}}] for cell in row]}}
                for row in rows
            ]
        }
    }

def table_with_links(rows, urls):
    """First column cells linked if name in urls dict"""
    def make_cell(i, val):
        if i == 0 and val in urls:
            return [{"type": "text", "text": {"content": val, "link": {"url": urls[val]}}}]
        return [{"type": "text", "text": {"content": val}}]
    return {
        "object": "block", "type": "table",
        "table": {
            "table_width": len(rows[0]),
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                {"object": "block", "type": "table_row",
                 "table_row": {"cells": [make_cell(i, cell) for i, cell in enumerate(row)]}}
                for row in rows
            ]
        }
    }

def append(block_id, blocks):
    for i in range(0, len(blocks), 100):
        api("PATCH", f"/blocks/{block_id}/children", {"children": blocks[i:i+100]})
        time.sleep(0.3)

def append_after(parent_id, blocks, after_id):
    api("PATCH", f"/blocks/{parent_id}/children", {
        "children": blocks,
        "after": after_id
    })

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

# ── 1. PEOPLE TO FOLLOW — ADD DEVOPS SECTION ─────────────────────────────────
print("\nAdding DevOps section to People to Follow...")

people_id = pages_map.get("People to Follow")
if people_id:
    append(people_id, [
        divider(),
        h2("DevOps / Platform Engineering / Infrastructure Track"),
        para("Follow these for DevOps tools, cloud infra, Kubernetes, and breaking into the SRE/DevOps field."),
        table_with_links([
            ["Person", "Platform", "Why follow"],
            ["Nana Janashia", "YouTube + LinkedIn", "TechWorld with Nana. 1.3M subscribers. The most accessible DevOps educator — Docker, Kubernetes, CI/CD, Terraform. Best starting point if you're new to the field."],
            ["Sid Palas", "YouTube + LinkedIn", "DevOps Directive. Hands-on, project-based DevOps content. Terraform, Kubernetes, CI/CD pipelines. Practical over theoretical."],
            ["Kunal Kushwaha", "YouTube + LinkedIn", "CNCF Ambassador. DevOps bootcamp, platform engineering, cloud-native tools. Strong community around breaking into DevOps."],
            ["Kelsey Hightower", "X (Twitter)", "Former Staff Engineer at Google, one of the most respected voices in Kubernetes and cloud-native infrastructure. Fewer posts but high signal."],
        ], urls={
            "Nana Janashia": "https://www.linkedin.com/in/nana-janashia",
            "Sid Palas": "https://www.linkedin.com/in/sid-palas",
            "Kunal Kushwaha": "https://www.linkedin.com/in/kunal-kushwaha",
            "Kelsey Hightower": "https://twitter.com/kelseyhightower",
        }),
    ])
    print("  ✓ DevOps people added")

# ── 2. JOB BOARDS — ADD DEVOPS SECTION ───────────────────────────────────────
print("\nAdding DevOps section to Job Boards...")

jobboards_id = pages_map.get("Job Boards")
if jobboards_id:
    blocks = get_children(jobboards_id)
    # Find the last table (recommended setup) — append DevOps section before it
    # Strategy: just append to end of page
    append(jobboards_id, [
        divider(),
        h2("DevOps / SRE / Infrastructure track"),
        table_with_links([
            ["Platform", "Best for", "Notes"],
            ["CNCF Job Board", "Cloud-native, Kubernetes, SRE", "jobs.cncf.io — roles at companies building cloud-native infrastructure. High signal, smaller volume."],
            ["Hired.com", "SRE, DevOps, infrastructure", "Strong for DevOps and infrastructure roles at mid-to-large tech companies."],
            ["LinkedIn (targeted)", "SRE, DevOps, Platform Eng", "Search 'site reliability engineer' or 'platform engineer' — filter by entry level. Apply directly, not Easy Apply."],
            ["Wellfound (AngelList)", "Startup DevOps/infra roles", "Startups often hire generalist engineers who own infra. Good for early-stage companies."],
            ["Company career pages", "Big tech SRE", "Google, Cloudflare, Datadog, HashiCorp, Grafana Labs, AWS — check directly for SRE and infra roles."],
        ], urls={
            "CNCF Job Board": "https://jobs.cncf.io",
            "Hired.com": "https://hired.com",
            "Wellfound (AngelList)": "https://wellfound.com",
        }),
        callout("Cloud consulting firms — Accenture, Deloitte, Slalom, Cognizant cloud practices — hire new grads for cloud infrastructure roles. Lower comp than product companies but structured training and real cloud experience. Worth considering as an entry point.", "💡"),
        para(""),
        h3("Communities where DevOps job leads happen"),
        bullet("CNCF Slack (#jobs channel) — cloud-native community, real job posts"),
        bullet("DevOps subreddits: r/devops, r/kubernetes, r/sre"),
        bullet("Kubernetes Slack — active community, occasional job posts"),
        bullet("Hangops Slack — DevOps community with job board channel"),
    ])
    print("  ✓ DevOps job boards added")

# ── 3. INTERVIEW PREP — ADD DEVOPS/INFRA SECTION ─────────────────────────────
print("\nAdding DevOps/Infra section to Interview Prep...")

interview_id = pages_map.get("Interview Prep")
if interview_id:
    append(interview_id, [
        divider(),
        h2("DevOps / SRE / Infrastructure track"),
        callout("DevOps interviews test different things than SWE interviews. Less LeetCode. More Linux, networking, systems design for reliability, and how you think through incidents.", "💡"),
        para(""),
        h3("What to expect"),
        table([
            ["Round", "What they test"],
            ["Recruiter screen", "Same as any track — background, interest, basics"],
            ["Technical screen", "Linux commands, scripting (bash/Python), basic networking"],
            ["Systems design", "Design a CI/CD pipeline, design for high availability, design a monitoring system"],
            ["Incident response", "Walk through how you'd diagnose and resolve a production issue"],
            ["Coding (sometimes)", "Light scripting problems, not full LeetCode — automate a task, parse logs"],
        ]),
        para(""),
        h3("Linux fundamentals — expect these"),
        bullet("File permissions (chmod, chown, what 755 means)"),
        bullet("Process management (ps, top, kill, systemctl)"),
        bullet("Networking commands (netstat, ss, curl, dig, traceroute)"),
        bullet("Disk and memory (df, du, free, lsof)"),
        bullet("Log files (journalctl, /var/log, grep through logs)"),
        bullet("What happens when you type a URL in a browser — know this cold (DNS → TCP → TLS → HTTP → response)"),
        para(""),
        h3("Networking fundamentals — expect these"),
        bullet("DNS: how resolution works, what a TTL is, difference between A/CNAME/MX records"),
        bullet("TCP vs UDP: when you'd use each"),
        bullet("Load balancing: L4 vs L7, round robin vs least connections"),
        bullet("Ports: common ones (22 SSH, 80 HTTP, 443 HTTPS, 5432 Postgres, 6379 Redis)"),
        bullet("NAT, subnets, CIDR notation basics"),
        para(""),
        h3("Systems design for reliability"),
        para("Common prompts:"),
        bullet("Design a CI/CD pipeline for a web app"),
        bullet("How would you make this service highly available?"),
        bullet("Design a monitoring and alerting system"),
        bullet("How would you handle a database that's getting too large?"),
        para(""),
        para("Framework for reliability design questions:"),
        bullet("Single points of failure — what breaks if X goes down?"),
        bullet("Redundancy — active-active vs active-passive"),
        bullet("Observability — metrics, logs, traces (the three pillars)"),
        bullet("Deployment strategy — blue/green, canary, rolling"),
        para(""),
        h3("Incident response — how to answer these"),
        quote("'Production is down. Users can't log in. Walk me through how you'd diagnose it.'\n\nDon't panic. Don't jump to solutions. Show your process:\n1. What do you know? (symptoms, scope, when it started)\n2. What do you check first? (dashboards, logs, recent deploys)\n3. How do you narrow it down? (is it DNS? the app? the database? the network?)\n4. How do you communicate while diagnosing? (who do you notify, how often)\n5. How do you resolve and verify it's fixed?\n\nThe answer isn't the right diagnosis. It's showing a calm, methodical process."),
        para(""),
        h3("Portfolio — what to build"),
        callout("A well-documented project showing the full stack of DevOps skills is worth more than any certification for getting your first interview.", "💡"),
        bullet("Deploy an app on AWS/GCP using Terraform — infrastructure defined as code, not clicked together in the console"),
        bullet("Set up a CI/CD pipeline with GitHub Actions — test, build, deploy on every push"),
        bullet("Add monitoring and alerting — Prometheus + Grafana, or a cloud-native equivalent"),
        bullet("Document the architecture — a README that explains the design decisions, not just the commands"),
        para("Cloud certifications worth pursuing (these actually signal something in DevOps, unlike most SWE certs):"),
        bullet("AWS Solutions Architect Associate — broad cloud fundamentals, widely recognized"),
        bullet("CKA (Certified Kubernetes Administrator) — hands-on, practical, respected by hiring managers"),
        bullet("HashiCorp Terraform Associate — signals IaC proficiency"),
        para(""),
        h3("Realistic entry points for new grads"),
        para("Most DevOps/Platform Eng roles prefer people who've shipped software before. The realistic paths in:"),
        bullet("SWE first, pivot after 1-2 years — most common. Learn what you're building infra for, then move into platform/SRE"),
        bullet("Cloud consulting — firms like Accenture, Deloitte, Slalom cloud practices hire new grads for cloud roles. Lower comp, real experience, structured path"),
        bullet("SRE new grad at companies with explicit programs — Google has a well-known SRE campus hiring track. Check company career pages directly for 'new grad SRE' or 'university SRE'"),
        bullet("Smaller companies — a startup or mid-size company where 'DevOps' means one person doing everything is real experience, even if the title is vague"),
    ])
    print("  ✓ DevOps interview prep added")

# ── 4. START HERE — ADD DEVOPS TO WHO THIS IS FOR ────────────────────────────
print("\nUpdating Start Here...")

start_here_id = pages_map.get("Start Here")
if start_here_id:
    blocks = get_children(start_here_id)
    # Find last bullet in "Who this is for" section
    in_who = False
    last_bullet_id = None
    for block in blocks:
        btype = block.get("type", "")
        if btype == "heading_2":
            texts = block.get("heading_2", {}).get("rich_text", [])
            heading = "".join(t.get("text", {}).get("content", "") for t in texts)
            if "Who this is for" in heading:
                in_who = True
            elif in_who:
                in_who = False
        elif in_who and btype in ("bulleted_list_item", "toggle"):
            last_bullet_id = block["id"]

    if last_bullet_id:
        append_after(start_here_id, [
            bullet("Early career professionals targeting DevOps, SRE, Platform Engineering, or cloud infrastructure roles"),
        ], last_bullet_id)
        print("  ✓ DevOps added to Who this is for")

    # Add DevOps row to table of contents
    for block in blocks:
        if block.get("type") == "table":
            rows = get_children(block["id"])
            if len(rows) > 3:
                api("PATCH", f"/blocks/{block['id']}/children", {"children": [
                    {"object": "block", "type": "table_row",
                     "table_row": {"cells": [
                         [{"type": "text", "text": {"content": "⚙️ DevOps / SRE / Infra Track"}}],
                         [{"type": "text", "text": {"content": "Entry points, skills, portfolio, interview prep for infra careers"}}],
                     ]}}
                ]})
                print("  ✓ DevOps added to table of contents")
                break

print("\n✓ All DevOps track updates complete.")
