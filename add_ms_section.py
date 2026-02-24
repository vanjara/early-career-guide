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
    return result.get("results", []) if result else []

def rich_text(content):
    return [{"type": "text", "text": {"content": content}}]

def bullet(content):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rich_text(content)}}

def callout(content, emoji="💡"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": rich_text(content), "icon": {"type": "emoji", "emoji": emoji}}}

def toggle(title, children):
    return {"object": "block", "type": "toggle",
            "toggle": {"rich_text": rich_text(title), "children": children}}

def para(content):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": rich_text(content)}}

# Find Start Here page
children = get_children(PARENT_ID)
start_here_id = next((b["id"] for b in children
    if b.get("type") == "child_page" and "Start Here" in b.get("child_page", {}).get("title", "")), None)

print(f"Start Here page: {start_here_id}")

blocks = get_children(start_here_id)

# Find the "Who this is for" heading and the bullets after it
who_heading_id = None
last_bullet_id = None
in_who_section = False

for block in blocks:
    btype = block.get("type", "")
    if btype == "heading_2":
        texts = block.get("heading_2", {}).get("rich_text", [])
        heading_text = "".join(t.get("text", {}).get("content", "") for t in texts)
        if "Who this is for" in heading_text:
            who_heading_id = block["id"]
            in_who_section = True
        elif in_who_section:
            # Hit the next heading — stop
            in_who_section = False
    elif in_who_section and btype == "bulleted_list_item":
        last_bullet_id = block["id"]

print(f"Last bullet in 'Who this is for': {last_bullet_id}")

# Insert MS bullet + toggle after the last existing bullet
ms_blocks = [
    bullet("Master's students (MS in CS, data science, analytics, finance) transitioning or pivoting"),
    toggle("If you're an MS student, read this first", [
        para("An MS degree opens some doors and is irrelevant at others. Here's the honest version:"),
        bullet("Where it matters: ML/AI research, quant roles (Jane Street, Citadel), grad-specific consulting tracks (BCG, McKinsey associate), data scientist (not analyst) roles at larger companies"),
        bullet("Where it doesn't: SWE roles at most tech companies, startups, PM roles, most analyst roles — these evaluate your skills and interviews, not your degree level"),
        bullet("Where it can hurt: If you're competing for entry-level roles built for undergrads while carrying grad-level salary expectations, recruiters will filter you out"),
        para("The positioning question matters more than the degree itself. Target roles that explicitly value a graduate degree or use it as a filter. Don't apply as if you're competing with undergrads — you're not, and you shouldn't want to be."),
        bullet("Thesis or capstone project → put it on GitHub with a real README, it's a portfolio item"),
        bullet("TA or research experience → frame it as leadership and communication, not just coursework"),
        bullet("Prior work experience (pre-MS) → lead with it, your MS reinforces it rather than replacing it"),
    ]),
]

result = api("PATCH", f"/blocks/{start_here_id}/children", {
    "children": ms_blocks,
    "after": last_bullet_id,
})

if result:
    print("✓ MS section added to 'Who this is for'")
else:
    print("✗ Failed")
