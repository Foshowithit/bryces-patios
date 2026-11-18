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
  * light unsharp after downscale - one pass, not three

**The negative is the phone frame**, always, except for one target: the hero's
2400px retina tier, which is the only width in the set that the source cannot
cover. `work/sr/<stem>-x4.png` holds a 4x Real-ESRGAN reconstruction of each
phone frame (tools/sr-upscale.py, local, no API) and is consulted only where the
target is wider than the photo. Everywhere else it was measured to *cost*
realism rather than add it: these sources are 1600px platform downloads, so four
times the pixels is invented, and at display size the invention reads as yellow
speckle in a stone joint and pastel marbling across a granite face. Downsampling
to a width the phone already covers cannot recover that as detail - it only
bakes the artefact in at a smaller size. Cropping specs in CROP are written in
*source* pixels and are scaled to the negative that is actually open, so one spec
serves both masters.

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

import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
BACKUP = IMG / "_orig"
SR = ROOT / "work" / "sr"          # 4x reconstructed negatives (see sr-upscale.py)


def _negative(stem: str) -> Path | None:
    """The best negative on disk for a stem: the 4x reconstruction if it exists.

    Falls back to None so the caller keeps its own pristine-copy logic; the SR
    master is never written to, so it needs no backup of its own.
    """
    p = SR / f"{stem}-x4.png"
    return p if p.exists() else None


# Wide images get a full frame at 1600 + a 900 variant; square/tall ones keep
# their own aspect and a 1200 + 900 pair.
WIDE = {
    "hero-finished", "patio-firepit-build", "patio-diagonal", "project-walkway",
    "project-dining", "steps-detail", "yard", "craft-edge", "craft-base",
    "about-site", "transform-before", "transform-after", "big-yard", "walkway",
}
TALL = {"stairs-landing"}

