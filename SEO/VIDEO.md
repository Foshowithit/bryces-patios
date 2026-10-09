# Bryce's Patios — Video upload package (paste-ready)

**Why:** the site is *live but invisible* (Google 0, Bing 0 — see
`SEO/BASELINE.md` ck114). Real video is the one piece of content that earns
discovery and trust **without** depending on a search engine crawling a brand-new
domain. YouTube is a search engine of its own that ranks new channels fast, and
Google surfaces YouTube for "how to" patio queries. Upload these and you give
Bryce a second front door.

## 2026-10-09 — the reel is now eight REAL job photos (v2, 29 s)

The first shipped reel was built from the old AI renders. It is replaced. The reel
in the repo today is cut from **eight real photos now on the site** (finished
patios, an in-progress paver build over the base, a walkway, steps). No renders.
Silent, no narration, no music, 29.0 s, one h264 stream, zero audio streams.

Repo files (`assets/video/`, cache-buster `dba670bb`):

| Cut | File | Size | Size |
|---|---|---|---|
| 16:9 | `showreel-1080p-silent-dba670bb.mp4` | 1920×1080 | 15,075,228 B |
| 9:16 | `showreel-reel-9x16-dba670bb.mp4` | 1080×1920 | 12,653,408 B |
| 1:1 | `showreel-square-1x1-dba670bb.mp4` | 1080×1080 | 8,333,172 B |

Rendered on the Dell (`~/bryce-reel/work/render-real-silent.sh`). The old
narrated masters stay quarantined in `~/bryce-reel/out/rejected/`.

## 2026-10-09 — second video: a 23 s explainer, "How a patio base is built"

A second, different piece for the YouTube channel: a five-shot explainer cut from
the real in-progress photos (the paver field over the aggregate base, the herringbone
over the setting bed, the edge detail, then the finished patio). On-screen captions
carry it, silent, so it autoplays anywhere. This is the kind of video that answers a
real question ("what is under a paver patio?") rather than a montage, so it can rank
for the query on its own.

Repo files (`assets/video/`):

| Cut | File | Size |
|---|---|---|
| 16:9 | `patio-base-explainer-1080p-silent.mp4` | 23.0 s, 1920×1080, 10,112,905 B |
| 9:16 | `patio-base-explainer-9x16-silent.mp4` | 23.0 s, 1080×1920, 8,541,532 B |

Rendered on the Dell (`~/bryce-reel/work/edu.sh`, `edu-deriv.sh`). Captions voice-gated
SHIP. **Suggested YouTube title:** "What is actually under a paver patio (and why it
matters in New England)". **Description:** paste the site blurb, link
`https://brycespatios.work/learn/patio-base/`, phone `(508) 212-6433`.

---

**Files (1920×1080 / 1080×1920 / 1080×1080, silent, no music):**

Use these. They are the **silent** cuts. Upload them as-is.

- Mac: `~/Movies/bryce-patios-reel/` — 16:9 `showreel-1080p.mp4` (**14,238,968 B**),
  9:16 `showreel-reel-9x16.mp4` (**12,034,636 B**), 1:1 `showreel-square-1x1.mp4` (**7,746,369 B**).
  All three are video-only (`ffprobe` = 1 h264 stream, 0 audio).
- Dell render box: `~/bryce-reel/out/` — same cuts under `-silent` names:
  `showreel-1080p-silent.mp4`, `showreel-reel-9x16-silent.mp4`,
  `showreel-square-1x1-silent.mp4`. All three video-only, 32.233 s.

> **Never upload a file named plain `showreel-1080p.mp4` / `showreel-reel-9x16.mp4` /
> `showreel-square-1x1.mp4` from the Dell.** On the Dell those exact names were the
> **narrated TTS masters**. They are now quarantined in `~/bryce-reel/out/rejected/`
> as `*.NARRATED-rejected-20261009.mp4` (see `BASELINE.md` ck119). If you find a
> plain-named one anywhere, treat it as narrated and re-probe before shipping.

All three are **silent and captioned on-screen** on purpose: silent works autoplay
on every platform, and captions mean it is readable with sound off (which is how
almost everyone watches short video). **Do not add music you do not own** — a
copyright strike kills a new channel.

**Rules for every upload:** business name exactly `Bryce's Patios`; link
`https://brycespatios.work`; phone `(508) 212-6433`; never claim a licence,
insurance, warranty, or review count. The reel is cut from real photos of Bryce's
jobs, so say that plainly if a comment asks.

---

## 1. YouTube — the main channel

**Channel name:** `Bryce's Patios`
**Handle (try in this order):** `@brycespatios` → `@brycespatiosma` → `@brycespatiosmansfield`
**Channel description:**
```
Stone patios, walkways, and hardscape built around Mansfield, MA. Owner-operated.
Free estimates. Call or text (508) 212-6433. brycespatios.work
```
**Channel links:** Website `https://brycespatios.work` · Email
`bryces-patios@agentmail.to`
**Channel art:** the site logo (`/assets/img/logo.png` on the repo) as avatar,
any finished-patio photo as the banner.

