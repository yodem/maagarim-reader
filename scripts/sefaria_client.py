"""Thin Sefaria HTTP client (same endpoints as sefaria-mcp).

Sefaria MCP is not always wired into Cursor; this module calls the public API
directly the same way `sefaria_mcp.logic` does.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_BASE = "https://www.sefaria.org"
USER_AGENT = "maagarim-reader-nikud/1.0 (+https://github.com/yodem/maagarim-reader)"

# Hebrew Tanakh edition with nikud and without te'amim (v1 `vhe=`).
NIKKUD_VERSION = "Tanach with Nikkud"


class SefariaError(RuntimeError):
    pass


def _request(
    method: str,
    url: str,
    *,
    data: bytes | None = None,
    timeout: float = 60.0,
) -> tuple[int, Any]:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            code = resp.getcode()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        code = e.code
        if code not in (202,):
            raise SefariaError(f"HTTP {code} for {url}: {body[:400]}") from e
    if not body.strip():
        return code, None
    try:
        return code, json.loads(body)
    except json.JSONDecodeError as e:
        raise SefariaError(f"Non-JSON from {url}: {body[:200]}") from e


def get_text_nikud(
    tref: str,
    *,
    base: str = DEFAULT_BASE,
    version: str = NIKKUD_VERSION,
) -> str:
    """Fetch Hebrew verse with nikud, no te'amim.

    Uses v1 `vhe=` — the reliable selector for "Tanach with Nikkud".
    Falls back to v3 `version=source` + caller should strip te'amim.
    """
    # Prefer dotted URL form: Genesis.1.1
    ref = tref.replace(" ", ".")
    q = urllib.parse.urlencode(
        {"lang": "he", "vhe": version, "context": "0"},
        quote_via=urllib.parse.quote,
    )
    url = f"{base.rstrip('/')}/api/texts/{urllib.parse.quote(ref)}?{q}"
    _, data = _request("GET", url)
    if not isinstance(data, dict):
        raise SefariaError(f"Unexpected texts payload for {tref}")
    he = data.get("he")
    if isinstance(he, list):
        he = " ".join(x for x in he if isinstance(x, str))
    if isinstance(he, str) and he.strip():
        return he

    # Fallback: Masorah source (usually with te'amim)
    url3 = (
        f"{base.rstrip('/')}/api/v3/texts/{urllib.parse.quote(ref)}"
        f"?version=source&return_format=text_only"
    )
    _, data3 = _request("GET", url3)
    versions = (data3 or {}).get("versions") or []
    if not versions:
        raise SefariaError(f"No Hebrew text for {tref}")
    text = versions[0].get("text")
    if isinstance(text, list):
        text = " ".join(x for x in text if isinstance(x, str))
    if not isinstance(text, str) or not text.strip():
        raise SefariaError(f"Empty Hebrew text for {tref}")
    return text


def find_refs(
    body: str,
    *,
    title: str = "",
    lang: str = "he",
    base: str = DEFAULT_BASE,
    poll_s: float = 0.4,
    timeout_s: float = 120.0,
) -> dict[str, Any]:
    """Async find-refs (linker v3), same as gdocs plugin / MCP-adjacent API."""
    payload = json.dumps(
        {"text": {"title": title, "body": body}, "lang": lang},
        ensure_ascii=False,
    ).encode("utf-8")
    url = f"{base.rstrip('/')}/api/find-refs"
    code, data = _request("POST", url, data=payload)
    if not isinstance(data, dict) or "task_id" not in data:
        raise SefariaError(f"find-refs did not return task_id: {data!r}")
    task_id = data["task_id"]
    deadline = time.time() + timeout_s
    delay = poll_s
    while time.time() < deadline:
        acode, a = _request("GET", f"{base.rstrip('/')}/api/async/{task_id}")
        if not isinstance(a, dict):
            time.sleep(delay)
            delay = min(delay * 1.5, 2.0)
            continue
        state = a.get("state")
        if a.get("ready") or state == "SUCCESS":
            return a.get("result") or {}
        if state == "FAILURE":
            raise SefariaError(f"find-refs failed: {a}")
        time.sleep(delay)
        delay = min(delay * 1.5, 2.0)
    raise SefariaError(f"find-refs timed out after {timeout_s}s (task {task_id})")


def _is_tanakh_ref(tref: str, meta: dict[str, Any]) -> bool:
    cat = meta.get("primaryCategory")
    if cat == "Tanakh":
        return True
    if cat and cat != "Tanakh":
        return False
    book = tref.split()[0] if tref else ""
    # Multi-word books: "I Samuel", "Song of Songs", …
    for name in _TANAKH_BOOKS_EN:
        if tref == name or tref.startswith(name + " "):
            return True
    return book in _TANAKH_BOOKS_EN


def tanakh_refs_from_find_result(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten successful Tanakh hits from find-refs result."""
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int]] = set()
    for section in ("title", "body"):
        block = result.get(section) or {}
        ref_data = block.get("refData") or {}
        for hit in block.get("results") or []:
            if hit.get("linkFailed"):
                continue
            refs = hit.get("refs") or []
            if not refs:
                continue
            tref = refs[0]
            meta = ref_data.get(tref) or {}
            if not _is_tanakh_ref(tref, meta):
                continue
            key = (tref, int(hit["startChar"]), int(hit["endChar"]))
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "ref": tref,
                    "url": meta.get("url") or tref.replace(" ", "."),
                    "heRef": meta.get("heRef"),
                    "startChar": int(hit["startChar"]),
                    "endChar": int(hit["endChar"]),
                    "text": hit.get("text") or "",
                    "section": section,
                }
            )
    return out


# English book titles for fallback when primaryCategory is missing.
_TANAKH_BOOKS_EN = frozenset(
    {
        "Genesis",
        "Exodus",
        "Leviticus",
        "Numbers",
        "Deuteronomy",
        "Joshua",
        "Judges",
        "I Samuel",
        "II Samuel",
        "I Kings",
        "II Kings",
        "Isaiah",
        "Jeremiah",
        "Ezekiel",
        "Hosea",
        "Joel",
        "Amos",
        "Obadiah",
        "Jonah",
        "Micah",
        "Nahum",
        "Habakkuk",
        "Zephaniah",
        "Haggai",
        "Zechariah",
        "Malachi",
        "Psalms",
        "Proverbs",
        "Job",
        "Song of Songs",
        "Ruth",
        "Lamentations",
        "Ecclesiastes",
        "Esther",
        "Daniel",
        "Ezra",
        "Nehemiah",
        "I Chronicles",
        "II Chronicles",
    }
)