# Per-image grade offsets. Only where the negative needs it; everything else
# uses the base recipe so the set stays coherent.
TWEAK = {
    # dusk hero: already warm and already dark, needs no fade and no vignette
    # (the hero scrim does that job and a second vignette would band the sky).
    # The 1%/99.5% clip is not cosmetic on this frame: measured on the rendered
    # 1600px tier, it is what separates the shadowed stone risers at the right
    # edge from the lawn behind them without touching the dusk sky.
    "hero-finished": dict(level="1%,99.5%,0.99", sat=100, vig=0),
    # the firepit frame is the most cluttered and the flattest; push it a little
    # harder so it can sit next to the finished work without looking like a
    # different camera.
    "patio-firepit-build": dict(sat=84, contrast=1.06),
    # the four white-granite frames are high-key at capture (mean luma 160-176
    # against 108-125 for the rest of the set) and the base recipe holds them at
    # capture tone rather than pushing them, which is why they were the only
    # frames that still read as phone snapshots at card size. They need the
    # opposite of a lift: a few points down to sit with their neighbours, and
    # MORE local contrast than the hot branch's gentler 15, because the flat read
    # comes from missing contrast in the stone, not from the pixels.
    # Saturation runs 80-84 here instead of the base 94 for a measured reason:
    # the clarity pass is a large-radius local contrast, and on this stone it
    # multiplies the coloured specular fringes already in the source JPEG
    # (craft-edge: 380 -> 1015 per 10k bright pixels with spread > 70, i.e. the
    # joint between two stones went yellow-green at card size). Pulling chroma
    # down to 80 takes those frames to 0 per 10k and the stone stays warm -
    # a cut in colour noise, not in saturation of anything that was there.
    "craft-base": dict(bright=86, sat=84, clarity=26),
    # sunlit granite on a white cap: hold it a few points down or the stone reads
    # as paper at full width, which is the exact defect this recipe exists to fix
    "craft-edge": dict(bright=76, sat=80, clarity=26),
    "steps-detail": dict(bright=86, sat=82, clarity=24),
    # same white-granite family as the three above, sitting beside them in the
    # process triplet: it gets the same downward move so the row does not step
    # from grey stone straight into paper.
    "patio-diagonal": dict(bright=92, sat=84, clarity=24),
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


def _recipe(src: Path, width: int, tw: dict, wb: tuple[float, float]) -> list[str]:
    """Everything the recipe does to a frame, as an argv tail.

    Split out of grade() so the white-balance pass can render the *actual* recipe
    at thumbnail size and measure what it produces, instead of measuring the raw
    negative and guessing how the grade will move it. One builder, so a preview
    can never drift from the delivered file.
    """
    # A frame that is already close to white gets a gentler lift and a rolloff
    # instead of a push: lifting it further just turns stone into paper.
    hot = _high_key(src, tw)
    level = tw.get("level", "1.5%,99.8%,0.975" if hot else "2%,99.7%,0.995")
    contrast = tw.get("contrast", 1.0)
    sat = tw.get("sat", 98 if hot else 96)
    vig = tw.get("vig", 0)
    clarity = tw.get("clarity", 15 if hot else 22)
    curve = tw.get("curve", 2.0 if hot else 2.9)

    args: list[str] = ["magick", str(src), "-colorspace", "sRGB"]
    if tw.get("crop"):
        args += ["-crop", _crop_for(src, tw["crop"]), "+repage"]
    if width:
        args += ["-filter", "Lanczos", "-resize", f"{width}x{width}>"]
    args += ["-sigmoidal-contrast", f"{curve},52%"]
    if level:
        args += ["-level", level]
    args += [
        # Brightness is a plain multiply, NEVER -modulate's first argument. On
        # this ImageMagick build -modulate with brightness != 100 round-trips the
        # pixel through HSL, and for a near-neutral bright stone that round trip
        # invents hue: measured on craft-edge at the shipped crop, the recipe with
        # `-modulate 76,80` put 368 bright high-chroma pixels per 10k on the stone
        # (844 at 76,100 - the brightness alone), while `-evaluate multiply 0.76`
        # plus `-modulate 100,80` left it at 0.0. That is the yellow-green confetti
        # that made the stone look rendered, and it is why brightness is applied
        # here and saturation below.
        "-evaluate", "multiply", f"{tw.get('bright', 100 if hot else 101) / 100:.3f}",
        # stone stays warm, foliage gives up a little
        "-modulate", f"100,{sat},100",
        # 1.018/0.986 is the house warmth; wb is this frame's drift off the set,
        # measured by _wb_scale and clamped to 5%. Passed in rather than measured
        # here because the before/after pair shares one correction.
        "-channel", "R", "-evaluate", "multiply", f"{1.018 * wb[0]:.4f}",
        "-channel", "B", "-evaluate", "multiply", f"{0.986 * wb[1]:.4f}",
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

    return args


def grade(src: Path, dst: Path, width: int, tw: dict,
          wb: tuple[float, float] = (1.0, 1.0)) -> None:
    """One recipe, tuned for the site this photo lands on: a dark hero overlay and
    light gallery panels, so the file has to carry its own local contrast.

    Three moves, in this order: filmic S-curve about mid-grey, a large-radius
    unsharp local-contrast pass at a whisper (clarity - lifts stone texture and
    paver joints without the grey veil a brightness/contrast push gives), a colour
    settle that keeps stone warm and pulls the green back, then ONE small-radius
    unsharp to restore what the Lanczos downscale took.

    This replaced a recipe that sharpened three times (0x20 clarity at 0.55, then
    0.62/0.85, then 2.4/0.28) because sharpening was doing the work real detail
    should do. With a 4x reconstructed negative underneath, every one of those
    passes now reads as a halo: the stone gets outlined instead of textured, which
    is the "crunchy phone photo" look the old pipeline was trying to cure.
    """
    args = _recipe(src, width, tw, wb)
    args += [
        "-unsharp", "0x0.7+0.35+0.01",
        "-strip",
        "-interlace", "Plane",
        "-sampling-factor", "4:2:0",
        "-quality", "88",
        "-depth", "8",
        str(dst),
    ]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"grade failed for {src.name}: {r.stderr.strip()}")


def _crop_for(src: Path, spec: str) -> str:
    """CROP specs are written against the phone frame; rescale to this negative.

    A 4x master is the same picture at four times the pixels, so an 810x456+790+400
    crop of a 1600px frame is 3240x1824+3160+1600 of a 6400px one. Scaling here
    rather than writing a second table means a single composition decision can
    never drift between the two negatives.
    """
    box, *offs = spec.split("+")
    w, h = (int(x) for x in box.split("x"))
    x, y = (int(o) for o in offs)
    src_w = _jpeg_dims(src)[0]
    if not src_w:
        return spec
    base = _jpeg_dims(BACKUP / f"{src.stem.split('-x4')[0]}.jpg")[0]
    if not base or src_w == base:
        return spec
    f = src_w / base
    if abs(f - round(f)) > 1e-6:
        raise SystemExit(f"{src.name}: negative width {src_w} is not a whole "
                         f"multiple of the {base}px phone frame - crop would drift")
    f = int(round(f))
    return f"{w * f}x{h * f}+{x * f}+{y * f}"


# White balance is the one thing a fixed recipe cannot fix: the frames were shot
# over different weather, and a single R/B multiplier leaves a cool grey card next
# to a warm brown one. Measured on the shipped set, the grey-world gain of the
# stone drifts gR 0.967-1.037 / gB 0.961-1.037 (sd 0.019 / 0.022) - a 5% spread
# that reads as "two different cameras" once three cards sit side by side.
# So each frame is measured and nudged toward the set's own mean instead of being
# forced to neutral: the warm house look survives, only the drift goes.
WB_TARGET = (1.0148, 0.9853)      # set-mean gain, measured on the 16 frames rendered by this recipe
WB_LIMIT = 0.05                   # never move a frame more than 5%
PAIR = ("transform-before", "transform-after")   # transform pair: one treatment


def _wb_gains(src: Path, tw: dict) -> tuple[float, float]:
    """Grey-world gain of the low-saturation midtones in what the recipe produces.

    Measured on a 320px render of the *actual* recipe, not on the raw negative:
    the grade moves colour (a sigmoid, a saturation pull, the warm R/B touch), so
    a gain measured before it describes a different picture than the one that
    ships. One extra tiny render per stem buys a number that is the delivered
    frame's own.
    """
    args = _recipe(src, 320, tw, (1.0, 1.0))
    args += ["-colorspace", "sRGB", "-depth", "8", "ppm:-"]
    r = subprocess.run(args, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"{src.name}: wb render failed: {r.stderr.decode()[:200]}")
    # P6 header: magic, width, height, maxval. Whitespace inside pixel data can
    # be any byte of 0x09-0x0d/0x20, so find the fields and then consume exactly
    # one separator byte - splitting the whole buffer eats leading pixel bytes.
    buf, pos, fields = r.stdout, 2, []
    while len(fields) < 3:
        while pos < len(buf) and buf[pos:pos + 1].isspace():
            pos += 1
        begin = pos
        while pos < len(buf) and not buf[pos:pos + 1].isspace():
            pos += 1
        fields.append(buf[begin:pos])
    pos += 1
    w, h = int(fields[0]), int(fields[1])
    px = np.frombuffer(buf[pos:pos + w * h * 3], dtype=np.uint8)
    if px.size != w * h * 3:
        raise SystemExit(f"{src.name}: short PPM body ({px.size} of {w * h * 3})")
    px = px.reshape(h, w, 3).astype(np.float32) / 255
    mx, mn = px.max(2), px.min(2)
    L = px.mean(2)
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    m = (L > 0.35) & (L < 0.92) & (sat < 0.18)
    if m.sum() < 2000:                        # a frame with almost no neutral area
        m = (L > 0.30) & (L < 0.95)
    mean = px[m].mean(0)
    g = float(mean.mean()) or 1.0
    return float(mean[0] / g), float(mean[2] / g)


def _wb_scale(stem: str, src: Path, tw: dict, override: dict) -> tuple[float, float]:
    """Multipliers that move this frame onto WB_TARGET, clamped to WB_LIMIT."""
    gr, gb = override.get(stem) or _wb_gains(src, tw)
    out = []
    for got, want in ((gr, WB_TARGET[0]), (gb, WB_TARGET[1])):
        k = want / got if got else 1.0
        out.append(round(max(1 - WB_LIMIT, min(1 + WB_LIMIT, k)), 4))
    return out[0], out[1]


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

    # The transform pair is one comparison, so both frames get the mean of
    # their two corrections: applying two different ones would tilt the pair
    # toward whichever frame still had its own light.
    pair: dict[str, tuple[float, float]] = {}
    if all((BACKUP / f"{p}.jpg").exists() for p in PAIR):
        g = [_wb_gains(BACKUP / f"{p}.jpg", dict(TWEAK.get(p, {}))) for p in PAIR]
        pair = {p: (sum(x[0] for x in g) / 2, sum(x[1] for x in g) / 2) for p in PAIR}

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
        neg = _negative(stem)
        before = main_jpg.stat().st_size
        if stem in CROP:
            # The crop box IS the delivered width. It is always a cut *down*
            # from the phone frame (never an upscale), so it comes straight off
            # the pristine negative at 1:1 - see the note in the target loop for
            # why the 4x master is not used to supersample a crop.
            crop_w = int(CROP[stem].split("x")[0])
            targets = [(main_jpg, crop_w)]
            for w in (640,):
                targets.append((IMG / f"{stem}-{w}.jpg", w))
            for stale in IMG.glob(f"{stem}-900.jpg"):
                stale.unlink()
        else:
            # The main file stays at the width the markup already declares for it
            # (1600 for a wide frame, 1200 for a tall one). The hero's 2400 retina
            # tier is a *separate* file built below; letting the master be 2400
            # here would rewrite hero-finished.jpg to 2400x1350, change the
            # generated width/height and srcset, and leave the -2400 tier as a
            # duplicate of the base file.
            master = 1200 if stem in TALL else 1600
            targets = [(main_jpg, master)]
            for w in (900,) if stem != "hero-finished" else (2400, 1200, 900):
                p = IMG / f"{stem}-{w}.jpg"
                if p.exists():
                    targets.append((p, w))

        if check:
            print(f"would grade {stem}: {len(targets)} files")
            continue

        # The phone frame this stem was shot on is the only real negative. Every
        # variant is composed from it, never from another variant, so a graded
        # variant can never become the input of the next one.
        pristine = BACKUP / main_jpg.name
        region_w = int(CROP[stem].split("x")[0]) if stem in CROP else _jpeg_dims(pristine)[0]

        for path, width in targets:
            # The 4x reconstruction is a negative only for a target that needs
            # pixels the phone does not have, which in this set is exactly the
            # hero's 2400 retina tier. Fed a width the phone already covers it
            # can only add invention it then throws away: measured at display
            # size on craft-edge and craft-base, the supersampled crops carried
            # yellow speckle through the joints and pastel marbling across the
            # granite face - the "generated" tell this pipeline exists to
            # remove, sitting inside a photograph that is otherwise real. So
            # downsamples come off the phone frame (1:1 or better, sharpened
            # once) and only true upscales consult the master.
            b = (neg or pristine) if width > region_w else pristine
            grade(b, path, width, tw, _wb_scale(stem, pristine, tw, pair))
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
