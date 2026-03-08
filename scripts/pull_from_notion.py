#!/usr/bin/env python3
"""
Pull Notion pages → GitHub markdown files.
Use this to recover Notion as source of truth before setting up the sync.

Usage:
  python3 scripts/pull_from_notion.py            # pull all pages
  python3 scripts/pull_from_notion.py job-boards  # pull one page (partial title match)
"""
import json, urllib.request, urllib.error, os, sys, time

TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
PAGES_CONFIG = os.path.join(SCRIPT_DIR, "pages.json")


def api_get(path):
    url = f"https://api.notion.com/v1{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  API error {e.code}: {e.read().decode()[:200]}")
        return None


def get_all_children(block_id):
    """Fetch all child blocks recursively, expanding toggles and tables."""
    results = []
    cursor = None
    while True:
        path = f"/blocks/{block_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        data = api_get(path)
        if not data:
            break
        results.extend(data.get("results", []))
        if data.get("has_more"):
            cursor = data.get("next_cursor")
        else:
            break

    for block in results:
        if block.get("has_children") and block.get("type") != "child_page":
            block["_children"] = get_all_children(block["id"])
            time.sleep(0.1)

    return results


def rich_text_to_md(rich_text):
    """Convert Notion rich_text array to markdown string."""
    parts = []
    for rt in rich_text:
        text = rt.get("plain_text", "")
        ann = rt.get("annotations", {})
        href = rt.get("href")
        if ann.get("code"):
            text = f"`{text}`"
        if ann.get("bold"):
            text = f"**{text}**"
        if ann.get("italic"):
            text = f"*{text}*"
        if ann.get("strikethrough"):
            text = f"~~{text}~~"
        if href:
            text = f"[{text}]({href})"
        parts.append(text)
    return "".join(parts)


def is_nav_line(text):
    """Skip Notion navigation footer lines like '← Resume | Job Search Strategy →'."""
    return "←" in text or "→" in text


def blocks_to_markdown(blocks, list_indent=0):
    lines = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        btype = block.get("type", "")
        obj = block.get(btype, {})
        rt = obj.get("rich_text", [])
        text = rich_text_to_md(rt)
        children = block.get("_children", [])

        if is_nav_line(text):
            i += 1
            continue

        if btype == "heading_1":
            lines.append(f"# {text}")
            lines.append("")
        elif btype == "heading_2":
            lines.append(f"## {text}")
            lines.append("")
        elif btype == "heading_3":
            lines.append(f"### {text}")
            lines.append("")
        elif btype == "paragraph":
            if text:
                lines.append(text)
            lines.append("")
        elif btype == "bulleted_list_item":
            prefix = "  " * list_indent + "- "
            lines.append(f"{prefix}{text}")
            if children:
                lines.extend(blocks_to_markdown(children, list_indent + 1))
        elif btype == "numbered_list_item":
            prefix = "  " * list_indent + "1. "
            lines.append(f"{prefix}{text}")
            if children:
                lines.extend(blocks_to_markdown(children, list_indent + 1))
        elif btype == "to_do":
            checked = obj.get("checked", False)
            mark = "x" if checked else " "
            lines.append(f"- [{mark}] {text}")
        elif btype == "divider":
            lines.append("---")
            lines.append("")
        elif btype == "quote":
            lines.append(f"> {text}")
            lines.append("")
        elif btype == "callout":
            icon = obj.get("icon", {})
            emoji = icon.get("emoji", "") if isinstance(icon, dict) else ""
            prefix = f"{emoji} " if emoji else ""
            lines.append(f"> {prefix}{text}")
            lines.append("")
        elif btype == "code":
            lang = obj.get("language", "")
            if lang == "plain text":
                lang = ""
            lines.append(f"```{lang}")
            lines.append(text)
            lines.append("```")
            lines.append("")
        elif btype == "toggle":
            # Render as heading_3 + children
            lines.append(f"### {text}")
            lines.append("")
            if children:
                lines.extend(blocks_to_markdown(children, list_indent))
        elif btype == "table":
            if children:
                header_done = False
                for row_block in children:
                    if row_block.get("type") == "table_row":
                        cells = row_block.get("table_row", {}).get("cells", [])
                        cell_texts = [rich_text_to_md(cell) for cell in cells]
                        lines.append("| " + " | ".join(cell_texts) + " |")
                        if not header_done:
                            lines.append("|" + "|".join(["---"] * len(cells)) + "|")
                            header_done = True
            lines.append("")
        elif btype in ("table_row", "child_page", "embed", "link_preview", "image"):
            pass  # handled inside their parent or skipped
        else:
            # Unknown block — emit text if any
            if text:
                lines.append(text)
                lines.append("")

        i += 1

    return lines


def clean_markdown(lines):
    """Collapse multiple blank lines, strip trailing whitespace, ensure single trailing newline."""
    result = []
    prev_blank = False
    for line in lines:
        stripped = line.rstrip()
        if stripped == "":
            if not prev_blank:
                result.append("")
            prev_blank = True
        else:
            result.append(stripped)
            prev_blank = False

    # Strip leading/trailing blank lines
    while result and result[0] == "":
        result.pop(0)
    while result and result[-1] == "":
        result.pop()
    result.append("")  # single trailing newline
    return "\n".join(result)


def pull_page(notion_id, title, file_path):
    print(f"  {title}...")
    blocks = get_all_children(notion_id)
    lines = blocks_to_markdown(blocks)
    md = clean_markdown(lines)
    full_path = os.path.join(ROOT_DIR, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(md)
    print(f"    → {file_path} ({len(blocks)} blocks)")
    return md


def main():
    filter_arg = sys.argv[1].lower() if len(sys.argv) > 1 else None

    with open(PAGES_CONFIG) as f:
        config = json.load(f)

    pulled = 0
    for page in config["pages"]:
        if not page.get("file"):
            continue
        if filter_arg and filter_arg not in page["title"].lower():
            continue
        pull_page(page["notion_id"], page["title"], page["file"])
        time.sleep(0.3)
        pulled += 1

    print(f"\nDone — {pulled} page(s) pulled.")


if __name__ == "__main__":
    main()
