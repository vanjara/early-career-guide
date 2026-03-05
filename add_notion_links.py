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

# All URLs mapped to their display text (exact match on first cell of table rows)
URL_MAP = {
    # Resume templates
    "Jake's Resume (Overleaf/LaTeX)": "https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs",
    "Google Docs resume templates": "https://docs.google.com/templates",
    "Harvard OCS templates": "https://ocs.fas.harvard.edu/resumes-cvs",

    # Job boards — new grad
    "Handshake": "https://joinhandshake.com",
    "RippleMatch": "https://ripplematch.com",
    "WayUp": "https://www.wayup.com",
    "Simplify.jobs": "https://simplify.jobs",
    "Parker Dewey": "https://www.parkerdewey.com",

    # Job boards — tech
    "Wellfound (AngelList)": "https://wellfound.com",
    "Levels.fyi": "https://www.levels.fyi",
    "Y Combinator job board": "https://www.ycombinator.com/jobs",
    "Dice": "https://www.dice.com",
    "Kaggle Jobs": "https://www.kaggle.com/jobs",
    "Built In": "https://builtin.com",

    # Job boards — finance
    "eFinancialCareers": "https://www.efinancialcareers.com",
    "Wall Street Oasis": "https://www.wallstreetoasis.com",
    "Wall Street Oasis job board": "https://www.wallstreetoasis.com/jobs",
    "Mergers & Inquisitions": "https://mergersandinquisitions.com",
    "Vault": "https://www.vault.com",
    "Glassdoor": "https://www.glassdoor.com",

    # Job boards — visa
    "myvisajobs.com": "https://www.myvisajobs.com",
    "H1Bdata.info": "https://h1bdata.info",
    "Immigrationhelp.org": "https://www.immigrationhelp.org",

    # Interview prep
    "Neetcode.io": "https://neetcode.io",
    "LeetCode": "https://leetcode.com",
    "interviewing.io": "https://interviewing.io",
    "DataLemur": "https://datalemur.com",
    "StrataScratch": "https://www.stratascratch.com",
    "Wall Street Prep": "https://www.wallstreetprep.com",
    "Breaking Into Wall Street": "https://breakingintowallstreet.com",
    "IGotAnOffer": "https://igotanoffer.com",
    "MConsultingPrep": "https://mconsultingprep.com",

    # Offer & negotiation
    "LinkedIn Salary": "https://www.linkedin.com/salary",
    "Blind": "https://www.teamblind.com",
    "Payscale": "https://www.payscale.com",

    # Visa/OPT resources
    "USCIS.gov": "https://www.uscis.gov",
    "Murthy Law Firm (murthy.com)": "https://www.murthy.com",
    "trackitt.com": "https://www.trackitt.com",
    "Immihelp forums": "https://www.immihelp.com",

    # Reddit
    "r/cscareerquestions": "https://www.reddit.com/r/cscareerquestions",
    "r/datascience": "https://www.reddit.com/r/datascience",
    "r/dataengineering": "https://www.reddit.com/r/dataengineering",
    "r/FinancialCareers": "https://www.reddit.com/r/FinancialCareers",
    "r/ibanking": "https://www.reddit.com/r/ibanking",
    "r/consulting": "https://www.reddit.com/r/consulting",
    "r/f1visa": "https://www.reddit.com/r/f1visa",
    "r/OPTjobs": "https://www.reddit.com/r/OPTjobs",
    "r/h1b": "https://www.reddit.com/r/h1b",

    # Newsletters / people
    "The Pragmatic Engineer": "https://newsletter.pragmaticengineer.com",
    "Levels.fyi newsletter": "https://www.levels.fyi/newsletter",
    "WSO Daily": "https://www.wallstreetoasis.com/newsletter",
    "Mergers & Inquisitions newsletter": "https://mergersandinquisitions.com/newsletter",
    "Dear Sophie": "https://www.alcorn.law/dear-sophie",
}

def api(method, path, data=None):
    url = f"https://api.notion.com/v1{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"    API Error {e.code}: {e.read().decode()[:200]}")
        return None

def get_children(block_id):
    result = api("GET", f"/blocks/{block_id}/children?page_size=100")
    if not result:
        return []
    blocks = result.get("results", [])
    # Handle pagination
    while result.get("has_more"):
        cursor = result.get("next_cursor")
        result = api("GET", f"/blocks/{block_id}/children?page_size=100&start_cursor={cursor}")
        if result:
            blocks.extend(result.get("results", []))
    return blocks

def make_link_cell(text, url):
    return [{"type": "text", "text": {"content": text, "link": {"url": url}}, "annotations": {"bold": False, "italic": False, "strikethrough": False, "underline": False, "code": False, "color": "default"}}]

def make_plain_cell(text):
    return [{"type": "text", "text": {"content": text}}]

def process_table_row(row_block):
    """Check table row cells and add links where applicable. Returns True if updated."""
    cells = row_block.get("table_row", {}).get("cells", [])
    if not cells:
        return False

    updated = False
    new_cells = []

    for i, cell in enumerate(cells):
        # Get plain text of cell
        cell_text = "".join(rt.get("text", {}).get("content", "") for rt in cell)

        if cell_text in URL_MAP and i == 0:  # Only linkify first column
            new_cells.append(make_link_cell(cell_text, URL_MAP[cell_text]))
            updated = True
        else:
            new_cells.append(cell if cell else [{"type": "text", "text": {"content": ""}}])

    if updated:
        result = api("PATCH", f"/blocks/{row_block['id']}", {
            "table_row": {"cells": new_cells}
        })
        time.sleep(0.3)  # Rate limit
        return result is not None
    return False

def process_page(page_id, page_title):
    print(f"\n  Processing: {page_title}")
    blocks = get_children(page_id)
    updates = 0

    for block in blocks:
        btype = block.get("type")

        if btype == "table":
            # Get table rows
            rows = get_children(block["id"])
            for row in rows:
                if row.get("type") == "table_row":
                    if process_table_row(row):
                        updates += 1

        elif btype == "toggle":
            # Process blocks inside toggles
            toggle_children = get_children(block["id"])
            for child in toggle_children:
                if child.get("type") == "table":
                    rows = get_children(child["id"])
                    for row in rows:
                        if row.get("type") == "table_row":
                            if process_table_row(row):
                                updates += 1

    print(f"    → {updates} cells updated with links")

# Get all child pages
print("Finding subpages...\n")
children = get_children(PARENT_ID)
subpages = [(b["id"], b.get("child_page", {}).get("title", "Unknown"))
            for b in children if b.get("type") == "child_page"]

print(f"Found {len(subpages)} pages:")
for pid, title in subpages:
    print(f"  - {title}")

print("\nAdding links...")
for page_id, title in subpages:
    process_page(page_id, title)

print("\n✓ Done — links added to all pages.")
