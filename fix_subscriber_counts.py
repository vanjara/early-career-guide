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

def cell(text, url=None):
    rt = {"type": "text", "text": {"content": text}}
    if url:
        rt["text"]["link"] = {"url": url}
    return [rt]

# Updated descriptions without subscriber counts
UPDATES = {
    "Nana Janashia": {
        "url": "https://www.linkedin.com/in/nana-janashia",
        "platform": "YouTube + LinkedIn",
        "why": "TechWorld with Nana. The most accessible DevOps educator — Docker, Kubernetes, CI/CD, Terraform. Best starting point if you're new to the field.",
    },
    "Sid Palas": {
        "url": "https://www.linkedin.com/in/sid-palas",
        "platform": "YouTube + LinkedIn",
        "why": "DevOps Directive. Hands-on, project-based DevOps content. Terraform, Kubernetes, CI/CD pipelines. Practical over theoretical.",
    },
}

# Find People to Follow page
children = get_children(PARENT_ID)
people_id = next((b["id"] for b in children
    if b.get("type") == "child_page" and "People to Follow" in b.get("child_page", {}).get("title", "")), None)

blocks = get_children(people_id)

# Find all tables and scan rows
updated = 0
for block in blocks:
    if block.get("type") != "table":
        continue
    rows = get_children(block["id"])
    for row in rows:
        if row.get("type") != "table_row":
            continue
        cells = row.get("table_row", {}).get("cells", [])
        if not cells:
            continue
        name = "".join(rt.get("text", {}).get("content", "") for rt in cells[0])
        if name in UPDATES:
            u = UPDATES[name]
            api("PATCH", f"/blocks/{row['id']}", {
                "table_row": {"cells": [
                    cell(name, u["url"]),
                    cell(u["platform"]),
                    cell(u["why"]),
                ]}
            })
            time.sleep(0.3)
            print(f"  ✓ Updated {name}")
            updated += 1

print(f"\n✓ {updated} rows updated.")
