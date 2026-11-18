#!/usr/bin/env python3
"""AI remaster: rebuild real photographic detail on Bryce's phone photos.

The shipped set is soft because every frame is a ~900-1600 px phone photo pushed
to 1600-2400 px and then triple-sharpened by grade-photos.py. Sharpening cannot
invent detail; it only outlines what is there, which is what reads as crunchy.

This pass asks an image model to *restore* the negative - recover stone grain,
paver joints and foliage at print scale - under a prompt that forbids the model
from moving anything. Every candidate is then checked against the source with a
structural diff, because "looks better" and "is the same job" are two separate
claims and only the second one is negotiable with a client.

  python3 tools/ai-remaster.py hero-finished
  python3 tools/ai-remaster.py --all
  python3 tools/ai-remaster.py hero-finished --model google/gemini-3-pro-image

Transport is OpenRouter (the direct Gemini key is on a free tier whose image
quota is zero - measured 2026-10-26, both 3-pro and 3.1-flash answer 429
"limit: 0"). --transport gemini keeps the direct call for the day that changes.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
SRC = IMG / "_orig"
OUT = ROOT / "work" / "ai-remaster"
KEY = Path(os.path.expanduser("~/.agent-vault/keys/gemini.key"))
OR_KEY = Path(os.path.expanduser("~/.agent-vault/keys/openrouter.key"))
API = "https://generativelanguage.googleapis.com/v1beta/models"
OR_API = "https://openrouter.ai/api/v1/chat/completions"

PROMPT = (
    "Restore this photograph to full photographic quality. It is a real photo of a "
    "finished hardscape installation - a hand-laid stone patio, dry-stack stone wall, "
    "stone steps and planting, shot by the contractor on a phone.\n\n"
    "WHAT TO DO: recover true detail that the small sensor lost - individual stone "
    "faces and mortar-free joints, crisp paver edges and surface texture, honest leaf "
    "and grass detail, clean window and door frames. Correct the phone-camera flaws: "
    "mushy compression, soft focus, dull or green-cast colour, flat contrast, muddy "
    "shadows, clipped highlights. Return a natural premium architectural photograph: "
    "clean whites, believable shadows, accurate stone colour, subtle grain. High "
    "resolution, print sharpness, no visible upscaling.\n\n"
    "WHAT NOT TO DO - these are hard constraints: do not move, add, remove, resize or "
    "duplicate anything. The layout, paver pattern, stone courses, furniture positions, "
    "plant placement and quantities must stay pixel-for-pixel where they are. Keep the "
    "same camera angle, framing, crop and lens. Keep the sun direction and every shadow "
    "exactly where the source has them. No HDR look, no halos, no painterly or "
    "illustrated texture, no plastic smoothing, no vignette, no colour cast, no text or "
    "watermark.\n\n"
    "If a region is genuinely unrecoverable, leave it soft rather than inventing it."
)


def read_key(path: Path = KEY) -> str:
    k = path.read_text().strip()
    if len(k) < 20:
        raise SystemExit(f"error: {path} does not look like a key")
    return k


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def sniff(data: bytes) -> str:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return "bin"


def remaster_or(src: Path, dst: Path, model: str, size: str, key: str) -> dict:
    """OpenRouter chat-completions transport: image in, image out."""
    body = {
        "model": model,
        "modalities": ["image", "text"],
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": f"{PROMPT}\n\nOutput the restored frame at {size}."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{b64(src)}"}},
            ],
        }],
    }
    req = urllib.request.Request(
        OR_API,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{model} HTTP {e.code}: {e.read()[:400].decode(errors='replace')}")

    msg = payload.get("choices", [{}])[0].get("message", {})
    for img in msg.get("images") or []:
        url = (img.get("image_url") or {}).get("url", "")
        if url.startswith("data:"):
            data = base64.b64decode(url.split(",", 1)[1])
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            return {"format": sniff(data), "bytes": len(data),
                    "model": payload.get("model", model), "src": src.name}
    raise SystemExit(
        f"no image returned for {src.name}: "
        f"{(msg.get('content') or '')[:400] or json.dumps(payload)[:400]}")


def remaster(src: Path, dst: Path, model: str, size: str, key: str) -> dict:
    body = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": PROMPT},
                {"inline_data": {"mime_type": "image/jpeg", "data": b64(src)}},
            ],
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"imageSize": size},
        },
    }
    req = urllib.request.Request(
        f"{API}/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{model} HTTP {e.code}: {e.read()[:400].decode(errors='replace')}")

    parts = payload.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        inline = p.get("inlineData") or p.get("inline_data")
        if inline:
            data = base64.b64decode(inline["data"])
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            return {"format": sniff(data), "bytes": len(data),
                    "model": model, "src": src.name}
    text = " ".join(p.get("text", "") for p in parts)[:600]
    raise SystemExit(f"no image returned for {src.name}: {text or payload}")


def dims(p: Path) -> tuple[int, int]:
    out = subprocess.run(["magick", "identify", "-format", "%w %h", str(p)],
                         capture_output=True, text=True)
    w, h = out.stdout.split()
    return int(w), int(h)


def drift(src: Path, cand: Path) -> float:
    """How far the candidate moved the picture, 0 = identical. Structural, not
    perceptual: a candidate that quietly re-laid the pavers scores high even if it
    looks lovely, and that is the number worth printing."""
    out = subprocess.run([
        "magick", str(src), "-colorspace", "gray", "-resize", "800x800!",
        "(", str(cand), "-colorspace", "gray", "-resize", "800x800!", ")",
        "-compose", "difference", "-composite", "-format", "%[fx:mean*100]", "info:",
    ], capture_output=True, text=True)
    try:
        return round(float(out.stdout.strip()), 2)
    except ValueError:
        return -1.0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--model", default="google/gemini-3-pro-image")
    ap.add_argument("--size", default="4K")
    ap.add_argument("--transport", default="openrouter", choices=["openrouter", "gemini"])
    ap.add_argument("--suffix", default="")
    args = ap.parse_args(argv)

    names = args.names
    if args.all:
        names = sorted(p.stem for p in SRC.glob("*.jpg") if "-900" not in p.stem
                       and "-1200" not in p.stem and "-2400" not in p.stem
                       and "-640" not in p.stem and not p.stem.startswith("r"))
    if not names:
        ap.error("give at least one name, or --all")

    key = read_key(OR_KEY if args.transport == "openrouter" else KEY)
    run = remaster_or if args.transport == "openrouter" else remaster
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names:
        src = SRC / f"{name}.jpg"
        if not src.exists():
            print(f"MISS {name}")
            continue
        dst = OUT / f"{name}{args.suffix}.jpg"
        info = run(src, dst, args.model, args.size, key)
        sw, sh = dims(src)
        dw, dh = dims(dst)
        d = drift(src, dst)
        print(f"{name}: {sw}x{sh} -> {dw}x{dh}  {info['bytes']//1024}KB  "
              f"drift={d:.2f}%  {info['format']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
