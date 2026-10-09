#!/usr/bin/env python3
"""Bryce's Patios — static site generator (no build step at deploy time).

Emits static HTML into the repo root so GitHub Pages serves it directly.
Everything here is copy-only unless a page needs new CSS, which is why the
templates reuse assets/css/style.css and assets/js/main.js unchanged.

Run:  python3 work/gen/site.py
"""
from __future__ import annotations
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V = "a1c6e204"          # cache-buster, must match index.html
BASE = "https://brycespatios.work"
PHONE_TEL = "+15082126433"
PHONE_TXT = "(508) 212-6433"
EMAIL = "bryces-patios@agentmail.to"
ADDR = "885 West St, Mansfield, MA 02048"
COORDS = "42.022753;-71.256955"
FB = "https://www.facebook.com/people/Bryces-Landscape-and-Patio-Service/61593835211578/"
OG = f"{BASE}/assets/img/og-cover.jpg"
TODAY = "2026-10-08"

TOWNS_MA = ["Mansfield", "Attleboro", "North Attleboro", "Norton", "Foxborough",
            "Seekonk", "Rehoboth", "Plainville", "Franklin", "Taunton",
            "Easton", "Sharon"]
TOWNS_RI = ["Pawtucket", "Cumberland", "Lincoln", "Central Falls", "Providence",
            "East Providence", "Woonsocket", "Barrington", "Smithfield",
            "North Smithfield"]

# The towns that get a full service x town page (keep in sync with _town_note()).
TOP_TOWNS = ["Mansfield", "Foxborough", "Attleboro", "North Attleboro",
             "Norton", "Franklin"]

# Real photo used on each town page, plus a one-line local read of the yards.
# Images are the same real jobs; the note is per-town and never spun.
TOWN_IMG = {
    "Mansfield": "project-dining", "Attleboro": "project-walkway",
    "North Attleboro": "transform-after", "Norton": "big-yard",
    "Foxborough": "patio-herringbone", "Seekonk": "walkway",
    "Rehoboth": "yard", "Plainville": "steps-detail",
    "Franklin": "transform-before", "Taunton": "stone-arch",
    "Easton": "craft-base", "Sharon": "craft-edge",
}
TOWN_IMG_ALT = {
    "project-dining": "A finished stone patio with a dining table, laid on a compacted base.",
    "project-walkway": "A curved stone walkway leading to a house, set on a compacted base.",
    "transform-after": "A capped stone retaining wall stepping up a graded yard.",
    "big-yard": "A curved stone patio tying a large yard together.",
    "patio-herringbone": "A herringbone stone patio laid off the back stairs of a house.",
    "walkway": "A straight stone walkway with a raised edge course beside a planting bed.",
    "yard": "New pavers with a contrasting border curving into a low block wall.",
    "steps-detail": "Steps and a landing in a stone patio laid up to the grade.",
    "transform-before": "A graded yard during patio base preparation.",
    "stone-arch": "A two-level stone patio in front of a two-level wooden deck.",
    "craft-base": "A patio partly laid, showing the compacted stone base under the pavers.",
    "craft-edge": "Edging and base detail on a stone patio built for a cold climate.",
}

# Per-town read of the local yards. Two short paragraphs, town-specific.
TOWN_INTRO = {
    "Mansfield": ("Mansfield is home, so it is the town we see most, and it is not one kind "
                  "of yard. Stop and go along Route 106 and 140 gives way to quieter streets off "
                  "the Great Woods and Mansfield Crossing side, and the lots change with them. "
                  "The older ones near the center are tight and shaded, with grades that were "
                  "finished by eye decades ago. The newer subdivisions out toward Foxborough and "
                  "Norton are flatter, but the builder left the drainage to whoever came next. "
                  "Both kinds need the same thing before stone goes down: the shape of the yard "
                  "decided first, then the patio set to that. We have dug in this ground long "
                  "enough to know where the ledge sits and how the spring water moves, and it is "
                  "why most of our calls come from neighbors who watched a patio go in."),
    "Attleboro": ("Attleboro sits on ledge and old mill-era lots, so the work starts with "
                  "finding where the rock is and where the water wants to go. Downtown-side "
                  "yards are tight; the ones out toward South Attleboro open up and take a "
                  "bigger patio and a walkway."),
    "North Attleboro": ("North Attleboro yards trend sloped, which is why so many of the jobs "
                        "here turn into steps, a landing and a seat wall. When the grade drops "
                        "hard, we build the transitions so they read as part of the design, not "
                        "as a problem we hid."),
    "Norton": ("Norton lots are bigger and flatter than most of the neighbors, which sounds "
               "easy until the water has nowhere to leave. Here the patio and the drainage get "
               "planned together, so the yard drains around the patio instead of through it."),
    "Foxborough": ("Foxborough has a lot of flat ground and a lot of spring water, so a patio "
                   "here lives or dies on the base. We dig deeper, compact in lifts, and plan the "
                   "slope that sends water out before any stone goes down."),
    "Seekonk": ("Seekonk yards run close to the RI line and the wet ground that comes with it, "
                "so drainage is the first conversation. Walkways and patios here get a base and "
                "a slope built for spring, not for the week of the install."),
    "Rehoboth": ("Rehoboth is big-lot country, with long driveways and back yards that open up "
                 "under a wide sky. That scale changes the job. A patio sized for a suburban "
                 "backyard would get lost here, so the design starts bigger and the walkway has "
                 "to actually be worth the walk. The ground runs sandy in stretches and holds "
                 "water in others, so the base and the slope get read on site before anything is "
                 "priced. Out this way people also want the patio to sit quietly in the land "
                 "rather than shout, and that is usually less about the stone and more about "
                 "where the edges and the grade fall."),
    "Plainville": ("Plainville yards are a mix of newer builds and older homes, and the newer "
                   "ones often have a grade that was never really finished. We fix the shape of "
                   "the yard first, then set the patio to that."),
    "Franklin": ("Franklin sits up where the frost bites harder and springs run wet, so depth "
                 "and compaction decide whether the patio is flat in ten years. This is the town "
                 "where the base matters most, and where we build it deepest."),
    "Taunton": ("Taunton runs from tight city lots to roomy yards out toward the lake, and the "
                "grade swing between them is real. Whatever the lot, the patio gets built to shed "
                "water away from the house, not toward it."),
    "Easton": ("Easton yards often back onto woods and wetland, so the water table is high in "
               "spring. Retaining walls and patios here are built with the drainage worked out "
               "first, and the wall tied in so it does not creep."),
    "Sharon": ("Sharon is hillier than the towns around it, and the yards come with it. Lots "
               "off the Moose Hill and Lake Massapoag sides drop hard enough that flat ground is "
               "the exception, so a patio here usually means steps, a landing and some wall, "
               "staying within what the lot allows and graded so it sits level and still sheds "
               "water away from the house. The stone walls that edge so many Sharon yards are "
               "part of the look too, and we tie new work into their lines rather than cutting "
               "against them."),
}
TOWN_IMG_ALT_DEFAULT = "A finished stone patio built by Bryce's Patios in southeastern Massachusetts."

