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

def rt(content, bold=False):
    t = {"type": "text", "text": {"content": content}}
    if bold:
        t["annotations"] = {"bold": True}
    return t

def h2(content):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [rt(content)]}}

def h3(content):
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [rt(content)]}}

def para(parts):
    if isinstance(parts, str):
        parts = [rt(parts)]
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": parts}}

def bullet(parts):
    if isinstance(parts, str):
        parts = [rt(parts)]
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": parts}}

def callout(content, emoji="💡"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [rt(content)], "icon": {"type": "emoji", "emoji": emoji}}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def toggle(title, children):
    return {"object": "block", "type": "toggle",
            "toggle": {"rich_text": [rt(title)], "children": children}}

def table(rows):
    return {
        "object": "block", "type": "table",
        "table": {
            "table_width": len(rows[0]),
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                {"object": "block", "type": "table_row",
                 "table_row": {"cells": [[{"type": "text", "text": {"content": cell}}] for cell in row]}}
                for row in rows
            ]
        }
    }

# Find Interview Prep page
children = get_children(PARENT_ID)
interview_id = next((b["id"] for b in children
    if b.get("type") == "child_page" and "Interview Prep" in b.get("child_page", {}).get("title", "")), None)

print(f"Interview Prep page: {interview_id}")

blocks = get_children(interview_id)

# Find the STAR heading/section — insert frameworks section after it
# We'll insert after the behavioral interviews table (the "Common questions" table)
# Strategy: find the table block inside the behavioral section, insert after it
star_section_last_block_id = None
in_behavioral = False

for block in blocks:
    btype = block.get("type", "")
    if btype == "heading_2":
        texts = block.get("heading_2", {}).get("rich_text", [])
        heading_text = "".join(t.get("text", {}).get("content", "") for t in texts)
        if "Behavioral" in heading_text:
            in_behavioral = True
        elif in_behavioral:
            in_behavioral = False
    elif in_behavioral:
        star_section_last_block_id = block["id"]

print(f"Last block in behavioral section: {star_section_last_block_id}")

frameworks_blocks = [
    divider(),
    h2("Beyond STAR — other frameworks worth knowing"),
    callout("STAR works for 90% of behavioral questions. These frameworks are worth knowing for specific situations.", "💡"),
    table([
        ["Framework", "Stands for", "When to use it"],
        ["STAR", "Situation, Task, Action, Result", "Default — most behavioral questions"],
        ["STARR", "Situation, Task, Action, Result, Reflection", "When growth mindset matters — add what you learned and would do differently"],
        ["SOAR", "Situation, Obstacle, Action, Result", "When the difficulty is the point — turnarounds, hard deadlines, conflict"],
        ["CAR", "Context, Action, Result", "Concise answers where the context is simple — keeps you from over-explaining setup"],
        ["PARADE", "Problem, Anticipated outcome, Role, Action, Decision, End result", "Consulting interviews — McKinsey, BCG. Forces you to show judgment vs. what you expected"],
        ["DIGS", "Dilemma, Insight, Growth, Success", "Failure and weakness questions — STAR produces flat answers here, DIGS forces reflection"],
    ]),
    para(""),
    h3("How to pick the right one"),
    bullet([rt("Default to "), rt("STAR", bold=True), rt(" — it's what interviewers are trained to evaluate against")]),
    bullet([rt("Use "), rt("SOAR", bold=True), rt(" when the obstacle or conflict is central to the story")]),
    bullet([rt("Use "), rt("PARADE", bold=True), rt(" if interviewing at a consulting firm — it signals you understand their evaluation style")]),
    bullet([rt("Use "), rt("DIGS", bold=True), rt(" for 'tell me about a failure' or 'what's your biggest weakness' — STAR makes these feel like you're avoiding the question")]),
    bullet([rt("Use "), rt("STARR", bold=True), rt(" when you want to show self-awareness and growth — good for culture-fit focused companies")]),
    para(""),
    callout("The framework matters less than the story. Pick the one that makes your answer clearest — don't force a story into a framework that doesn't fit.", "💡"),
]

result = api("PATCH", f"/blocks/{interview_id}/children", {
    "children": frameworks_blocks,
    "after": star_section_last_block_id,
})

if result:
    print("✓ Frameworks section added to Interview Prep")
else:
    print("✗ Failed")