### Upload A — the 16:9 showreel (`showreel-1080p-silent.mp4`)

> The shipped reel was renamed to `…-silent` on the Mac on 2026-10-09 (and `V`
> was bumped to `f4a9c1d2` in the same commit) so no browser or CDN cache can serve
> the rejected narrated cut. The shipped file has **no audio stream** — verified by
> `ffprobe` on both the repo copy and a fresh download of the live file
> (`BASELINE.md` ck119). Upload the **silent** file; add YouTube's own music if
> wanted, never the TTS voice.
**Title (pick one, keep under 70 chars):**
```
Stone Patio Design in Mansfield, MA | Bryce's Patios
```
**Description:**
```
A walkthrough of a stone patio design built around Mansfield, MA.

Bryce's Patios builds patios, walkways, and hardscape for homeowners across
Mansfield and the surrounding towns. Owner-operated, free estimates.

The reel is cut from photos of real Bryce's Patios jobs around Mansfield, MA:
finished patios, an in-progress paver build, a walkway and steps.

Website: https://brycespatios.work
Phone or text: (508) 212-6433
Email: bryces-patios@agentmail.to
Area: Mansfield, Attleboro, North Attleboro, Norton, Foxborough, Seekonk,
Rehoboth, Plainville, Franklin, Taunton, Easton, Sharon, and nearby MA + RI towns.

Call Bryce for a free estimate.
```
**Tags (comma-separated, paste as-is):**
```
stone patio Mansfield MA, patio installer Mansfield, paver patio Massachusetts,
hardscape contractor Mansfield, walkway installation MA, patio builder near me,
Bryce's Patios, patio estimate Mansfield MA
```
**Category:** `Howto & Style` (also fine: `People & Blogs`)
**Visibility:** Public · **Made for kids:** No · **Language:** English
**Thumbnail:** frame at ~3 s (the finished-patio shot).

### Upload B — the 9:16 Short (`showreel-reel-9x16.mp4`)
**Title:**
```
Stone patio, Mansfield MA #shorts
```
**Description:** same text as Upload A, plus `#shorts` on its own last line.
Tags: same list, plus `patio shorts`, `hardscape shorts`.
**Category:** `Howto & Style` · **Visibility:** Public

### Upload C — the 1:1 square (`showreel-square-1x1.mp4`)
**Title:**
```
What a stone patio build looks like | Bryce's Patios, Mansfield MA
```
**Description:** same text as Upload A.
**Category:** `Howto & Style` · **Visibility:** Public

> Upload **A** first, then **B** and **C**. Once the channel has the reel, set the
> channel's "Featured video" to A. Add each video's real URL to `SEO/BASELINE.md`
> and to the site footer/schema only after it is live (never link a dead URL).

---

## 2. Pinterest — design-led, photos and short video travel well

**Account:** business account, name `Bryce's Patios`,
website `https://brycespatios.work`.
**Boards to create:** `Stone Patios`, `Paver Walkways`, `Fire Pits & Outdoor
Living`, `Before & After`.
**Upload B (9:16) and C (1:1)** as Idea Pins.
**Pin title:** `Stone patio design ideas | Mansfield, MA`
**Pin description:**
```
Stone patio, walkway, and fire pit ideas for New England yards. Built around
Mansfield, MA. Owner-operated, free estimates. Call or text (508) 212-6433.
brycespatios.work
```
**Link:** `https://brycespatios.work` (Pinterest sends real referral traffic).

---

## 3. Google Business Profile — weekly "Post" (after GBP is live)

Once the GBP exists (`SEO/GBP.md`), post the 16:9 reel as a **Video post**:
**Post text:**
```
New stone patio design walkthrough. Free estimates in Mansfield and nearby towns.
Call or text (508) 212-6433.
```
GBP video posts show on the profile and in Maps; they are one of the few GBP
elements that still move local ranking.

---

## 4. Facebook — the existing page (`Bryces Landscape and Patio Service`)

**Do not edit the page without Bryce's OK** (see checklist §4). If he approves,
upload the 1:1 and 9:16 clips with the same description text. Facebook video reach
is largely free and local.

---

## Ledger — fill in as each goes live

| Platform | Video | URL | Date |
|---|---|---|---|
| YouTube | 16:9 | _pending_ | |
| YouTube | 9:16 | _pending_ | |
| YouTube | 1:1 | _pending_ | |
| Pinterest | 9:16 | _pending_ | |
| Pinterest | 1:1 | _pending_ | |
| GBP post | 16:9 | _pending_ | |
| Facebook | 1:1 | _pending_ | |