def slug(s: str) -> str:
    s = s.lower().replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

SERVICES = [
    dict(
        key="patios", name="Stone Patios", short="patios",
        h1="Stone patio installation in {town}, MA",
        meta=("Stone patios built on a full-depth compacted base in {town}, MA and "
              "across southeastern Massachusetts. Owner-operated. Free estimates."),
        blurb=("A patio is a floor that lives outside, so it gets built like one: "
               "dug out to depth, a crushed stone base compacted in lifts, a screeded "
               "bedding layer, and pavers restrained at the edge so the field can't "
               "creep. The visible part is the last inch. Everything that decides "
               "whether it's still flat in ten years is underneath."),
        img="project-dining", img_alt="A finished stone patio with a dining table, laid on a compacted base.",
        bullets=[
            "Full-depth excavation, not a skim over the existing grade",
            "Crushed stone base built in lifts and compacted between each pass",
            "Slope planned to shed water away from the house",
            "Edge restraint set so the field stays put",
        ],
        faq=[
            ("How long does a patio take to install?",
             "Most residential patios run a few days to a couple of weeks depending on square footage, access to the yard and how much digging and hauling the grade needs. You get a start window with the estimate."),
            ("Do I need a permit for a patio in Massachusetts?",
             "Most patios under a certain size don't need a permit, but the line is different in each town and some lots sit in a wetland buffer. We check which side your property falls on before anything is dug."),
            ("What does a patio cost in {town}?",
             "It depends on square footage, the stone you pick and how much site work the grade needs. Paver is the friendliest budget, bluestone and flagstone climb from there. We give you an itemized number after seeing the yard."),
        ],
    ),
    dict(
        key="walkways", name="Walkways & Paths", short="walkways",
        h1="Stone walkway installation in {town}, MA",
        meta=("Stone walkways and garden paths installed in {town}, MA with a proper "
              "compacted base and drainage. Owner-operated. Free estimates."),
        blurb=("A walkway takes more traffic per square foot than any patio, and it "
               "usually sits where water wants to run. That means the same discipline "
               "as a patio in a narrower trench: dig to depth, compact the base in "
               "lifts, set the slope so the path drains, and restrain both edges."),
        img="project-walkway", img_alt="A curved stone walkway leading to a house, set on a compacted base.",
        bullets=[
            "Width and curve laid out around how you actually walk the yard",
            "Base built to the same depth as a patio, in the same lifts",
            "Steps and landings broken out and built to a comfortable rise",
            "Joints and edges detailed so the path holds its line",
        ],
        faq=[
            ("How wide should a walkway be?",
             "Three feet is the comfortable minimum for one person, and closer to four feet feels generous and lets two people pass. If it snows and you want it cleared easily, wider is easier."),
            ("Can you match a walkway to an existing patio?",
             "Yes. If the stone is still available we match it, and where it isn't we lay out a path that reads as deliberate rather than mismatched. Stone and pattern are chosen together with you."),
            ("Do walkways need a base like a patio?",
             "They do. A walkway on bare soil or a thin bed of sand looks fine the first year and then heaves and settles, usually right where water crosses it."),
        ],
    ),
    dict(
        key="retaining-walls", name="Retaining Walls", short="retaining walls",
        h1="Retaining wall installation in {town}, MA",
        meta=("Segmental and stone retaining walls built in {town}, MA with proper "
              "drainage and compaction. Owner-operated. Free estimates."),
        blurb=("A retaining wall holds back the weight of wet soil, so it's the one "
               "hardscape where the hidden work is almost all of the job. A wall is "
               "only as good as its base course, its drainage and what's behind it. "
               "Get those right and the face is the easy part."),
        img="transform-after", img_alt="A capped stone retaining wall stepping up a graded yard.",
        bullets=[
            "A level, compacted base course the rest of the wall sits on",
            "Drainage stone and a path for water behind the wall, not against it",
            "Geogrid or batter as the height and soil load call for",
            "Caps, steps and seat walls detailed to match the house",
        ],
        faq=[
            ("How tall can a retaining wall be before it needs an engineer?",
             "Short garden walls are straightforward. As walls get taller, or when they hold up a driveway or a surcharge, the design and permitting questions grow. We'll tell you when a job belongs with an engineer."),
            ("Why do retaining walls lean or bulge?",
             "Almost always water. Soil that stays saturated is far heavier than dry soil and pushes harder than the wall was built for. Proper drainage behind the wall is what prevents it."),
            ("Do I need a permit for a retaining wall?",
             "It depends on the town and the wall height, and rules differ across the state line. We check the requirement for your property before the work is scheduled."),
        ],
    ),
    dict(
        key="fire-pits", name="Fire Pits & Outdoor Living", short="fire pits",
        h1="Fire pit installation in {town}, MA",
        meta=("Stone fire pits, seat walls and patio living spaces built in {town}, MA. "
              "Owner-operated. Free estimates."),
        blurb=("A fire pit is the thing you end up using most, and the thing most often "
               "dropped onto a patio that wasn't planned for it. Building it into the "
               "layout from the start is what makes it feel like part of the yard "
               "instead of an afterthought."),
        img="project-firepit", img_alt="A circular stone fire pit set into a stone patio with seating around it.",
        bullets=[
            "Built into the patio layout, with seating sized to the circle",
            "Matching stone, caps or a steel insert for a clean bowl",
            "Clearance and grade around the pit planned for drainage",
            "Seat walls, steps and lighting detailed alongside it",
        ],
        faq=[
            ("What size fire pit should I build?",
             "Most backyard pits land between three and four feet across inside; that's a comfortable circle for four to six people. Bigger looks impressive and then never gets a fire warm enough to enjoy."),
            ("Can you add a fire pit to an existing patio?",
             "Often, yes. If the layout and the base will take it we can build one in. Sometimes the honest answer is that the patio was never graded for it, and we'll say so."),
            ("Wood or gas?",
             "Wood is the classic and what most people picture. Gas is cleaner to start and stop. We build the bowl either way and can discuss the trade-off when we look at the yard."),
        ],
    ),
]

