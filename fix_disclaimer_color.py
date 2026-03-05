import json
import urllib.request
import urllib.error
import time

TOKEN = "YOUR_NOTION_TOKEN"
PARENT_ID = "311b3490-e35a-80bb-afcf-fb14f5a27feb"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

DISCLAIMER = ("This guide is maintained by volunteers and reflects our best understanding of the job market. "
              "Company hiring practices, visa rules, and market conditions change. "
              "Verify anything time-sensitive before acting on it. Last updated: February 2026.")

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

children = get_children(PARENT_ID)
pages = [b for b in children if b.get("type") == "child_page"]
print(f"Found {len(pages)} pages")

updated = 0
for page in pages:
    page_id = page["id"]
    page_title = page.get("child_page", {}).get("title", "")
    blocks = get_children(page_id)
    for block in blocks:
        if block.get("type") != "callout":
            continue
        icon = block.get("callout", {}).get("icon", {})
        if icon.get("emoji") != "⚠️":
            continue
        # Check it's our disclaimer (not another warning callout)
        text = "".join(rt.get("text", {}).get("content", "")
                       for rt in block.get("callout", {}).get("rich_text", []))
        if "volunteers" not in text:
            continue
        api("PATCH", f"/blocks/{block['id']}", {
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": DISCLAIMER}}],
                "icon": {"type": "emoji", "emoji": "ℹ️"},
                "color": "gray_background"
            }
        })
        time.sleep(0.3)
        print(f"  ✓ {page_title}")
        updated += 1

print(f"\n✓ {updated} disclaimers updated.")
