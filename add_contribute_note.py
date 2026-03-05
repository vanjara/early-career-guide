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

# Find Start Here page
children = get_children(PARENT_ID)
start_here_id = next((b["id"] for b in children
    if b.get("type") == "child_page" and "Start Here" in b.get("child_page", {}).get("title", "")), None)

# Append contribute note at the bottom
api("PATCH", f"/blocks/{start_here_id}/children", {"children": [
    {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [
                {"type": "text", "text": {"content": "Found something outdated or missing? "}},
                {"type": "text", "text": {
                    "content": "Suggest an improvement on GitHub.",
                    "link": {"url": "https://github.com/vanjara/early-career-guide/issues/new"}
                }},
            ],
            "icon": {"type": "emoji", "emoji": "✏️"},
            "color": "gray_background"
        }
    }
]})

print("✓ Contribute note added to Start Here")