GUIDES = [
    dict(
        key="patio-base", tag="01. The base", title="Nine-tenths of it is underground",
        h1="What's under a patio (and why it matters)",
        meta="The paver is the last inch of a patio. Here's the base underneath it, in plain language, and why it decides whether the patio stays flat.",
        lede="The pavers you see are the last inch. Everything that decides whether the patio is still flat in ten years is underneath them and invisible when the job is done.",
        paras=[
            "Under the pavers sit the bedding layer, the crushed stone base and the depth of the dig. Each layer has a job. The dig removes soil that would move under frost and water. The base, built up in lifts and compacted between each pass, spreads the load and stays put. The bedding layer is screeded flat so the pavers sit even.",
            "The failure mode is easy to picture. Pavers laid on dirt, or on a base dumped in one pass and never compacted, look exactly the same on day one as a job done right. It shows up the first hard winter, when a paver moves and never settles back.",
        ],
        note=("<strong>Ask anyone bidding:</strong> how deep are you digging, and how "
              "thick is the base? A real job has a number for both. A vague answer is "
              "an answer."),
        img="craft-base", img_alt="A patio partly laid, showing the compacted stone base and bedding layer under the pavers.",
    ),
    dict(
        key="drainage", tag="02. Drainage", title="Water always finds the low spot",
        h1="How a patio drains (and why it fails)",
        meta="Pooling water and sinking pavers are almost always a grading problem. Here's how drainage under a patio actually works.",
        lede="A patio should shed water like a roof does: away from the house, off the surface and out. That comes from the slope built into it, not from sand added later.",
        paras=[
            "Water that sits on a patio is almost always a grading problem rather than a stone problem. The surface is set to slope, the joints and base are planned to drain together, and the whole thing sends water somewhere it can leave. When any of that is off, water sits, the base below softens and pavers sink unevenly.",
            "It's the single most common reason patios fail around here, and it's also the cheapest thing to get right at the start and the most expensive to fix later. Puddling at a door is usually the same problem showing up years in.",
        ],
        note=("<strong>Easiest test:</strong> after a heavy rain, look where the puddles "
              "sit. If the same spot is wet days later, the grade is telling you "
              "something before anyone digs."),
        img="transform-after", img_alt="A graded patio surface shedding water away from a house.",
    ),
    dict(
        key="frost", tag="03. Frost", title="Why the freeze beats shallow work",
        h1="Frost and patios in Massachusetts",
        meta="Ground here freezes and thaws all winter. Here's why patio depth isn't optional in Massachusetts, in plain language.",
        lede="Ground here freezes and thaws many times over a winter. Each cycle lifts the soil, and anything sitting too close to the surface comes up with it.",
        paras=[
            "Mansfield and the towns around it sit in a 30-inch frost zone. The ground can freeze about two and a half feet down. That number is why patios here fail and patios in the Carolinas don't. Depth isn't a premium option; it's what keeps the surface below the layer that moves.",
            "Here's what the freeze does. Water sits in the soil, freezes, and pulls more water up into the ice. Ice takes up more room than water, so the soil swells, then drops back when it thaws. Anything sitting in that band gets carried with it. A patio dug out below the frost and rebuilt with compacted stone sits in ground that stays put.",
            "Failure is gradual, then sudden. The first winter one paver sits a hair high. The second winter a joint opens and water gets under the field. On day one it looked perfect; that's the point.",
            "Depth also has to be paired with drainage. A deep base holding water is worse than a shallow base that drains. Frost and drainage are one conversation here, and the slope gets planned before the first scoop of dirt comes out.",
        ],
        checklist=[
            "30-inch frost zone: base and dig planned from that number",
            "Base compacted in lifts, not dumped in one pass",
            "Slope planned so water leaves the base, not sits in it",
            "Edges restrained so the field cannot spread as it freezes",
        ],
        note=("<strong>Watch for:</strong> a quote far cheaper than the rest. Sometimes "
              "that is a lower labor rate. More often it is less digging, which you "
              "will never see."),
        img="steps-detail", img_alt="A patio set to the grade, with steps and a landing, on a site built for a cold winter.",
    ),
    dict(
        key="materials", tag="04. Materials", title="Stone is a budget, not a style",
        h1="Paver vs. bluestone vs. flagstone",
        meta="Paver, bluestone and flagstone explained plainly: what each looks like, what each costs, and which fits your project.",
        lede="Picking the look is the easy part. What moves the price is the material itself and how much cutting it needs.",
        paras=[
            "The three surfaces people weigh most often are paver, bluestone and flagstone, with dry-stacked fieldstone on the walls. Each carries its own look and its own labor cost, and that gap is mostly about cutting and setting time.",
        ],
        bullets=[
            ("Paver", "uniform, cut to fit, fastest to lay. Good for clean lines and a tight budget."),
            ("Bluestone", "natural stone, cooler and more varied up close. Costs more per foot and takes longer."),
            ("Flagstone", "irregular shapes, the traditional look. Lots of cutting, so it lives in the higher range."),
            ("Fieldstone walls", "dry-stacked, no mortar. Slowest of all, and the one people stop to look at."),
        ],
        note=("Stone choice is a budget conversation as much as a design one, and the "
              "right answer is usually a mix: a hard-wearing surface with one feature "
              "that carries the look."),
        img="patio-herringbone", img_alt="Close view of a herringbone stone pattern on a patio surface.",
    ),
    dict(
        key="the-quote", tag="05. The quote", title="What a real estimate includes",
        h1="What a patio estimate should include",
        meta="What a real patio estimate itemizes, and the questions to ask any contractor bidding on your yard.",
        lede="A lump-sum price tells you nothing. The useful ones are itemized enough that you know what you're buying.",
        paras=[
            "A useful estimate names the things that decide the job: how much is excavated and hauled away, the base depth in inches, which stone and pattern, edge restraint, a stated drainage plan for your grade, and any steps, seat walls and lighting broken out separately.",
            "It also names when they start and who's on site doing the work. Those two lines tell you a lot about how the job will actually run.",
        ],
        checklist=[
            "Excavation and how much material leaves the site",
            "Base depth, in inches, not \"to code\"",
            "Which stone, and the actual pattern or size",
            "Edge restraint: the hidden piece that keeps the border from spreading",
            "Drainage plan for your grade, stated plainly",
            "Steps, seat walls and lighting broken out separately",
            "When they start, and who's on site doing it",
        ],
        note=("<strong>The tell:</strong> a bidder who asks about your grade and how "
              "you'll use the space is planning a build. One who only asks how you want "
              "it to look is quoting a surface."),
        img="craft-edge", img_alt="Edging detail on a finished stone patio.",
    ),
    dict(
        key="your-questions", tag="06. Your questions", title="Ask us anything",
        h1="Questions about your patio? Ask us",
        meta="Questions about your yard, your drainage or a bid you've been given? Ask Bryce's Patios directly. Free estimates in Mansfield, MA.",
        lede="You don't need to know any of this to get a good patio. That's our job. But if you have a question about your own yard, the drainage around your house, or a number someone gave you, just ask.",
        paras=[
            "We'd rather answer it up front than fix a patio you didn't want later. Tell us where you are and what you're thinking about and we'll give you a straight answer.",
        ],
        bullets=[
            ("\"How much is a patio?\"", "It depends on size, dig, drainage and access. Any number texted before the yard is walked is a guess. Send a photo and the rough size and we can give you a real range."),
            ("\"How long does it take?\"", "Days, not weeks, for a normal patio. Weather is the variable, and we build year-round. You get a start window before we begin."),
            ("\"Do I need a permit?\"", "It depends on the town and whether anything touches a structure or a property line. We tell you what your town's rules mean for your job before it starts."),
            ("\"What about drainage?\"", "It's the first thing we read on any yard. A patio that sheds water away from the house is the whole point, and the slope gets planned before anything is dug."),
            ("\"Can you work with what I have?\"", "Often, yes. Existing steps, walls and walks can be tied in, replaced or left alone. We'll tell you honestly where reusing helps and where it costs you later."),
            ("\"Do you do repairs?\"", "Sunken pavers, spreading edges, a wall that's leaning. Small repairs are welcome, and we'll say if a rebuild makes more sense than a patch."),
        ],
        cta=True,
        img="about-site", img_alt="A finished stone patio beside a house in southeastern Massachusetts.",
    ),
dict(
    key="paver-cost", tag="07. Cost", title="What a paver patio actually costs",
    h1="What a paver patio costs in Massachusetts",
    meta="A plain-language look at what drives the price of a paver patio in Massachusetts and Rhode Island, and where cheap quotes hide the difference.",
    lede="Nobody likes a vague number, so here is how a patio price is actually built: size first, then what is under it, then how hard it is to get to.",
    paras=[
        "The honest answer on cost is that it depends on four things: how big the patio is, how deep the base has to go, how much the ground has to change to drain, and how hard it is for a machine to reach the work. A flat, open backyard with good access is a different job than a tight side yard you have to wheelbarrow through.",
        "That is why a price per square foot texted before anyone looks at the yard is a guess. Two patios the same size can differ by thousands once digging, drainage and access are counted. When you get a bid, ask what it includes. Dig depth, base thickness, edge restraint, drainage and cleanup should all be named. If a quote is just a number with no breakdown, that is the thing to question.",
        "Here is a rough shape for the area, using paver on a full-depth base. A small patio, say 10 by 12 feet, is the low end. A 16 by 20 foot patio is the middle. Anything with steps, a seat wall or a fire pit is priced as the patio plus the added structure. These are ranges, not quotes, and the only real number comes from walking the yard.",
        "Walls and steps are where budgets move fastest. Every course of a retaining wall adds both stone and labor, and any spot that needs a step instead of a slope adds cutting and a solid footing. A fire pit is a modest add-on by itself, but it needs the same base and clearances as a small patio, so it is never free.",
        "Time is the other half of the number. A simple patio with easy access is usually days, not weeks, from dig to cleanup. Add drainage, steps or a large wall and the calendar stretches. Weather pushes it further, since digging frozen or soaked ground is slower and we do not set stone in a downpour. A build in May and a build in November are not the same job.",
    ],
    bullets=[
        ("Size and shape", "straight runs are faster than curves and cutouts"),
        ("Base depth", "more dig and more stone when the soil is soft"),
        ("Drainage", "the yard decides how much grading is needed"),
        ("Access", "tight paths and long carries add labor"),
        ("Stone choice", "some pavers and patterns simply cost more"),
        ("Steps and walls", "each course adds stone, labor and a footing"),
        ("Cleanup and haul", "removed soil has to leave the site"),
    ],
    note=("<strong>The tell:</strong> a real bid names the base and the drainage. "
          "A price with no breakdown is a number, not an estimate."),
    img="project-dining", img_alt="A finished stone patio with a dining area behind a house.",
),
dict(
    key="patio-vs-concrete", tag="08. Choices", title="Pavers, concrete or stamped concrete",
    h1="Pavers vs concrete vs stamped concrete",
    meta="Paver patio, poured concrete or stamped concrete in Massachusetts: how they differ in cost, cracking, repairs and how they age through a hard winter.",
    lede="All three can make a flat outdoor floor. They behave very differently after a Massachusetts winter, and that is the part worth understanding before you pick.",
    paras=[
        "Poured concrete is one continuous slab. That is its strength and its weakness: when the ground moves under a slab, which it does with our freeze and thaw, the slab cracks, and a crack runs where it wants to. Stamped concrete is the same slab with a pattern pressed into the surface. It looks good on day one and ages with the same slab underneath it.",
        "Pavers are separate units set in a base on purpose. The base is built to move a little without tearing. If one paver settles or cracks, it can be lifted and reset without replacing the whole patio. Concrete cannot be repaired that way. That is the trade: pavers cost more up front and are far easier to fix later.",
    ],
    bullets=[
        ("Poured concrete", "lowest up front, cracks as one piece, hard to repair"),
        ("Stamped concrete", "pattern on a slab, same cracking behavior"),
        ("Pavers", "more up front, fixable in sections, forgiving of frost"),
    ],
    img="transform-after", img_alt="A finished paver patio beside a home.",
),
dict(
    key="winter-ready", tag="09. Seasons", title="Getting a patio through a New England winter",
    h1="How to get a patio through a winter",
    meta="Simple, practical steps to keep a paver patio, walkway or retaining wall in good shape through a Massachusetts winter and spring thaw.",
    lede="A patio built right survives winter on its own. The things you do at the edges of the season are what keep it looking new.",
    paras=[
        "The base and the slope are doing the heavy lifting all winter, even under two feet of snow. Your job is small: keep the surface draining, do not carve it up with a steel blade, and watch the low corners when the thaw comes. Water that has somewhere to go does no damage. Water that pools and freezes is what moves things.",
        "The single most common winter mistake is scraping a paver surface with a steel snow shovel or a metal-edged plow. That scratches the finish and can catch a joint. A plastic shovel or a rubber-edged blade from the house out is plenty. Spread sand or a pet-safe melt rather than rock salt, and do not chip ice off with a bar. Come spring, a quick look at the edges and joints tells you everything is fine, and a small sweep of sand back into the joints finishes the job.",
    ],
    checklist=[
        "Shovel with plastic or rubber, not steel",
        "Keep snow piled off the low side so melt has a path",
        "Use sand or pet-safe melt, not rock salt",
        "After the thaw, sweep sand back into the joints",
    ],
    note=("<strong>Easiest habit:</strong> shovel the same direction the water drains, "
          "so you are never pushing melt back against the house."),
    img="craft-edge", img_alt="A finished patio edge showing tight paver joints.",
),
dict(
    key="choosing-contractor", tag="10. Hiring", title="How to spot a good crew from a bad one",
    h1="How to tell a good patio crew from a bad one",
    meta="What to watch for when hiring a patio contractor in Massachusetts, from how they measure, to what they put in writing, to what shows up on site.",
    lede="You are not expected to know stone. You are allowed to watch how someone works, and that tells you almost everything.",
    paras=[
        "A good crew measures, asks about water, and puts the base in writing. A bad one quotes a number from the truck and starts tomorrow. You do not need to catch a technical mistake to tell the difference. You just need to notice whether anyone on the job is thinking about anything you cannot see.",
        "Ask two questions and listen. First: how deep are you digging and how thick is the base? A real answer has numbers. Second: what happens to the water? A real answer mentions slope, the direction of the grade, and where it goes. Then ask who will actually be on site, since some companies sell the job and send a different crew. The person who will do the work should be the person who walked the yard.",
    ],
    checklist=[
        "They measure and look at the grade, not just the shape",
        "The base depth and dig are stated as numbers",
        "Drainage is explained, not waved off",
        "The crew doing the work is named",
        "You get a written scope, not just a price",
    ],
    img="craft-base", img_alt="Preparing the base for a patio installation.",
),
dict(
    key="driveway-aprons", tag="11. Walkways", title="Walkways, steps and aprons",
    h1="Walkways, steps and driveway aprons",
    meta="How walkways, steps and driveway aprons are built in Massachusetts and Rhode Island, and why the base and slope matter as much as the stone you see.",
    lede="A walkway is a small patio you use every day. Because you use it every day, the details that fail are the ones you will notice first.",
    paras=[
        "Walkways and steps get the same base and drainage as a patio, only tighter and steeper, which makes them less forgiving. A step that is a hair out of level or a walk that slopes the wrong way is felt, not just seen. That is why a good walkway build starts with the height difference from the door to the grade, not with the look of the stone.",
        "A driveway apron, where the paved surface meets the road or the garage, is the one spot that catches everything: plow snow, running water, and the weight of whatever rolls over it. It needs a solid edge and a slope that sends water away from both the house and the street. Done right, it is invisible and lasts. Done wrong, it is the first thing to move.",
    ],
    bullets=[
        ("Steps", "risers stay even, treads stay level, edges get restraint"),
        ("Walkways", "slope away from the house, base as deep as a patio"),
        ("Aprons", "built for plow and traffic, water sent clear"),
    ],
    img="project-walkway", img_alt="A finished stone walkway leading to a home.",
),
dict(
    key="yard-grades", tag="12. Drainage", title="Where does your yard drain?",
    h1="How to read the water in your own yard",
    meta="A simple way for homeowners to watch water move across their yard after rain, and why that matters before any patio, walkway or wall project.",
    lede="Before anyone talks stone, walk your yard after a real rain. Where the water goes tells you more than any plan.",
    paras=[
        "Put on boots after the next heavy rain and walk the property. Look for the low spots, the puddle that takes a day to leave, the streak where water crosses the lawn, and the corner against the house that stays wet. You are not diagnosing anything, you are just watching. Water always takes the easiest path downhill, and that path is the same path a new patio has to work with, not against.",
        "Write down where it goes and take a few pictures. When Bryce estimates the job, those pictures answer half the questions before he arrives. If a yard has nowhere to send water, the plan has to make somewhere. If it already drains well, the build just has to respect it. Knowing which one you have puts you ahead of most homeowners before the first bid.",
    ],
    checklist=[
        "Walk the yard right after a heavy rain",
        "Mark the low spots and the slow puddles",
        "Note where water crosses the lawn",
        "Check the corner against the house",
        "Take photos to show at the estimate",
    ],
    img="craft-base", img_alt="A yard during base preparation, showing grade and drainage work.",
),
]

