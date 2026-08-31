"""Pull each remaining Extended Library CM lesson from sabercraft.org into a
compact JSON file, so the cloud migration routine (which has no web egress)
can work from committed files instead of the network.

Two kinds of Ninja Table appear on these lessons:
  nt_type_ajax_table   - the <table> ships empty; rows come from admin-ajax.php
  nt_type_legacy_table - the rows are already rendered inline in the page HTML
Both are handled, and the AJAX path falls back to the inline parse when the
endpoint answers with an empty payload.
"""
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)


def fetch(url, tries=3):
    for attempt in range(tries):
        r = subprocess.run(["curl", "-sL", "--max-time", "45", "-A", "Mozilla/5.0", url],
                           capture_output=True)
        body = r.stdout.decode("utf-8", "replace")
        if r.returncode == 0 and len(body) > 500:
            return body
        time.sleep(2 * (attempt + 1))
    return body


def strip_tags(fragment):
    fragment = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", fragment)
    fragment = re.sub(r"(?i)<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"(?i)</p>", "\n\n", fragment)
    text = html.unescape(re.sub(r"(?s)<[^>]+>", "", fragment)).replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def video_id(page):
    for pat in (r"youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{8,})",
                r"youtu\.be/([A-Za-z0-9_-]{8,})",
                r"youtube\.com/watch\?v=([A-Za-z0-9_-]{8,})",
                r"ytimg\.com/vi/([A-Za-z0-9_-]{8,})"):
        m = re.search(pat, page)
        if m:
            return m.group(1)
    return None


LOGIN_WALL = "haven't logged in yet"


def body_text(page):
    """Everything inside the post body, tags stripped. Some lessons put their
    notation in running text rather than in a table, so nothing is discarded."""
    m = re.search(r'(?s)<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*?)(?:<footer|</article)', page)
    return strip_tags(m.group(1)) if m else ""


def prose(page):
    body = page
    m = re.search(r'(?s)<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*)', page)
    if m:
        body = m.group(1)
    body = body.split("footable_parent")[0]
    out = []
    for p in re.findall(r"(?s)<p[^>]*>(.*?)</p>", body):
        t = strip_tags(p)
        if len(t) > 25 and "cookie" not in t.lower():
            out.append(t)
    return out


def inline_rows(chunk):
    """Rows already rendered in the page HTML."""
    head = [strip_tags(c) for c in re.findall(r"(?s)<th[^>]*>(.*?)</th>", chunk)]
    rows = []
    for tr in re.findall(r"(?s)<tr[^>]*>(.*?)</tr>", chunk):
        if "<th" in tr:
            continue
        cells = [strip_tags(c) for c in re.findall(r"(?s)<td[^>]*>(.*?)</td>", tr)]
        if any(c for c in cells):
            rows.append(cells)
    return {"header": head, "rows": rows} if rows else None


def ajax_rows(tid):
    url = ("https://sabercraft.org/wp-admin/admin-ajax.php"
           "?action=wp_ajax_ninja_tables_public_action"
           f"&table_id={tid}&target_action=get-all-data")
    try:
        data = json.loads(fetch(url).strip())
    except json.JSONDecodeError:
        return None
    if not isinstance(data, list) or not data:
        return None
    rows = []
    for r in data:
        if not isinstance(r, dict):
            continue
        v = dict(r.get("value", {}))
        v.pop("___id___", None)
        v.pop("order", None)
        rows.append({k: val for k, val in v.items() if str(val).strip() != ""})
    return rows or None


def tables(page):
    out = []
    for m in re.finditer(r'(?s)<div id="footable_parent_(\d+)"(.*?)(?=<div id="footable_parent_|</article|\Z)', page):
        tid, chunk = m.group(1), m.group(2)
        cap = re.search(r'(?s)class="table_description[^"]*">(.*?)</div>\s*(?:<table|$)', chunk)
        label = re.search(r'aria-label="([^"]*)"', chunk)
        legacy = "nt_type_legacy_table" in chunk
        rec = {
            "table_id": tid,
            "aria_label": html.unescape(label.group(1)) if label else "",
            "caption": strip_tags(cap.group(1)) if cap else "",
            "kind": "legacy_inline" if legacy else "ajax",
        }
        got = inline_rows(chunk) if legacy else ajax_rows(tid)
        if got is None and not legacy:
            got = inline_rows(chunk)
            if got:
                rec["kind"] = "ajax_empty_used_inline"
        rec["data"] = got
        out.append(rec)
    return out


EXTENDED = Path(__file__).resolve().parent.parent / "docs" / "core" / "extended-library.md"
ROW = re.compile(r"\*\*(CM-[A-Z])\*\* \| ([^|]*) \| \[Video lesson\]\(([^)]*)\)")
rows_in = [(m.group(1), m.group(2).strip(), m.group(3))
           for m in ROW.finditer(EXTENDED.read_text(encoding="utf-8"))]
only = set(a.upper() for a in sys.argv[1:])

report = []
for letter, focus, url in rows_in:
    if only and letter.upper() not in only:
        continue
    page = fetch(url)
    tbls = tables(page)
    rec = {
        "cm": letter,
        "focus": focus,
        "source_url": url,
        "page_title": strip_tags(re.search(r"(?s)<title>(.*?)</title>", page).group(1)),
        "youtube_id": video_id(page),
        "prose": prose(page),
        "body_text": body_text(page),
        "tables": tbls,
    }
    warn = []
    if LOGIN_WALL in page:
        rec["access"] = "login_required"
        warn.append("PAGE IS BEHIND A MEMBER LOGIN - no source material available")
    if not rec["youtube_id"]:
        warn.append("no video on page")
    if not rec["prose"]:
        warn.append("no intro prose found")
    if not tbls:
        warn.append("no notation table on page")
    elif any(t["data"] is None for t in tbls):
        warn.append("a table returned no rows")
    rec["warnings"] = warn
    (OUT / f"{letter.lower()}.json").write_text(
        json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    n = sum(len(t["data"]["rows"]) if isinstance(t["data"], dict) else len(t["data"] or [])
            for t in tbls)
    report.append(f"{letter}: vid={rec['youtube_id'] or '-':12s} prose={len(rec['prose'])} "
                  f"tables={len(tbls)} rows={n} {'| ' + '; '.join(warn) if warn else 'OK'}")
    time.sleep(1)

print("\n".join(report))
