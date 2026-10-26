#!/usr/bin/env python3
"""Retina tier for the site photographs.

The job photos top out at 1600-2000 px wide, and the hero is displayed at 100vw,
so a 1440 CSS px laptop at DPR 2 asks for ~2880 px and the browser stretches the
1600 px file. That stretch is the softness people see. This emits a <stem>-2400.jpg
for each photograph a page actually asks for at 2400w, so the browser can pick
real pixels instead of inventing them, and it does the sharpening here where the
filter is under our control (Lanczos + edge-aware unsharp) instead of leaving it
to the browser. The list is read from the markup, not assumed: a 2400 tier no
srcset names is ~1.3 MB of dead weight that still ships to the live site, and an
earlier run of this script built 26 MB of exactly that.

No geometry, colour or content changes: resize, sharpen, and a touch of film
grain that keeps the upscale from reading as plastic. Idempotent; -f rebuilds.
"""
import re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG = ROOT / "assets" / "img"
TARGET = 2400
QUALITY = "88"

def dims(p):
    out = subprocess.run(["magick", "identify", "-format", "%w %h", str(p)],
                         capture_output=True, text=True, check=True).stdout.split()
    return int(out[0]), int(out[1])

def build(src, dst, force=False):
    if dst.exists() and not force and dst.stat().st_mtime >= src.stat().st_mtime:
        return "skip"
    w, h = dims(src)
    if w >= TARGET:                      # already big enough: just re-encode sharper
        resize = []
    else:                                # upscale in linear-ish RGB, Lanczos only
        resize = ["-filter", "Lanczos", "-resize", f"{TARGET}x"]
    subprocess.run([
        "magick", str(src), "-colorspace", "RGB", *resize,
        "-unsharp", "0x1.15+0.55+0.015",
        "-define", "noise-type=Gaussian", "-attenuate", "0.11", "+noise", "Gaussian",
        "-colorspace", "sRGB", "-strip", "-sampling-factor", "4:2:0",
        "-quality", QUALITY, "-interlace", "Plane", str(dst),
    ], check=True)
    return "built"

def retina_stems() -> set[str]:
    """Stems the shipped markup asks for at 2400w - the only ones worth building."""
    stems = set()
    for page in ROOT.rglob("*.html"):
        if ".git" in page.parts:
            continue
        for hit in re.finditer(r"assets/img/([A-Za-z0-9._-]+?)-2400\.jpg", page.read_text(errors="ignore")):
            stems.add(hit.group(1))
    return stems


def main():
    force = "-f" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("-")]
    srcs = [IMG / f"{n}.jpg" for n in names] if names else sorted(
        IMG / f"{stem}.jpg" for stem in retina_stems()
        if (IMG / f"{stem}.jpg").exists())
    for src in srcs:
        dst = IMG / f"{src.stem}-2400.jpg"
        state = build(src, dst, force)
        w0, h0 = dims(src); w1, h1 = dims(dst)
        print(f"{state:5} {src.name:28} {w0}x{h0} -> {w1}x{h1}  {dst.stat().st_size//1024}KB")

if __name__ == "__main__":
    main()