def esc(s: str) -> str:
    return html.escape(s, quote=True)

def jsonld(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def business_ld() -> dict:
    return {
        "@type": "LandscapingBusiness",
        "@id": f"{BASE}/#business",
        "additionalType": "https://schema.org/HomeAndConstructionBusiness",
        "name": "Bryce's Patios",
        "url": f"{BASE}/",
        "telephone": "+1-508-212-6433",
        "email": EMAIL,
        "priceRange": "$$",
        "currenciesAccepted": "USD",
        "image": f"{BASE}/assets/img/og-cover.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "885 West St",
            "addressLocality": "Mansfield",
            "addressRegion": "MA",
            "postalCode": "02048",
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 42.022753, "longitude": -71.256955},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "08:00", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Saturday", "Sunday"],
             "opens": "08:00", "closes": "18:00",
             "description": "By appointment"},
        ],
        "sameAs": [FB],
        "areaServed": [{"@type": "City", "name": f"{t}, MA"} for t in TOWNS_MA]
                      + [{"@type": "City", "name": f"{t}, RI"} for t in TOWNS_RI],
    }

def head(*, title, desc, canonical, ld_blocks, extra_head="") -> str:
    blocks = "\n".join(
        '<script type="application/ld+json">%s</script>' % jsonld(b) for b in ld_blocks
    )
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#F7F4EE">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="geo.region" content="US-MA">
<meta name="geo.placename" content="Mansfield, Massachusetts">
<meta name="geo.position" content="{COORDS}">
<meta name="ICBM" content="42.022753, -71.256955">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Bryce&apos;s Patios">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2314171A'/%3E%3Cg fill='%23F7F4EE'%3E%3Crect x='4' y='5' width='14' height='10' rx='1.6'/%3E%3Crect x='20' y='5' width='8' height='10' rx='1.6'/%3E%3Crect x='4' y='17' width='8' height='10' rx='1.6'/%3E%3Crect x='14' y='17' width='14' height='10' rx='1.6'/%3E%3C/g%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{BASE}/assets/img/og-cover.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Inter:wght@300..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v={V}">
<link rel="alternate" type="application/atom+xml" title="Bryce's Patios guides" href="{BASE}/feed.xml">
{extra_head}{blocks}
</head>"""

NAV = f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="nav" id="nav">
  <div class="nav__inner">
    <a class="wordmark" href="/" aria-label="Bryce's Patios, home">
      <svg class="wordmark__mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <rect x="0" y="0" width="14" height="10" rx="1.4"></rect>
        <rect x="16" y="0" width="8" height="10" rx="1.4"></rect>
        <rect x="0" y="12" width="8" height="10" rx="1.4"></rect>
        <rect x="10" y="12" width="14" height="10" rx="1.4"></rect>
      </svg>
      <span class="wordmark__text">Bryce's<span class="wordmark__thin">&nbsp;Patios</span></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
      <a href="/#work">Work</a>
      <a href="/#craft">Craft</a>
      <a href="/#about">About</a>
      <a href="/learn/">Learn</a>
      <a href="/#area">Service Area</a>
    </nav>
    <div class="nav__actions">
      <a class="nav__phone" href="tel:{PHONE_TEL}">
        <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.2 1.5h2.3l1.1 2.8-1.5 1.1a9 9 0 0 0 4.5 4.5l1.1-1.5 2.8 1.1v2.3c0 .6-.5 1.1-1.1 1.1A11.9 11.9 0 0 1 2.1 2.6c0-.6.5-1.1 1.1-1.1Z"/></svg>
        <span>(508)&nbsp;212-6433</span>
      </a>
      <a class="btn btn--sm btn--solid" href="/#estimate">Get an estimate</a>
      <button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">
        <span></span><span></span>
      </button>
    </div>
  </div>
  <div class="nav__progress" id="progress" aria-hidden="true"></div>
</header>

<div class="drawer" id="drawer" hidden>
  <nav class="drawer__links" aria-label="Mobile">
    <a href="/#work"><span class="drawer__num">02</span>Work</a>
    <a href="/#craft"><span class="drawer__num">04</span>Craft</a>
    <a href="/#about"><span class="drawer__num">05</span>About</a>
    <a href="/learn/"><span class="drawer__num">06</span>Learn</a>
    <a href="/#area"><span class="drawer__num">07</span>Service Area</a>
  </nav>
  <div class="drawer__foot">
    <a class="btn btn--solid btn--block" href="/#estimate">Get a free estimate</a>
    <a class="drawer__tel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a>
    <p class="drawer__meta">Mansfield, Massachusetts<br>Serving southeastern MA &amp; Rhode Island</p>
  </div>
</div>"""

