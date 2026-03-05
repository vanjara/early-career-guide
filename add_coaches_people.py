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

def append(block_id, blocks):
    for i in range(0, len(blocks), 100):
        api("PATCH", f"/blocks/{block_id}/children", {"children": blocks[i:i+100]})
        time.sleep(0.3)

def cell(text, url=None):
    rt = {"type": "text", "text": {"content": text}}
    if url:
        rt["text"]["link"] = {"url": url}
    return [rt]

def table_row(cells):
    return {"object": "block", "type": "table_row", "table_row": {"cells": cells}}

def rt(content, bold=False):
    t = {"type": "text", "text": {"content": content}}
    if bold:
        t["annotations"] = {"bold": True}
    return t

def h2(content):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [rt(content)]}}

def para(content):
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [rt(content)]}}

def bullet(parts):
    if isinstance(parts, str):
        parts = [rt(parts)]
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": parts}}

def callout(content, emoji="💡"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [rt(content)], "icon": {"type": "emoji", "emoji": emoji}}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def table_with_links(rows, urls):
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
                 "table_row": {"cells": [make_cell(i, c) for i, c in enumerate(row)]}}
                for row in rows
            ]
        }
    }

# Get pages
children = get_children(PARENT_ID)
pages_map = {b.get("child_page", {}).get("title", ""): b["id"]
             for b in children if b.get("type") == "child_page"}
print("Found pages:", list(pages_map.keys()))

people_id = pages_map.get("People to Follow")
blocks = get_children(people_id)

# ── 1. ADD RAPHAEL TO TECH TABLE ──────────────────────────────────────────────
print("\nAdding Raphael to Tech table...")

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

if tech_table_id:
    api("PATCH", f"/blocks/{tech_table_id}/children", {"children": [
        table_row([
            cell("Raphael Oliveira-Neves", "https://www.linkedin.com/in/raphael-oliveira-neves/"),
            cell("LinkedIn"),
            cell("Director of Engineering at Zendesk. Certified Career & Leadership Coach. GDG London volunteer coach. Helps tech professionals with career development, CV refinement, and interview preparation."),
        ])
    ]})
    time.sleep(0.3)
    print("  ✓ Raphael added to Tech table")

# ── 2. ADD COACHES & COMMUNITY RESOURCES SECTION ─────────────────────────────
print("\nAdding Coaches & Community Resources section...")

append(people_id, [
    divider(),
    h2("Coaches & Community Resources"),
    callout("These are people you can reach out to directly — for resume review, 1:1 sessions, or structured guidance. Different from content creators: these people actively help.", "🤝"),
    table_with_links([
        ["Person", "What they offer", "Resource"],
        ["Debra Shaw", "Career coach specifically for new college grads. Focuses on getting first-time job seekers noticed and hired. Has a free job strategy guide.", "Free guide at stan.store/gradshired"],
        ["Seppo Helava", "Resume mentor and author. 20+ years in tech. Offers 1:1 resume guidance. Most useful if you have an existing resume that isn't working.", "Free resume guide (link below)"],
        ["Raphael Oliveira-Neves", "Director of Engineering at Zendesk. Certified Career & Leadership Coach. GDG London volunteer coach.", "LinkedIn — reach out directly"],
        ["Amrutha S", "Offers resume review help.", "LinkedIn — reach out directly"],
        ["Suresh Choudhary", "1:1 sessions via Topmate — career guidance and job search support.", "topmate.io/mrsureshchoudhary"],
    ], urls={
        "Debra Shaw": "https://www.linkedin.com/in/gradshired/",
        "Seppo Helava": "https://www.linkedin.com/in/helava/",
        "Raphael Oliveira-Neves": "https://www.linkedin.com/in/raphael-oliveira-neves/",
        "Amrutha S": "https://www.linkedin.com/in/amrutha-s-b68ba1100/",
        "Suresh Choudhary": "https://www.linkedin.com/in/mrsureshchoudhary/",
    }),
    para(""),
    bullet([rt("Debra Shaw free guide: "),
            {"type": "text", "text": {"content": "stan.store/gradshired/p/free-guide-get-yourself-hired",
                                      "link": {"url": "https://stan.store/gradshired/p/free-guide-get-yourself-hired"}}}]),
    bullet([rt("Seppo Helava free resume guide: "),
            {"type": "text", "text": {"content": "docs.google.com/document/d/1kYgQ9Z09hHu29-3C4e3MF8inIcqZk5qOgwEIf2G8bHQ",
                                      "link": {"url": "https://docs.google.com/document/d/1kYgQ9Z09hHu29-3C4e3MF8inIcqZk5qOgwEIf2G8bHQ/edit"}}}]),
    bullet([rt("Suresh Choudhary Topmate: "),
            {"type": "text", "text": {"content": "topmate.io/mrsureshchoudhary",
                                      "link": {"url": "https://topmate.io/mrsureshchoudhary"}}}]),
])
print("  ✓ Coaches & Community Resources section added")

print("\n✓ Done.")
