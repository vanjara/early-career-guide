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
        print(f"Error {e.code}: {e.read().decode()[:300]}")
        return None

def get_children(block_id):
    result = api("GET", f"/blocks/{block_id}/children?page_size=100")
    return result.get("results", []) if result else []

def cell(text, url=None):
    rt = {"type": "text", "text": {"content": text}}
    if url:
        rt["text"]["link"] = {"url": url}
    return [rt]

def table_row(cells):
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {"cells": cells}
    }

def append_blocks(block_id, blocks):
    return api("PATCH", f"/blocks/{block_id}/children", {"children": blocks})

# Find the People to Follow page
print("Finding People to Follow page...")
children = get_children(PARENT_ID)
people_page_id = None
for b in children:
    if b.get("type") == "child_page" and "People" in b.get("child_page", {}).get("title", ""):
        people_page_id = b["id"]
        break

if not people_page_id:
    print("Could not find People to Follow page")
    exit()

print(f"Found page: {people_page_id}")

# Get all blocks in the page
blocks = get_children(people_page_id)
print(f"Found {len(blocks)} blocks")

# Find tables by looking at surrounding headings
current_heading = ""
tech_table_id = None
visa_table_id = None

for i, block in enumerate(blocks):
    btype = block.get("type", "")

    if btype == "heading_2":
        texts = block.get("heading_2", {}).get("rich_text", [])
        current_heading = "".join(t.get("text", {}).get("content", "") for t in texts)
        print(f"  H2: {current_heading}")

    elif btype == "table":
        print(f"  Table found after heading: '{current_heading}'")
        if "Tech" in current_heading:
            tech_table_id = block["id"]
        elif "Visa" in current_heading or "OPT" in current_heading:
            visa_table_id = block["id"]

print(f"\nTech table ID: {tech_table_id}")
print(f"Visa/OPT table ID: {visa_table_id}")

# Add Alex Chiou to Tech table
if tech_table_id:
    print("\nAdding Alex Chiou to Tech track...")
    result = append_blocks(tech_table_id, [
        table_row([
            cell("Alex Chiou", "https://www.linkedin.com/in/alexander-chiou/"),
            cell("YouTube + LinkedIn"),
            cell("Co-founder of Taro (with Rahul Pandey), ex-Meta/Robinhood tech lead. Daily posting on career growth, leveling up in tech, and navigating big tech culture."),
        ])
    ])
    if result:
        print("  ✓ Alex Chiou added")
    time.sleep(0.5)

# Add Varun Negandhi and Ishi Sodhi to Visa/OPT table
if visa_table_id:
    print("\nAdding Varun Negandhi and Ishi Sodhi to Visa/OPT track...")
    result = append_blocks(visa_table_id, [
        table_row([
            cell("Varun Negandhi", "https://www.linkedin.com/in/vnegandhi/"),
            cell("LinkedIn"),
            cell("Founder of BeyondGrad. Specifically helps international students and immigrants navigate the US job search. Practical, not motivational."),
        ]),
        table_row([
            cell("Ishi Sodhi", "https://www.linkedin.com/in/ishi-sodhi-3b852a17/"),
            cell("LinkedIn"),
            cell("Global Mobility Programs Manager at Palo Alto Networks. 20 years in US immigration, came to US on F-1 herself. Posts on H1B, layoffs on visa, OPT — from an insider who builds these programs at companies."),
        ])
    ])
    if result:
        print("  ✓ Varun Negandhi and Ishi Sodhi added")

print("\nDone.")
