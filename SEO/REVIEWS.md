# Bryce's Patios — Review Generation System

**Why this exists:** for a local contractor, review **count, recency, and rating** are the
single strongest ranking inputs in the Google local pack *and* the strongest conversion
driver on the listing. Bryce has **zero** reviews today. Getting the first 5 is the hardest
and most valuable step; after that the flywheel turns on its own.

**Hard rules — do not break these:**
- **Never buy, trade for, or write a review.** Google detects and penalises it, and the
  suspension risk is real. One fake review can cost the whole profile.
- **Never add `aggregateRating` to the website schema until real reviews exist.** The site
  currently has none and correctly claims none. Once ≥5 real Google reviews are live, we
  add schema + an on-site reviews section (below).
- **Never gate reviews** — do not offer discounts or freebies in exchange for a review.
- **Do not door-knock former customers on Bryce's behalf without his list.** Only ask people
  he has actually done work for, or who have already asked him for a quote.

---

## 1. The direct review link (get this first)

Every ask below needs the short link, which drops the customer straight into the
review box:

1. Google Business Profile → **Ask for reviews** → copy the short link
   (form: `https://g.page/r/<ID>/review`).
2. Paste the short link into this file's placeholder: `[REVIEW_LINK]`.
3. Print it as a QR code for the truck / estimate sheet (optional, later).

**Placeholder used throughout: `[REVIEW_LINK]`**

---

## 2. The ask — timing is the whole game

**Ask at the single best moment:** the day the job is finished and Bryce is packing the
truck, the customer is happy and standing right there. That is the highest-converting
second of the entire relationship. Do **not** wait a week.

**Second-best:** the same evening, by text, while the patio is still new.

**Worst (avoid):** weeks later, by cold email.

Rule of thumb: **one ask at handover, one text reminder 48h later if nothing. Then stop.**
Two touches, max. Nagging costs more goodwill than the review is worth.

---

## 3. In-person script (Bryce says this out loud, at handover)

> "Glad you're happy with it. If you've got thirty seconds, a Google review really helps
> a small shop like mine — most of my work comes from people finding me there. I'll text
> you the link so you don't have to hunt for it."

Then **send the text before he leaves the driveway.** Don't rely on memory.

**Don't say:** "If you leave a review I'll knock X off." (gating — banned)
**Don't say:** "Can you leave me 5 stars?" (leading — technically fine but reads pushy; let them decide)

---

## 4. SMS templates (copy-paste, 2 total)

**SMS 1 — sent at handover (from Bryce's phone):**
```
Hey [NAME], Bryce here — thanks again for having us out. If you've got 30 seconds, a
quick Google review goes a long way for a small shop: [REVIEW_LINK]
No pressure at all either way. Appreciate you.
```

**SMS 2 — 48h reminder, only if no review appeared:**
```
Hey [NAME], just circling back on that review link if you get a sec: [REVIEW_LINK]
Totally fine if not — thanks again for the work. — Bryce
```

**Do not send a third.**

---

## 5. Email template (only when SMS isn't possible)

**Subject:** `Thanks from Bryce's Patios — one small favour`
```
Hi [NAME],

Thanks again for trusting us with the [PROJECT, e.g. patio / walkway] — hope it's
getting plenty of use.

If you have thirty seconds, leaving a Google review would genuinely help: small
businesses live and die on them, and it's how the next person finds us.

[REVIEW_LINK]

No pressure either way.

Bryce
Bryce's Patios
(508) 212-6433
```

---

## 6. Reply policy — reply to every review, in this voice

Replies are public and are read by the *next* customer. Match the register:
short, plain, no exclamation marks, no marketing language.

| Rating | Reply approach |
|---|---|
| 5★ | Thank them by first name, name the specific job if they mentioned it, stop. 1-2 sentences. |
| 4★ | Thank them, acknowledge the part that wasn't perfect if they named one, invite them to call. |
| 3★ | Thank them for the honesty, ask what would have made it a 5, give the phone number. |
| 1-2★ | Stay calm and factual. Do not argue, do not explain in detail publicly. Apologise for their experience, say you'd like to make it right, give the number, move it off the public thread. |

**Example 5★ reply:**
```
Thanks, Dana — glad the patio came out the way you pictured it. Enjoy it.
— Bryce
```

**Example 2★ reply:**
```
Sorry to hear that, [NAME] — that's not the experience I want anyone to have. I'd like
to understand what happened and make it right. Give me a call on (508) 212-6433 when
you have a minute. — Bryce
```

---

## 7. What goes on the website, and when

**Do not add anything review-related to the site until ≥5 real reviews exist.** Right now
the site is honest and clean with none claimed.

Once **≥5 real Google reviews** are live:
1. Add a **Reviews section** on `index.html` above the footer:
   - Section heading in the site's voice, e.g. `What people say`
   - 3-6 real review quotes, first name + town + star count
   - A `Leave a review` button pointing at `[REVIEW_LINK]`
2. Add **`aggregateRating`** to the LocalBusiness JSON-LD:
   ```json
   "aggregateRating": {
     "@type": "AggregateRating",
     "ratingValue": "5.0",
     "reviewCount": "5"
   }
   ```
   → **numbers must be the real live average and count.** Update it as reviews come in.
   Never round up. Never invent a count.
3. Optionally add individual `Review` objects to schema — only with the reviewer's real
   words and first name.

**Trigger to revisit:** whenever Google review count crosses 5, 10, and 25.

---

## 8. Target cadence and who owns it

- **Owner: Bryce** (he's the one on site). Adam can prep everything; only Bryce has the moment.
- **Goal:** every finished job → one ask → one review attempt. Even a 40% conversion
  rate gets to 5 reviews in ~2 weeks of work.
- **First milestone:** **5 reviews** → unlocks `aggregateRating` + the on-site section.
- **Second milestone:** **10 reviews** with a mix of towns → starts showing in local pack
  for the surrounding-town queries, not just Mansfield.

**Tracking (add rows as they happen):**

| Date | Customer | Town | Job | Asked | Reviewed |
|---|---|---|---|---|---|
| | | | | | |
