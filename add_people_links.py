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

# People URLs — name as it appears in the table
PEOPLE_URLS = {
    # General
    "Laszlo Bock": "https://www.linkedin.com/in/laszlobock/",
    "Austin Belcak": "https://www.linkedin.com/in/austinbelcak/",
    "Jenny Foss": "https://www.linkedin.com/in/jennyfoss/",
    # Tech
    "Rahul Pandey": "https://www.linkedin.com/in/rahul-pandey1/",
    "Alex Chiou": "https://www.linkedin.com/in/alexander-chiou/",
    "Neetcode": "https://www.youtube.com/@NeetCode",
    "Gergely Orosz": "https://newsletter.pragmaticengineer.com",
    "Kevin Naughton Jr.": "https://www.youtube.com/@KevinNaughtonJr",
    # Data
    "Ken Jee": "https://www.youtube.com/@KenJee_DS",
    "Luke Barousse": "https://www.youtube.com/@LukeBarousse",
    "Alex Freberg (Alex The Analyst)": "https://www.youtube.com/@AlexTheAnalyst",
    "Seattle Data Guy": "https://www.youtube.com/@SeattleDataGuy",
    # Finance
    "Patrick Curtis": "https://www.linkedin.com/in/partrickcurtis/",
    "10x EBITDA": "https://www.youtube.com/@10xEBITDA",
    "Mergers & Inquisitions": "https://mergersandinquisitions.com",
    "Marc Cenedella": "https://www.linkedin.com/in/cenedella/",
    # Visa
    "Stacy Monahan Tucker": "https://www.linkedin.com/in/stacymonahantucker/",
    "Sophie Alcorn": "https://www.linkedin.com/in/sophiealcorn/",
    "Varun Negandhi": "https://www.linkedin.com/in/vnegandhi/",
    "Ishi Sodhi": "https://www.linkedin.com/in/ishi-sodhi-3b852a17/",
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
    return result.get("results", []) if result else []

def make_link_cell(text, url):
    return [{"type": "text", "text": {"content": text, "link": {"url": url}},
             "annotations": {"bold": False, "italic": False, "strikethrough": False,
                             "underline": False, "code": False, "color": "default"}}]

def make_plain_cell(text):
    return [{"type": "text", "text": {"content": text}}]

def process_table_row(row_block):
    cells = row_block.get("table_row", {}).get("cells", [])
    if not cells:
        return False
    cell_text = "".join(rt.get("text", {}).get("content", "") for rt in cells[0])
    if cell_text in PEOPLE_URLS:
        # Rebuild all cells, linking the first
        new_cells = [make_link_cell(cell_text, PEOPLE_URLS[cell_text])]
        for cell in cells[1:]:
            ct = "".join(rt.get("text", {}).get("content", "") for rt in cell)
            new_cells.append(make_plain_cell(ct) if ct else [{"type": "text", "text": {"content": ""}}])
        result = api("PATCH", f"/blocks/{row_block['id']}", {"table_row": {"cells": new_cells}})
        time.sleep(0.3)
        return result is not None
    return False

# Find People to Follow page
children = get_children(PARENT_ID)
people_page_id = next((b["id"] for b in children
    if b.get("type") == "child_page" and "People" in b.get("child_page", {}).get("title", "")), None)

print(f"People to Follow page: {people_page_id}")
blocks = get_children(people_page_id)
updates = 0

for block in blocks:
    if block.get("type") == "table":
        rows = get_children(block["id"])
        for row in rows:
            if row.get("type") == "table_row":
                if process_table_row(row):
                    updates += 1

print(f"✓ {updates} people linked")