STICKY = f"""<div class="sticky-cta" id="sticky-cta" hidden>
  <a class="sticky-cta__call" href="tel:{PHONE_TEL}" aria-label="Call Bryce's Patios">
    <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.2 1.5h2.3l1.1 2.8-1.5 1.1a9 9 0 0 0 4.5 4.5l1.1-1.5 2.8 1.1v2.3c0 .6-.5 1.1-1.1 1.1A11.9 11.9 0 0 1 2.1 2.6c0-.6.5-1.1 1.1-1.1Z"/></svg>
    Call
  </a>
  <a class="sticky-cta__est" href="/#estimate">Get a free estimate</a>
</div>"""


def page_actions(*, center: bool = False) -> str:
    """Above-the-fold call + estimate row for inner pages (no hero)."""
    cls = "page-actions page-actions--center" if center else "page-actions"
    return (f'<div class="{cls}">'
            f'<a class="btn btn--solid btn--lg" href="/#estimate">Get a free estimate</a>'
            f'<a class="btn btn--ghost btn--lg" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a>'
            f'</div>')


def footer(service_links: list[tuple[str, str]], town_links: list[tuple[str, str]]) -> str:
    svc = "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in service_links)
    twn = "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in town_links)
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="wordmark wordmark--light" href="/">
          <svg class="wordmark__mark" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <rect x="0" y="0" width="14" height="10" rx="1.4"></rect>
            <rect x="16" y="0" width="8" height="10" rx="1.4"></rect>
            <rect x="0" y="12" width="8" height="10" rx="1.4"></rect>
            <rect x="10" y="12" width="14" height="10" rx="1.4"></rect>
          </svg>
          <span class="wordmark__text">Bryce's<span class="wordmark__thin">&nbsp;Patios</span></span>
        </a>
        <p class="footer__tag">Stone patios, walls &amp; fire pits.</p>
        <ul class="footer__social">
          <li><a href="{FB}" aria-label="Bryce's Patios on Facebook" rel="noopener" target="_blank">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.4h-1.2c-1.2 0-1.6.8-1.6 1.6V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12Z"/></svg>
          </a></li>
        </ul>
      </div>

      <div class="footer__col">
        <h3>Contact</h3>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><address class="footer__addr">{ADDR}</address></li>
          <li><a href="/#estimate">Request an estimate</a></li>
        </ul>
      </div>

      <div class="footer__col">
        <h3>Services</h3>
        <ul>{svc}</ul>
      </div>

      <div class="footer__col">
        <h3>Areas</h3>
        <ul>{twn}</ul>
      </div>
    </div>

    <div class="footer__base">
      <p>&copy; <span id="year">2026</span> Bryce's Patios. All rights reserved.</p>
      <p class="footer__fine">Based in Mansfield, MA. Serving southeastern Massachusetts and Rhode Island. {ADDR}. <a href="/feed.xml">Guides feed</a>.</p>
    </div>
  </div>
