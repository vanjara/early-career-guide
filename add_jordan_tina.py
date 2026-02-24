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
        print(f"Error {e.code}: {e.read().decode()[:200]}")
        return None

def get_children(block_id):
    result = api("GET", f"/blocks/{block_id}/children?page_size=100")
    return result.get("results", []) if result else []

def table_row(cells):
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {"cells": cells}
    }

def cell(text, url=None):
    rt = {"type": "text", "text": {"content": text}}
    if url:
        rt["text"]["link"] = {"url": url}
    return [rt]

# Find People to Follow page
children = get_children(PARENT_ID)
people_page_id = next((b["id"] for b in children
    if b.get("type") == "child_page" and "People" in b.get("child_page", {}).get("title", "")), None)

print(f"People to Follow page: {people_page_id}")

# Find Tech table
blocks = get_children(people_page_id)
current_heading = ""
tech_table_id = None

for block in blocks:
    btype = block.get("type", "")
    if btype == "heading_2":
        texts = block.get("heading_2", {}).get("rich_text", [])
        current_heading = "".join(t.get("text", {}).get("content", "") for t in texts)
    elif btype == "table" and "Tech" in current_heading:
        tech_table_id = block["id"]
        break

print(f"Tech table ID: {tech_table_id}")

# Add Jordan Cutler and Tina Huang
result = api("PATCH", f"/blocks/{tech_table_id}/children", {
    "children": [
        table_row([
            cell("Jordan Cutler", "https://www.linkedin.com/in/jordancutler1/"),
            cell("Substack + LinkedIn"),
            cell("Author of High Growth Engineer newsletter. Ex-Pinterest senior engineer. Covers leveling up in SWE, promotion strategy, system design, and staff+ paths. Tactical and specific."),
        ]),
        table_row([
            cell("Tina Huang", "https://www.youtube.com/@TinaHuang1"),
            cell("YouTube + LinkedIn"),
            cell("Ex-Meta data scientist. Covers data science career, breaking in as a new grad, portfolio projects, and day-in-the-life content. One of the most credible voices for new grad data science job search."),
        ]),
    ]
})

if result:
    print("✓ Jordan Cutler and Tina Huang added to Tech track")
else:
    print("✗ Failed")
