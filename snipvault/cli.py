#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from pathlib import Path

VAULT_DIR = Path("vault")


def ensure_vault():
    VAULT_DIR.mkdir(parents=True, exist_ok=True)


def now_ms():
    return int(time.time() * 1000)


def add_snippet(args):
    ensure_vault()
    content = args.content or sys.stdin.read()
    if not content.strip():
        print("No content provided", file=sys.stderr)
        return 1
    meta = {
        "id": now_ms(),
        "tags": args.tags.split(",") if args.tags else [],
        "lang": args.lang or guess_lang(content),
        "note": args.note or "",
    }
    data = {"meta": meta, "content": content}
    out = VAULT_DIR / f"{meta['id']}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(str(out))
    return 0


def guess_lang(content: str) -> str:
    head = content.strip().splitlines()[:3]
    header = "\n".join(head).lower()
    if "function " in header or "=>" in header:
        return "js"
    if "package " in header or "import (\"" in header:
        return "go"
    if "def " in header or header.startswith("# "):
        return "py"
    if header.startswith("<"):
        return "html"
    if header.startswith("SELECT ") or "CREATE TABLE" in header.upper():
        return "sql"
    return ""


def search_snippets(args):
    ensure_vault()
    q = (args.query or "").lower()
    hits = []
    for p in VAULT_DIR.glob("*.json"):
        try:
            obj = json.loads(p.read_text())
        except Exception:
            continue
        text = (obj.get("content") or "")
        note = (obj.get("meta", {}).get("note") or "")
        tags = obj.get("meta", {}).get("tags") or []
        hay = "\n".join([text, note, " ".join(tags)]).lower()
        if q in hay:
            hits.append({"path": str(p), "meta": obj.get("meta", {})})
    for h in sorted(hits, key=lambda x: x["meta"].get("id", 0), reverse=True):
        print(f"{h['path']} :: {h['meta']}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="snipvault")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a snippet")
    p_add.add_argument("content", nargs="?", help="snippet content (or stdin)")
    p_add.add_argument("--tags")
    p_add.add_argument("--lang")
    p_add.add_argument("--note")
    p_add.set_defaults(func=add_snippet)

    p_search = sub.add_parser("search", help="search snippets")
    p_search.add_argument("query", nargs="?")
    p_search.set_defaults(func=search_snippets)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
