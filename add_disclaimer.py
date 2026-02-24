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

DISCLAIMER = ("This guide is maintained by volunteers and reflects our best understanding of the job market. "
              "Company hiring practices, visa rules, and market conditions change. "
              "Verify anything time-sensitive before acting on it. Last updated: February 2026.")

def disclaimer_block():
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": DISCLAIMER}}],
            "icon": {"type": "emoji", "emoji": "⚠️"}
        }
    }

def insert_after_h1(page_id, page_name):
    blocks = get_children(page_id)
    h1_id = None
    for block in blocks:
        if block.get("type") in ("heading_1", "heading_2"):
            h1_id = block["id"]
            break
    if not h1_id:
        # Fall back to inserting after first block
        h1_id = blocks[0]["id"] if blocks else None
    if not h1_id:
        print(f"  ✗ No blocks found in {page_name}")
        return
    api("PATCH", f"/blocks/{page_id}/children", {
        "children": [disclaimer_block()],
        "after": h1_id
    })
    time.sleep(0.4)
    print(f"  ✓ {page_name}")

# Get all pages
children = get_children(PARENT_ID)
pages_map = {b.get("child_page", {}).get("title", ""): b["id"]
             for b in children if b.get("type") == "child_page"}
print("Found pages:", list(pages_map.keys()))

# Pages to add disclaimer to
target_pages = [
    "Start Here",
    "Resume",
    "Job Boards",
    "Job Search Strategy",
    "Networking",
    "Interview Prep",
    "Offer & Negotiation",
    "Benefits",
    "Visa / OPT Track",
    "People to Follow",
    "Job Search in the AI Age",
]

print("\nAdding disclaimer to all pages...")
for name in target_pages:
    page_id = pages_map.get(name)
    if page_id:
        insert_after_h1(page_id, name)
    else:
        print(f"  ✗ Not found: {name}")

print("\n✓ Done.")
