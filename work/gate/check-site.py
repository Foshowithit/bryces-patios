#!/usr/bin/env python3
"""Structural gate for the built site.

Reads the emitted HTML and fails on anything a machine can decide, so nobody has
to eyeball 85 pages or trust a memory of what was checked last time. Advisory
findings (title/description length) are printed but do not fail the run.

    python3 work/gate/check-site.py            # from the repo root
    python3 work/gate/check-site.py --verbose  # list every offending path

Exit 0 = PASS, 1 = FAIL (hard check), 2 = the tree is not built yet.
Run it after `python3 work/gen/emit.py`, before any deploy.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "work" / "gen"))

VERBOSE = "--verbose" in sys.argv

# Pages that are deliberately not like the others.
NOINDEX_EXEMPT = {"404.html"}   # noindex,follow by design; canonical is advisory
H1_EXEMPT: set[str] = set()


def die(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(2)


def show(items: list[str], limit: int = 12) -> str:
    if VERBOSE or len(items) <= limit:
        return ", ".join(items)
    return ", ".join(items[:limit]) + f", ... (+{len(items) - limit} more)"


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html")
                   if "work" not in p.relative_to(ROOT).parts
                   and "node_modules" not in p.parts)
    if not pages:
        die("no built pages found - run python3 work/gen/emit.py first")

    # work/gen/site.py is imported by path: the module is named `site`, which is a
    # stdlib module already in sys.modules, so a plain import returns the wrong one.
    import importlib.util
    try:
        spec = importlib.util.spec_from_file_location(
            "bryce_gen_site", ROOT / "work" / "gen" / "site.py")
        gen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen)
    except Exception as exc:  # pragma: no cover
        die(f"cannot import the generator's tables: {exc}")
    token = gen.V

    hard: dict[str, list[str]] = {
        "h1": [], "canonical": [], "json-ld": [], "assets": [],
        "img": [], "token": [], "no-js": [], "title": [],
    }
    n_ld = n_img = n_ref = 0
    title_over, desc_off = [], []

    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        html = p.read_text(encoding="utf-8")

        n = len(re.findall(r"<h1\b", html))
        if rel in H1_EXEMPT:
            pass
        elif n != 1:
            hard["h1"].append(f"{rel}({n})")

        if rel not in NOINDEX_EXEMPT and 'rel="canonical"' not in html:
            hard["canonical"].append(rel)

        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',
                             html, re.S):
            n_ld += 1
            try:
                json.loads(m.group(1))
            except json.JSONDecodeError as exc:
                hard["json-ld"].append(f"{rel}:{exc.lineno}")

        t = re.search(r"<title>(.*?)</title>", html, re.S)
        if not t or not t.group(1).strip():
            hard["title"].append(rel)
        else:
            plain = re.sub(r"&[a-z]+;|&#\d+;", "x", t.group(1))
            if len(plain) > 65:
                title_over.append(f"{rel}({len(plain)})")
        d = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        if not d or not (70 <= len(d.group(1)) <= 165):
            desc_off.append(f"{rel}({len(d.group(1)) if d else 0})")

        for m in re.finditer(r"<img\b[^>]*>", html):
            n_img += 1
            tag = m.group(0)
            if 'alt="' not in tag or 'width="' not in tag or 'height="' not in tag:
                hard["img"].append(f"{rel}:{tag[:60]}")

        htmltag = re.search(r"<html\b[^>]*>", html)
        if not htmltag or 'class="no-js"' not in htmltag.group(0):
            hard["no-js"].append(rel)
        elif "className.replace(\"no-js\",\"js\")" not in html:
            hard["no-js"].append(f"{rel}:flip-missing")
        elif html.index('className.replace("no-js","js")') > html.index('assets/css/style.css'):
            hard["no-js"].append(f"{rel}:flip-after-css")

        # every first-party ?v= must be the current asset hash
        for m in re.finditer(r"\?v=([0-9a-f]{8})", html):
            if m.group(1) != token:
                hard["token"].append(f"{rel}:{m.group(1)}")
                break

        # local href/src targets must exist on disk
        for m in re.finditer(r'(?:href|src)="(/(?!/)[^"#?]*)"', html):
            target = m.group(1)
            n_ref += 1
            f = ROOT / target.lstrip("/")
            if target.endswith("/"):
                f = f / "index.html"
            if not f.exists():
                hard["assets"].append(f"{rel}->{target}")

    fails = {k: v for k, v in hard.items() if v}
    total_hard = sum(len(v) for v in fails.values())

    print(f"[{'FAIL' if fails else 'PASS'}] {len(pages)} pages, "
          f"{total_hard} hard failure(s), token {token}")

    def line(name: str, ok: str, bad: list[str]) -> None:
        if bad:
            print(f"  [FAIL] {name}: {len(bad)} - {show(bad)}")
        else:
            print(f"  [ok]   {name}: {ok}")

    line("one <h1> per page", f"{len(pages)}/{len(pages)}", hard["h1"])
    line("canonical", f"{len(pages)}/{len(pages)}", hard["canonical"])
    line("JSON-LD parses", f"{n_ld} blocks", hard["json-ld"])
    line("local asset/link targets", f"{n_ref} refs resolve", hard["assets"])
    line("<img> alt + width + height", f"{n_img} images", hard["img"])
    line("cache-buster current", f"{token} on every page", hard["token"])
    line("no-js reveal gate", "markup + inline flip before the sheet", hard["no-js"])
    line("<title> present", f"{len(pages)}/{len(pages)}", hard["title"])

    # advisory only: a 65-char <title> gets truncated in a SERP, but it is not a
    # broken page, and a rewrite should be a decision rather than a build failure
    if title_over:
        print(f"  [note] titles over 65 chars: {len(title_over)} - {show(title_over, 8)}")
    if desc_off:
        print(f"  [note] descriptions outside 70-165: {len(desc_off)} - {show(desc_off, 8)}")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
