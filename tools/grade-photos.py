#!/usr/bin/env python3
"""One grade for every photograph on the site.

Bryce shoots on a phone, in daylight, on a job that is still open. The frames are
honest but they read cheap: flat contrast, hard blue shadows, grass the colour of
a lawn-service flyer, and a different colour balance in every file. That is a
*grade* problem before it is a camera problem.

This applies a single deterministic treatment to every image so the set reads as
one portfolio:

  * blacks lifted to ~3% (film fade - stops the crushed, phone-y look)
  * highlights pulled to ~98% so white clapboard stops clipping
  * gentle sigmoidal contrast around mid-grey (depth without clipping)
  * a large-radius unsharp local-contrast pass, which is what makes stone and
    paver joints read at card size (see the note in grade() for why it is not
    the softlight blend it used to be)
  * greens -14 saturation, everything else -6 (grass is the cheapest colour here)
  * warm highlights / neutral shadows via a small red-up, blue-down curve
  * no vignette: -vignette sizes its sigma in pixels, so the same value that
    reads as a soft falloff on a 1600px frame crushes an 810px crop to mud
    (measured: mean 0.440 -> 0.319 at sigma 300, 0.440 -> 0.383 at 140 on an
    810x456 frame). The card scrims do that job in CSS instead.
  * light unsharp after downscale

Determinism matters: `transform-before/after` are a comparison pair, so the
recipe never adapts to image content (no -auto-level, no per-image exposure).
Same input -> same output, byte for byte.

Usage:
  python3 tools/grade-photos.py            # grade every asset in place
  python3 tools/grade-photos.py --check    # dry run, print what would change
Originals are copied to assets/img/_orig/ on first run and never overwritten.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
BACKUP = IMG / "_orig"

# Wide images get a full frame at 1600 + a 900 variant; square/tall ones keep
# their own aspect and a 1200 + 900 pair.
WIDE = {
    "hero-finished", "patio-firepit-build", "patio-herringbone", "project-walkway",
    "project-dining", "steps-detail", "yard", "craft-edge", "craft-base",
    "about-site", "transform-before", "transform-after", "big-yard", "walkway",
}
TALL = {"stone-arch", "stairs-landing"}

# Per-image grade offsets. Only where the negative needs it; everything else
# uses the base recipe so the set stays coherent.
TWEAK = {
    # dusk hero: already warm and already dark, needs no fade and no vignette
    # (the hero scrim does that job and a second vignette would band the sky).
    "hero-finished": dict(level=None, sat=100, vig=0),
    # the firepit frame is the most cluttered and the flattest; push it a little
    # harder so it can sit next to the finished work without looking like a
    # different camera.
    "patio-firepit-build": dict(sat=84, contrast=1.06),
    "craft-base": dict(sat=88),
    # sunlit granite on a white cap: hold it a few points down or the stone reads
    # as paper at full width, which is the exact defect this recipe exists to fix
    "craft-edge": dict(bright=89, sat=97),
    "steps-detail": dict(bright=93, sat=96),
    # before/after must be identical treatments or the comparison is a lie
    "transform-before": dict(),
    "transform-after": dict(),
}


# Frames that need recomposing before they ship. The camera was pointed at the
# whole job rather than at the work: a wheelbarrow and two of the crew sit at the
# left of the fire-pit frame, and the walkway was shot across a strip of bare
# subgrade with a shovel and a broom lying in it. Cropping to the finished half
# is a decision about composition, not an edit to what happened - every pixel
# that survives is Bryce's own photograph of that job.
CROP = {
    "patio-firepit-build": "810x456+790+400",   # fire pit + capped seat wall, crew out of frame
    "project-walkway": "980x551+620+30",        # walkway, raised course, planted bed
    "craft-edge": "1100x619+0+140",             # cap line, full fieldstone face, one riser at the right edge
    # the cap's lit top face fills the top third of the frame with one flat white
    # plane, which is the part that read as a cheap phone photo at card size. Cut
    # to the shadowed riser, the warm fieldstone and the joint under the cap: the
    # frame now has a real range from the moss to the stone instead of a white slab.
    "steps-detail": "1100x619+380+230",
}

# Full-bleed images whose source is taller than the 16:9 the page wants.
# (the masters are 3:2, so the shipped 16:9 already throws away a quarter of the
# frame; anything recomposed here is cut from the same negative.)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def grade(src: Path, dst: Path, width: int, tw: dict) -> None:
    """One recipe, tuned for the site this photo lands on: a dark hero overlay and
    light gallery panels, so the file has to carry its own local contrast.

    Four moves, in this order: filmic S-curve about mid-grey, a large-radius
    unsharp local-contrast pass (clarity - lifts stone texture and paver joints
    without the grey veil a plain brightness/contrast push gives), a colour
    settle that keeps stone warm and pulls the green back, then two sharpen
    radii, the wide one at a whisper to give the eye an edge to hold.
    """
    # A frame that is already close to white gets a gentler lift and a rolloff
    # instead of a push: lifting it further just turns stone into paper.
    hot = _high_key(src, tw)
    level = tw.get("level", "1.5%,99.8%,0.975" if hot else "2%,99.7%,0.995")
    contrast = tw.get("contrast", 1.0)
    sat = tw.get("sat", 96 if hot else 90)
    vig = tw.get("vig", 0)
    clarity = tw.get("clarity", 42 if hot else 55)
    curve = tw.get("curve", 2.3 if hot else 3.4)

    args: list[str] = ["magick", str(src), "-colorspace", "sRGB"]
    if tw.get("crop"):
        args += ["-crop", tw["crop"], "+repage"]
    if width:
        args += ["-resize", f"{width}x{width}>"]
    args += ["-sigmoidal-contrast", f"{curve},52%"]
    if level:
        args += ["-level", level]
    args += [
        # stone stays warm, foliage gives up a little
        "-modulate", f"{tw.get('bright', 100 if hot else 101)},{sat},100",
        "-channel", "R", "-evaluate", "multiply", "1.018",
        "-channel", "B", "-evaluate", "multiply", "0.986",
        "-channel", "RGB",
    ]
    if clarity:
        # Large-radius unsharp IS the local-contrast pass: same idea as a softlight
        # blend against a blurred copy, but it leaves the mid-tone where it was.
        # The softlight composite that used to sit here ignored compose:args on this
        # ImageMagick build (args=none/0.2/2/20/100 all measured byte-identical) and
        # ran at full strength on every frame: on craft-edge it lifted the mean
        # 0.694 -> 0.904 while dropping the spread 0.234 -> 0.207 - brighter and
        # flatter at once, which is exactly the washed phone-photo read this
        # pipeline exists to remove.
        args += ["-unsharp", f"0x20+{clarity / 100:.2f}+0.02"]
    if contrast != 1.0:
        args += ["-brightness-contrast", f"0x{int(round((contrast - 1) * 100))}"]
    if vig:
        args += ["-background", "black", "-vignette", f"0x{int(vig)}"]
    args += [
        "-unsharp", "0x0.62+0.85+0.008",
        "-unsharp", "0x2.4+0.28+0",
        "-strip",
        "-interlace", "Plane",
        "-sampling-factor", "4:2:0",
        "-quality", "86",
        "-depth", "8",
        str(dst),
    ]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"grade failed for {src.name}: {r.stderr.strip()}")


def _luma_stats(p: Path) -> tuple[float, float]:
    """mean luma and the fraction of pixels already at/above 90%, both 0..1.

    A granite cap in midday sun is already near white before any grading, so the
    recipe has to know that before it lifts a white point or it will simply clip
    the stone to paper. Measured on the master, not guessed. The fraction matters
    more than any percentile: every frame here has a bright sky or lit window, so
    a p99.5 test called nine of ten photos "high key" and flattened the hero too.
    """
    out = subprocess.run(
        ["magick", str(p), "-colorspace", "gray", "-depth", "8", "-format", "%c", "histogram:info:-"],
        capture_output=True, text=True)
    counts = [0] * 256
    for line in out.stdout.splitlines():
        # "   12345: ( 42, 42, 42) #2A2A2A gray(42)"
        if ":" not in line or "(" not in line:
            continue
        n = int(line.split(":")[0].strip())
        v = int(line.split("(")[1].split(",")[0])
        counts[v] += n
    total = sum(counts) or 1
    mean = sum(i * c for i, c in enumerate(counts)) / total / 255
    blown = sum(c for i, c in enumerate(counts) if i >= 230) / total
    return mean, blown


def _high_key(src: Path, tw: dict) -> bool:
    if "highkey" in tw:
        return bool(tw["highkey"])
    mean, blown = _luma_stats(src)
    return mean >= 0.60 or blown >= 0.09


def _jpeg_dims(p: Path) -> tuple[int, int]:
    out = subprocess.run(["magick", "identify", "-format", "%w %h", str(p)],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return 0, 0
    w, h = out.stdout.split()
    return int(w), int(h)


def _aspect(spec: str | None, stem: str) -> float:
    """Aspect of what the master is supposed to become: the crop if it has one."""
    if spec:
        box = spec.split("+")[0]
        w, h = (int(x) for x in box.split("x"))
        return w / h
    w, h = _jpeg_dims(BACKUP / f"{stem}.jpg")
    return w / h


OG = IMG / "og-cover.jpg"
OG_W, OG_H = 1200, 630          # Open Graph / iMessage / Slack card aspect
OG_Y_SHARE = 30 / 900           # top of the original hero crop, as a fraction


def og_cover() -> None:
    """Social card off the same graded hero, so a shared link matches the site.

    Taken from the native graded master, not the 2400 retina tier: that tier
    carries an upscale, an unsharp pass and grain, and downscaling its grain by
    two reads as speckle in foliage on a card that is never displayed above
    1200 px. The retina file is only a fallback for a master narrower than the
    card, since upscaling the card is the one direction that always shows.
    """
    src = IMG / "hero-finished.jpg"
    if not src.exists() or _jpeg_dims(src)[0] < OG_W:
        src = IMG / "hero-finished-2400.jpg"
    w, h = _jpeg_dims(src)
    ch = min(round(w * OG_H / OG_W), h)   # keep full width, trim height
    y = round(h * OG_Y_SHARE)
    y = max(0, min(y, h - ch))
    subprocess.run([
        "magick", str(src), "-crop", f"{w}x{ch}+0+{y}", "+repage",
        "-filter", "Lanczos", "-resize", f"{OG_W}x{OG_H}!",
        "-colorspace", "sRGB", "-strip", "-sampling-factor", "4:2:0",
        "-quality", "82", "-interlace", "Plane", str(OG),
    ], check=True)
    print(f"og-cover {w}x{h} -> {OG_W}x{OG_H} from {src.name}  "
          f"{OG.stat().st_size//1024}KB")


def main(argv: list[str]) -> int:
    check = "--check" in argv
    BACKUP.mkdir(exist_ok=True)
    done: list[tuple[str, int, int]] = []

    only = None
    for a in argv:
        if a.startswith("--only="):
            only = {x.strip() for x in a.split("=", 1)[1].split(",") if x.strip()}

    for stem in sorted(WIDE | TALL):
        if only and stem not in only:
            continue
        tw = dict(TWEAK.get(stem, {}))
        if stem in CROP:
            tw["crop"] = CROP[stem]
        main_jpg = IMG / f"{stem}.jpg"
        if not main_jpg.exists():
            print(f"skip {stem}: missing", file=sys.stderr)
            continue
        src = main_jpg
        backup = BACKUP / main_jpg.name
        if not backup.exists():
            shutil.copy2(src, backup)
        else:
            # always grade from the pristine copy, never from a graded file
            src = backup

        master_aspect = _aspect(CROP.get(stem), stem)
        before = main_jpg.stat().st_size
        if stem in CROP:
            # native width, plus a small variant for phones; no upscale
            targets = [(main_jpg, 0)]
            for w in (640,):
                targets.append((IMG / f"{stem}-{w}.jpg", w))
            for stale in IMG.glob(f"{stem}-900.jpg"):
                stale.unlink()
        else:
            master = 2400 if stem == "hero-finished" else (1200 if stem in TALL else 1600)
            targets = [(main_jpg, master)]
            for w in (900,) if stem != "hero-finished" else (2400, 1200, 900):
                p = IMG / f"{stem}-{w}.jpg"
                if p.exists():
                    targets.append((p, w))

        if check:
            print(f"would grade {stem}: {len(targets)} files")
            continue

        for path, width in targets:
            if stem in CROP:
                # every size comes off the same pristine negative and gets the
                # same crop; a variant's own file is already composed
                b = BACKUP / main_jpg.name
            else:
                b = BACKUP / path.name
                if not b.exists():
                    if not path.exists():
                        b = BACKUP / main_jpg.name
                    else:
                        shutil.copy2(path, b)
            grade(b, path, width, tw)
            w, h = _jpeg_dims(path)
            if w < 2 or h < 2 or abs((w / h) - master_aspect) > 0.01 * master_aspect:
                raise SystemExit(
                    f"{path.name}: graded to {w}x{h}, expected the master's "
                    f"aspect {master_aspect:.3f} - the recipe composed it twice")
        after = main_jpg.stat().st_size
        done.append((stem, before, after))

    if not check:
        og_cover()
        tb = sum(b for _, b, _ in done)
        ta = sum(a for _, _, a in done)
        print(f"{len(done)} photographs graded, {len(list(IMG.glob('*.jpg')))} jpgs on disk")
        print(f"main files {tb/1e6:.2f} MB -> {ta/1e6:.2f} MB")
        for stem, b, a in done:
            print(f"  {stem:22s} {b:8,} -> {a:8,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
