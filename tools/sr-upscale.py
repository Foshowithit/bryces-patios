#!/usr/bin/env python3
"""Real super-resolution for Bryce's photo masters - local, no API, no invention
beyond what the model reconstructs.

The shipped images are soft because grade-photos.py pushes ~900-1600 px phone
photos to 1600-2400 px and then sharpens three times. Sharpening cannot create
detail; it outlines what is missing, which is the crunchy, painted read. This
pass puts real reconstructed detail into the pixels first (Real-ESRGAN x4plus,
tiled), then hands the result to a restrained grade.

  tools/sr-upscale.py hero-finished                       # x4 master
  tools/sr-upscale.py --all --scale 4
  tools/sr-upscale.py hero-finished --width 2400          # x4 then Lanczos to 2400

Output: work/sr/<name>-x4.png (full master) and, with --width, work/sr/<name>-2400.jpg.

  tools/sr-upscale.py hero-finished --postfix      # re-colour a master, no
                                                  # model run: photo chroma
                                                  # replaces the model's
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "img" / "_orig"
OUT = ROOT / "work" / "sr"
MODEL = Path.home() / "tmp" / "sr-models" / "x4.onnx"


def session():
    import onnxruntime as ort
    providers = [p for p in ("CoreMLExecutionProvider", "CPUExecutionProvider")
                 if p in ort.get_available_providers()]
    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    return ort.InferenceSession(str(MODEL), sess_options=so, providers=providers)


def upscale(sess, img: np.ndarray, scale: int, tile: int = 384, pad: int = 16) -> np.ndarray:
    """Tile with overlap so the seams do not show; the model is fully
    convolutional but tiling keeps peak memory flat on a laptop."""
    h, w, _ = img.shape
    out = np.zeros((h * scale, w * scale, 3), dtype=np.float32)
    name = sess.get_inputs()[0].name
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            y0, x0 = max(0, y - pad), max(0, x - pad)
            y1, x1 = min(h, y + tile + pad), min(w, x + tile + pad)
            chunk = img[y0:y1, x0:x1]
            inp = np.transpose(chunk, (2, 0, 1))[None].astype(np.float32)
            res = sess.run(None, {name: inp})[0][0]
            res = np.transpose(res, (1, 2, 0))
            res = np.clip(res, 0.0, 1.0)
            # crop the pad back off
            top = (y - y0) * scale
            left = (x - x0) * scale
            out[y * scale:(min(y + tile, h)) * scale,
                x * scale:(min(x + tile, w)) * scale] = \
                res[top:top + min(tile, h - y) * scale,
                    left:left + min(tile, w - x) * scale]
    return out


def dims(p: Path) -> tuple[int, int]:
    out = subprocess.run(["magick", "identify", "-format", "%w %h", str(p)],
                         capture_output=True, text=True)
    w, h = out.stdout.split()
    return int(w), int(h)


# --- the model's colour is not evidence -------------------------------------
# Real-ESRGAN x4plus is a structure reconstructor that also invents chroma, and
# on a blown highlight it invents a *saturated* chroma. hero-finished came back
# with a cyan blotch and black speckle in the sky gap between the trees - the one
# thing on a contractor's site that must never look generated. Two rules remove
# it without touching a single reconstructed stone edge:
#   * chroma always comes from the Lanczos upscale of the phone frame, where a
#     near-white sky is near-white by construction;
#   * where the photo's own luma is already at or near clipping, luma comes from
#     the photo too - there is no tonal detail inside a blown highlight for the
#     model to reconstruct, so nothing real is lost there.
# Everywhere else the model's pixels pass through untouched.

_Y = (0.299, 0.587, 0.114)
_CB = (-0.168736, -0.331264, 0.5)
_CR = (0.5, -0.418688, -0.081312)


def _to_ycc(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    y = rgb @ np.array(_Y, dtype=np.float32)
    cb = rgb @ np.array(_CB, dtype=np.float32)
    cr = rgb @ np.array(_CR, dtype=np.float32)
    return y, cb, cr


def _to_rgb(y: np.ndarray, cb: np.ndarray, cr: np.ndarray) -> np.ndarray:
    r = y + 1.402 * cr
    g = y - 0.344136 * cb - 0.714136 * cr
    b = y + 1.772 * cb
    return np.stack([r, g, b], axis=-1)


def hybrid(sr: np.ndarray, src: np.ndarray) -> tuple[np.ndarray, float]:
    """Colour from the photograph, structure from the model. See the note above.

    `src` is the phone frame at its own size; it is resized to the master here so
    the two arrays line up pixel for pixel. Returns the composited master and the
    fraction of the frame where the photo's luma replaced the model's, which is
    the only honest way to say how much of the frame this touched.
    """
    h, w = sr.shape[:2]
    photo = np.asarray(Image.fromarray((src * 255.0 + 0.5).astype(np.uint8))
                       .resize((w, h), Image.LANCZOS), dtype=np.float32) / 255.0
    sr_y, _, _ = _to_ycc(sr)
    ph_y, ph_cb, ph_cr = _to_ycc(photo)
    # a blurred luma decides the mask: per-pixel brightness would stipple it
    smooth = np.asarray(Image.fromarray((np.clip(ph_y, 0, 1) * 255).astype(np.uint8))
                        .filter(ImageFilter.GaussianBlur(6)), dtype=np.float32) / 255.0
    m = np.clip((smooth - 0.88) / 0.08, 0.0, 1.0)
    y = sr_y * (1.0 - m) + ph_y * m
    out = np.clip(_to_rgb(y, ph_cb, ph_cr), 0.0, 1.0)
    return out, float(m.mean())


def postfix(name: str, scale: int) -> None:
    """Re-composite an existing master through hybrid(). No model, no re-run."""
    master = OUT / f"{name}-x{scale}.png"
    src = SRC / f"{name}.jpg"
    if not master.exists():
        print(f"MISS {master.name}")
        return
    t0 = time.time()
    sr = np.asarray(Image.open(master).convert("RGB"), dtype=np.float32) / 255.0
    img = np.asarray(Image.open(src).convert("RGB"), dtype=np.float32) / 255.0
    out, touched = hybrid(sr, img)
    Image.fromarray((out * 255.0 + 0.5).astype(np.uint8)).save(master)
    print(f"{name}: hybrid chroma, photo luma on {touched:.2%} of the frame, "
          f"{time.time()-t0:.1f}s")



def run(name: str, sess, scale: int, width: int | None) -> None:
    src = SRC / f"{name}.jpg"
    if not src.exists():
        print(f"MISS {name}")
        return
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    img = np.asarray(Image.open(src).convert("RGB"), dtype=np.float32) / 255.0
    res = upscale(sess, img, scale)
    res, touched = hybrid(res, img)
    master = OUT / f"{name}-x{scale}.png"
    Image.fromarray((res * 255.0 + 0.5).astype(np.uint8)).save(master)
    sw, sh = dims(src)
    mw, mh = dims(master)
    msg = (f"{name}: {sw}x{sh} -> {mw}x{mh} in {time.time()-t0:.1f}s, photo luma on {touched:.2%}")
    if width:
        dst = OUT / f"{name}-{width}.jpg"
        # Downscale the 4x master to the delivery width with Lanczos: this is the
        # step that turns model texture into believable grain instead of a
        # tell-tale "upscaled" sheen.
        subprocess.run(["magick", str(master), "-filter", "Lanczos",
                        "-resize", f"{width}x", "-strip", "-quality", "92", str(dst)],
                       check=True)
        dw, dh = dims(dst)
        msg += f"; delivered {dw}x{dh} {dst.name}"
    print(msg)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--scale", type=int, default=4)
    ap.add_argument("--width", type=int, default=0)
    ap.add_argument("--postfix", action="store_true",
                    help="re-composite existing masters (no model run)")
    args = ap.parse_args(argv)
    names = args.names
    if args.all:
        names = sorted(p.stem for p in SRC.glob("*.jpg")
                       if not any(t in p.stem for t in ("-900", "-640", "-1200", "-2400"))
                       and not p.stem.startswith("r"))
    if not names:
        ap.error("give at least one name, or --all")
    if args.postfix:
        for n in names:
            postfix(n, args.scale)
        return 0
    if not MODEL.exists():
        raise SystemExit(f"missing model: {MODEL} (see tools/README-photos.md)")
    sess = session()
    for n in names:
        run(n, sess, args.scale, args.width or None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