</footer>
{STICKY}
<script src="/assets/js/main.js?v={V}" defer></script>"""

def breadcrumb_ld(trail: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(trail)
        ],
    }

def page_ld(url: str, name: str, trail) -> dict:
    return {
        "@type": "WebPage",
        "@id": url,
        "url": url,
        "name": name,
        "isPartOf": {"@id": f"{BASE}/#website"},
        "about": {"@id": f"{BASE}/#business"},
        "breadcrumb": breadcrumb_ld(trail),
    }

WEBSITE_LD = {
    "@type": "WebSite",
    "@id": f"{BASE}/#website",
    "url": f"{BASE}/",
    "name": "Bryce's Patios",
    "publisher": {"@id": f"{BASE}/#business"},
}

def render_shell(*, title, desc, url, trail, body, ld_extra, svc_links, town_links) -> str:
    lds = [WEBSITE_LD, business_ld(), page_ld(url, title.split(" | ")[0], trail)] + ld_extra
    return f"""<!DOCTYPE html>
<html lang="en">
{head(title=title, desc=desc, canonical=url, ld_blocks=lds)}
<body>
{NAV}
<main id="main">
{body}
</main>
{footer(svc_links, town_links)}
</body>
</html>
"""

def crumb_html(trail) -> str:
    items = []
    for i, (name, url) in enumerate(trail):
        last = i == len(trail) - 1
        if last:
            items.append(f'<span aria-current="page">{esc(name)}</span>')
        else:
            items.append(f'<a href="{url}">{esc(name)}</a>')
    inner = '<span class="crumb__sep" aria-hidden="true">/</span>'.join(items)
    return f'<nav class="crumb" aria-label="Breadcrumb">{inner}</nav>'


# ── related guides + contextual service links (WS3) ───────────────────────
# Three same-family guides per guide page. Keeps readers inside /learn/ and
# gives every guide page three internal links with descriptive anchors.
RELATED = {
    "patio-base": ["frost", "drainage", "materials"],
    "drainage": ["yard-grades", "patio-base", "frost"],
    "frost": ["patio-base", "drainage", "winter-ready"],
    "materials": ["paver-cost", "patio-vs-concrete", "the-quote"],
    "the-quote": ["choosing-contractor", "paver-cost", "patio-base"],
    "your-questions": ["the-quote", "choosing-contractor", "patio-base"],
    "paver-cost": ["materials", "the-quote", "patio-vs-concrete"],
    "patio-vs-concrete": ["materials", "paver-cost", "frost"],
    "winter-ready": ["frost", "drainage", "yard-grades"],
    "choosing-contractor": ["the-quote", "your-questions", "materials"],
    "driveway-aprons": ["materials", "drainage", "patio-base"],
    "yard-grades": ["drainage", "frost", "driveway-aprons"],
}

# guide key -> the service page it naturally sits next to
GUIDE_SERVICE = {
    "patio-base": "patios",
    "drainage": "patios",
    "frost": "patios",
    "materials": "patios",
    "the-quote": "patios",
    "your-questions": "patios",
    "paver-cost": "patios",
    "patio-vs-concrete": "patios",
    "winter-ready": "patios",
    "choosing-contractor": "patios",
    "driveway-aprons": "walkways",
    "yard-grades": "retaining-walls",
}
