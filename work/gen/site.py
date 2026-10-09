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
V = "b7d3f918"          # cache-buster, must match index.html
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
    "project-dining": "A stone paver patio in dappled shade, with chairs and planters along the edge.",
    "project-walkway": "Flagstone steps and a low stacked-stone wall rising through a planted bed.",
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
                  "why most of our calls come from neighbors who watched a patio go in. "
                  "If you have been looking for a patio installer in Mansfield, MA, we are "
                  "twenty minutes from most of the town."),
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
# Per-town second read: what the jobs here actually involve, and what drives cost.
# Real, checkable local facts only. Three short paragraphs, town-specific, no spin.
TOWN_DETAIL = {
    "Mansfield": [
        "Most Mansfield work starts with the same question: where does the water go when the snow melts? "
        "The lots off Route 106 and around the Great Woods side were finished decades apart, so the grade "
        "under any one yard can fall a foot over twenty feet or barely move at all. Before a stone is set we "
        "read the slope against the house, and the patio is set to shed away from the foundation rather than "
        "toward it. In the older shaded yards near the center, that often means a shallow swale dressed to "
        "look like planting instead of a trench.",
        "Mansfield sits in the 30-inch frost zone, so the base under a patio here is dug out past the depth "
        "that freezes and thawed, then rebuilt in compacted lifts. That is the part nobody sees. It is also "
        "the part that decides whether the surface is still flat five winters from now. If a quote for a "
        "patio in town comes in well under the others, the first thing to ask is how deep they plan to dig.",
        "Mansfield is home base, so we are usually on site the same week a call comes in, and a patio of "
        "400 to 500 square feet is normally a handful of working days once we start: dig and haul one day, "
        "base and compaction the next, then setting and cuts. Timelines move with access, how tight the "
        "back yard is, and how much cutting the pattern needs. A simple field with a clean border goes "
        "faster than a herringbone with curves.",
    ],
    "Attleboro": [
        "Attleboro is ledge country, and the old mill-era lots downtown do not help. On a lot like that the "
        "first real work is finding the rock and reading where the water already runs, because both decide "
        "how deep the dig can actually go before the grade has to change shape. Where ledge sits high, the "
        "answer is usually to build up rather than dig down, and that means retaining a fill that will not "
        "creep.",
        "Yards toward South Attleboro open up and take a bigger patio with a walkway that is worth laying "
        "out properly, rather than a short path patched onto the corner of a deck. The tighter downtown "
        "yards do better with a compact patio set close to the house and a path kept narrow, so the small "
        "space still reads as finished instead of crowded.",
        "Base depth and compaction still follow the same 30-inch frost zone the rest of the area sits in, "
        "and mixed grades mean the transitions, steps and any low wall get planned before the stone gets "
        "picked. Material choice in Attleboro tends toward paver and bluestone for durability on uneven "
        "ground; flagstone shows up where the look matters more than the budget.",
        "Attleboro work also runs along the Rhode Island line at South Attleboro, which means a couple of jobs a year start as a call from just over the border. The same rules apply on either side of the line: dig to depth, compact in lifts, and send the water where it needs to go. What changes is only how far the material has to come, and that is a small part of any price.",
    ],
    "North Attleboro": [
        "North Attleboro yards trend sloped, which is why so many jobs here turn into steps, a landing and "
        "a seat wall rather than a flat pad. When the grade drops hard off the back of the house, the "
        "interesting part is not the patio itself but the transitions, and those get built so they read as "
        "part of the design instead of a problem that got hidden behind a wall.",
        "On slope work the base matters twice as much. A patio on a hill is holding back fill on the high "
        "side and holding the surface on the low side, so the dig, the compaction and the restraint at the "
        "edges all have to agree with each other. A wall here is not just a look, it is what keeps the "
        "patio from sliding with the grade over a few winters.",
        "The mix of older homes and newer builds means the yards are inconsistent from street to street. "
        "Some were graded by hand and finished by eye, some were left to the builder's last day on site. "
        "We look at the yard in person before pricing, because a number quoted off a photo on a sloped lot "
        "is a guess, not an estimate.",
        "North Attleboro also has a good number of homes where the back yard drops more than a full story, which turns a simple patio into a small terraced project. Those jobs take longer and cost more, but they also give the yard something it did not have. If the drop is that steep, it is worth walking the yard before either of us guesses at a number.",
    ],
    "Norton": [
        "Norton lots are bigger and flatter than most of the neighbors, which sounds like an easy job until "
        "you notice the water has nowhere to leave. On flat ground the patio and the drainage are one "
        "design, so the yard carries water around the patio instead of through it. That often means grading "
        "a shallow path for water to travel before the base goes in, because once the stone is down the "
        "surface drains only as well as the ground under it.",
        "Larger lots also change the plan itself. A patio sized for a suburban back yard gets lost on a lot "
        "this big, so the scale starts bigger and the walkway has to be worth walking. We would rather lay "
        "out one patio that fits the space than squeeze in something tidy that looks unfinished from the "
        "kitchen window.",
        "Base depth follows the same frost line as the rest of Bristol County, and with more open ground the "
        "edge restraint gets checked carefully, since a wide field of pavers has more push against the "
        "borders than a small one. Timelines on a big lot usually run a little longer than a compact "
        "Mansfield yard, mostly because of hauling and site room.",
        "Norton also has stretches of new construction where the builder graded the lot and left it, so the lawn and the yard settle unevenly for a year or two. On those lots we like to see how the ground has moved before we set the final height, so the patio does not inherit a dip that shows up the first spring. Windham and the lake side tend to be the flatter ones; the lots off the old roads are the ones that surprise you.",
    ],
    "Foxborough": [
        "Foxborough has a lot of flat ground and a lot of spring water, and a patio here lives or dies on "
        "the base. Flat lots hold water because nothing is pushing it away, so we dig deeper, compact in "
        "lifts and set the slope that sends water out before any stone goes down. If the ground under a "
        "patio stays wet, it does not matter how well the surface was laid; the base softens and the field "
        "moves.",
        "The pattern and the material are the visible half of the job, and Foxborough clients tend to want "
        "a clean line: a straight paver field with a border, or a herringbone laid off the back steps. "
        "Those look best when the setting bed is screeded dead flat, because a clean pattern shows every "
        "high and low paver. The invisible half, drainage and depth, is what keeps the pattern clean years "
        "later.",
        "Frost here behaves like the rest of the 30-inch zone, so a shallow patio that looked fine in July "
        "will show its first lifted paver after one hard freeze and thaw. It is a gradual failure; the "
        "patio never fails all at once, it just stops being level one winter at a time.",
        "Foxborough is also where a lot of the work sits near the stadium and the newer office parks, which means traffic can change the start time of a job on a game day. We plan pours and deliveries around that so a morning start is not stuck behind a line of cars on Route 1. It does not change the work, only the clock.",
    ],
    "Seekonk": [
        "Seekonk runs right up against the RI line and the wet ground that comes with it, so drainage is "
        "the first conversation, not the last. Yards here sit low in stretches and the water table comes up "
        "in spring, which means the base has to be built so it can stay dry even when the ground around it "
        "is not. Walkways and patios here get a base and a slope designed for spring, not for the week of "
        "the install.",
        "Because the ground stays wet longer, edge restraint and compaction get extra attention. A field of "
        "pavers that is not locked at the edges will spread, and on soft spring ground it spreads sooner "
        "than it would on a dry Mansfield lot. We tie the edges in and check the slope so the water leaves "
        "the surface and the base rather than pooling under either one.",
        "Seekonk jobs are usually a day or two out from Mansfield depending on traffic, and we price them "
        "like the rest of the area for a given size and material. What changes the number is how much "
        "drainage work the yard needs first; a yard that already sheds fine is a simpler, faster job than "
        "one where the grade has to be rebuilt before stone goes down.",
        "A lot of Seekonk homes sit on generous lots, so the patio often wants to reach out toward the "
        "yard rather than hug the house. That is fine, but it puts the water question front and center, "
        "because a patio set away from the foundation still has to shed somewhere the ground can take it. "
        "We site it so the runoff heads to a low corner or a dry run of stone instead of sitting in the "
        "middle of the lawn after every storm.",
    ],
    "Rehoboth": [
        "Rehoboth is big-lot country, with long driveways and back yards that open up under a wide sky, and "
        "that scale changes the job. A patio sized for a suburban back yard would get lost here, so the "
        "design starts bigger and the walkway has to actually be worth the walk. Out this way people tend "
        "to want the patio to sit quietly in the land rather than shout, which is usually less about the "
        "stone and more about where the edges and the grade fall.",
        "The ground runs sandy in stretches and holds water in others, sometimes within the same lot, so the "
        "base and the slope get read on site before anything is priced. Sandy ground drains fast and needs "
        "careful compaction and edge restraint to stay put; the wetter pockets are the opposite problem and "
        "need the water routed away. Both are fixable, but only if the yard is actually walked first.",
        "On lots this size the timeline is usually driven by hauling and site access rather than by the "
        "stonework itself. A long driveway is not a problem for getting a job done, but it does add time "
        "moving material in and out, and that shows up in the schedule more than in the price.",
    ],
    "Plainville": [
        "Plainville yards are a mix of newer builds and older homes, and the newer ones often have a grade "
        "that was never really finished once the builder left. We fix the shape of the yard first and then "
        "set the patio to that, rather than laying stone over whatever slope happens to be there. Correcting "
        "the grade before the base goes down is the difference between a patio that drains and one that "
        "collects.",
        "Because the lots are small to medium and close together, access and how the water leaves the "
        "property both matter. A patio here is usually compact and set close to the house, with a walkway "
        "or step that ties the door to the yard cleanly. The neighbors' grades are part of the picture too, "
        "since on tight lots water does not always respect the property line.",
        "Plainville is a short run from Mansfield, so jobs here are quick to get on the schedule. Base "
        "depth follows the same 30-inch frost zone as the towns around it, and the price for a given size "
        "and material lands in the usual range for this part of Bristol County. The variable is how much "
        "grade correction the yard needs first.",
        "Plainville yards are close enough together that a patio here is often built to be looked at from a neighbor's window as much as your own, so the edges and the border get the same care as the field. We set the low point and the fall with the property line in mind, because on lots this tight the water and the view both cross the line whether anyone plans for it or not.",
    ],
    "Taunton": [
        "Taunton runs from tight city lots to roomy yards out toward the lake, and the grade swing between "
        "them is real. On the city lots the patio is compact and the path is narrow, and the whole job is "
        "about making a small space feel finished. Out toward the water the lots open up and take a bigger "
        "field with a walkway laid out properly, and the drainage plan changes with the ground.",
        "Whatever the lot, the patio gets built to shed water away from the house, not toward it. On the "
        "older city lots the grade was often set by eye and the ground has settled unevenly since, so part "
        "of the work is reading what the yard actually does now rather than trusting how it was built. That "
        "gets settled in person, not from a photo.",
        "Taunton is a moderate run from Mansfield and sits in the same frost zone, so base depth and "
        "compaction follow the same rules as everywhere else in the area. Pricing lands in the usual range "
        "for a given size and material; the swing on a job here is usually how much the grade has to be "
        "corrected before the first scoop of dirt can come out.",
        "Taunton has more than its share of homes where an old deck came down and left a bare patch of dirt against the house. That patch is usually the easiest spot to put a patio, but the grade there has often been changed by years of runoff off the roof, so we read where the water actually goes now before setting a height. A walkway out to the drive usually ties that spot back to the rest of the yard.",
    ],
    "Easton": [
        "Easton yards often back onto woods and wetland, so the water table is high in spring and the "
        "ground stays wet longer than it does a few miles east. Retaining walls and patios here are built "
        "with the drainage worked out first, and the wall tied in so it does not creep under wet ground. "
        "When the ground holds water, a wall that is not built to shed it will lean within a few seasons.",
        "Shade is the other thing here. Yards under trees keep their ground cool and damp into summer, "
        "which is good for planting and hard on a patio base if it was not built deep enough to stay dry. "
        "We plan the slope and the base around the shade rather than pretending the lot is a sunny field.",
        "The woods-and-wetland lots also tend to sit further off the road, which is fine for access but "
        "adds a little time to hauling material in. Easton is a short run from Mansfield, and the work "
        "prices in the usual range for the area; what moves the number is drainage and how much the grade "
        "has to be shaped before stone goes down.",
        "Easton also has a lot of stone walls already standing at the property lines, some of them a century old. We match that where it makes sense and leave it where it does not, but a new patio or wall usually reads better when it relates to the old stone rather than fighting it. A short drive down Route 106 from Mansfield means small jobs here can often be worked in without a long wait.",
    ],
    "Sharon": [
        "Sharon is hillier than the towns around it and the yards come with it. Lots off the Moose Hill and "
        "Lake Massapoag sides drop hard enough that flat ground is the exception, so a patio here usually "
        "means steps, a landing and some wall, staying within what the lot allows and graded so it sits "
        "level and still sheds water away from the house.",
        "The stone walls that edge so many Sharon yards are part of the look, and we tie new work into "
        "their lines rather than cutting against them. That is a design job as much as a build job, because "
        "a wall that does not follow the line of the land reads as wrong no matter how well it is built. "
        "Where a yard drops, the wall and the patio get designed together so the transitions look "
        "deliberate.",
        "On sloped ground the base is carrying more than on a flat lot, and the edge restraint is doing more "
        "work, so both get checked carefully. Sharon sits in the same 30-inch frost zone as the rest of the "
        "area. Pricing lands in the usual range for a given size and material; steep lots take longer "
        "because of the steps, the wall and the grade work that comes with them.",
    ],
    "Franklin": [
        "Franklin sits up a little higher than the towns below it, where the frost bites harder and springs "
        "run wet, so depth and compaction decide whether the patio is flat in ten years. This is the town "
        "where the base matters most and where we build it deepest. Wet spring ground plus a freeze is the "
        "combination that punishes shortcuts.",
        "A lot of Franklin yards back onto woods or open field, which means leaves, water and shade all "
        "arrive from the back. Drainage on those lots gets planned with the planting, so the water that "
        "comes off the trees and off the slope has somewhere to land that is not the surface of the patio. "
        "It is easier to shape that with a walkway and a planted edge than to fight it later with sand and "
        "sweeping.",
        "For cost, Franklin jobs sit in the same range as the rest of the area for a given size and "
        "material; what moves the number is depth and how much the grade has to be corrected first. A yard "
        "that needs regrading before a patio goes down is a different job from one that is already close to "
        "level, and the estimate reflects what the ground actually needs.",
        "Franklin also has a run of newer subdivisions out toward the town line where the grade was set by a machine and left flat, which is its own problem: flat ground with nowhere for water to go. On lots like that the first move is often to shape a low point in the yard before the patio height is set, so the whole lot drains to one place on purpose instead of in a dozen small puddles.",
    ],
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
        img="project-dining", img_alt="A stone paver patio in dappled shade, with chairs and planters along the edge.",
        prose=[
            "A patio is sized by how you use the yard, not by the biggest number that fits. A table for six "
            "wants about twelve by twelve of open stone, and the chairs need room to pull back without "
            "falling off an edge. Getting that footprint right is most of what makes a patio feel good, and "
            "it is cheaper to plan the size than to rebuild it later.",
            "The pattern and the stone are the part you choose and the part that changes the price most. "
            "Paver is the friendliest budget and comes in a wide range of colors. Bluestone and flagstone "
            "cost more and age into a look paver cannot match. We lay out the options on the grade, in the "
            "light the yard actually gets, before you commit.",
            "What costs the most is not the stone, it is the site. A yard with a clean slope and a clear path "
            "for material is a different job from one that needs a foot of grade worked out or a tight "
            "backyard access. That is why the estimate comes after a look at the ground, and why two patios "
            "the same size can be different numbers.",
        ],
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
        img="project-walkway", img_alt="Flagstone steps and a low stacked-stone wall rising through a planted bed.",
        prose=[
            "A walkway gets laid out around the path people already take, not the one that looks neatest on "
            "paper. Watch where the grass is worn and that is usually the line. From there the width gets set "
            "by traffic: three feet is the comfortable minimum for one person, closer to four lets two pass "
            "without stepping off.",
            "Because a path sits in the strip where water already travels, the base and the slope do more "
            "work here than on a patio. The trench gets dug to depth, the crushed base goes in and gets "
            "compacted in lifts, and the path is set to drain along its length rather than pond in the middle "
            "of a run.",
            "Steps and landings are where a path either feels easy or feels wrong. A comfortable rise is "
            "under seven inches with a tread deep enough to take a full stride, and landings break up a long "
            "run so it does not read as a ramp. Those get worked out with the layout, not after the stone is "
            "cut.",
        ],
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
        prose=[
            "A retaining wall is a simple machine: it takes the push of wet soil and sends it down into the "
            "ground instead of letting it tip the face. That is why the base course is buried and compacted "
            "before anything else, and why the drainage behind the wall matters as much as the stone you see. "
            "A wall built without them looks fine for a season and then starts to lean.",
            "Height drives everything else. A short garden wall can be stacked on a good base and set back "
            "as it rises. As the wall gets taller, or holds up a driveway or a surcharge, the loads climb "
            "quickly and the design questions grow with them. We will tell you plainly when a wall belongs "
            "with an engineer rather than guess at it.",
            "The finish is where a wall stops feeling like a barrier and starts feeling like part of the "
            "yard. Caps, steps and seat walls built into the same run turn a retaining wall into a place to "
            "sit, and tying the stone to the house means the yard reads as one design instead of a patch of "
            "work against a wall.",
        ],
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
        key="fire-pits", name="Fire Pits", short="fire pits",
        h1="Fire pit installation in {town}, MA",
        meta=("Stone fire pits, seat walls and patio living spaces built in {town}, MA. "
              "Designed into the patio from the start, on a base that does not heave."),
        blurb=("A fire pit is the thing you end up using most, and the thing most often "
               "dropped onto a patio that wasn't planned for it. Building it into the "
               "layout from the start is what makes it feel like part of the yard "
               "instead of an afterthought."),
        img="project-firepit", img_alt="A circular stone fire pit set into a stone patio with seating around it.",
        prose=[
            "The size most people actually enjoy is smaller than they expect. A pit three to four feet across "
            "inside is a comfortable circle for four to six people, and it throws heat you can feel from the "
            "chairs around it. A pit built too big gives you a fire that looks impressive and warms nobody, "
            "because everyone has to sit further back.",
            "Siting is the part that gets skipped and then regretted. The pit wants level ground, clearance "
            "from anything that can catch, and a spot where smoke leaves rather than hangs in the seating "
            "area. Building it into the patio layout from the start settles all of that, and lets the seating "
            "and the grade around it be planned together with the pit.",
            "Wood or gas is the other real choice. Wood is the classic and most people picture it, gas starts "
            "and stops clean. Either way the bowl gets built to last and the stone around it is detailed to "
            "match the patio, so the pit looks like it was always meant to be there.",
        ],
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
        
            "Depth is not a number you can eyeball once the job is done, which is exactly why it is worth pinning down before work starts. In this part of Massachusetts we are planning the dig and the base around a 30-inch frost zone, which is deeper than a lot of people expect. A patio is shallow work in a lot of the country. Here it is not.",
            "You can also think of the base as a sponge and a bridge at once. The crushed stone drains water sideways and down, and compacted in lifts it carries the load of everything on top without shifting. Skip the lifts, and the same stone becomes a loose pile that the pavers float on. The material is not the trick. The compaction is.",
            "The thickness of the base is not a guess; it comes from what the patio will carry and from the soil underneath it. A patio that only takes foot traffic and light furniture needs less than one that will hold a parked car, and a yard on soft fill needs more than one on hard native ground. That is why the same square footage can be a different job from one property to the next, and why a quote without anyone looking at the soil is only a guess.",
            "One more thing worth knowing: good base work is quiet work. There is no part of it that looks impressive in progress, and that is exactly the point. If a crew is racing to get pavers down on the first day, ask what is under them. The depth and the compaction are the whole job. The pavers are the receipt.",
        "A simple way to check a quote is to ask for the depth in inches and the compaction in lifts. A real answer sounds like numbers: so many inches of compacted base, laid in lifts and tamped between each. If the answer is a look and a shrug, the base is a guess. The base is most of the cost and all of the longevity, so it is the one line worth getting in writing.",
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
        
            "There are really four things that keep water moving: the slope of the surface, the pitch built into the base, the joints between the stones, and where everything eventually empties. Get all four pointed the same way and water behaves. Get one pointed backward and you get a puddle that never fully dries.",
            "A lot of drainage work is invisible once it is done, which makes it easy to sell cheaply and hard to check. A swale dressed as planting or a run of drain stone under the lawn does the same job as a fancy system when it is laid out with the fall in mind, and it costs a fraction of what people fear.",
            "Around a house, the number that matters is slope away from the foundation. A patio should fall about an eighth of an inch per foot, or a little more, away from the building and toward a place water can leave. That is gentle enough that furniture and feet never notice it and steep enough that a hard rain moves off the surface instead of standing on it. Flat is not neutral here. Flat is where water sits.",
            "Where the yard has nowhere lower to send water, the fix is often a hidden one: a swale you would not notice, a dry well, or a perforated drain under the stone that carries water around the house and out to daylight. None of that is visible when the job is done, which is why it is worth asking where the water goes before a single paver is set.",
        "One rule covers most yards: water should never be sent toward the house or left to sit against it. The patio should fall away from the foundation, and the ground around it should stay a little lower than the siding. If a downspout dumps right at the patio edge, that is worth moving or extending before the stone goes down, not after the first wet week shows you why.",
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
            "The practical effect for a homeowner is that the dig is deeper than it would be in a warmer state, and the base is built thicker to match. That is also why a patio poured or laid over an existing grade, with no real dig, is a bet against the first hard winter. It can look perfect in July and be a mess by March, and the repair is never as cheap as the first job done right.",
            "Frost heave is not one uniform push, either. It moves where soil and moisture and shade differ across the yard, which is why you see a corner lift or one paver proud of its neighbors rather than the whole patio rising together. Uniform movement you can live with. Uneven movement is what cracks joints and pops edges, and it comes straight from an uneven base.",
        "The practical takeaway is that the base is the insurance policy. You cannot see it when the job is done, and you cannot easily fix it later. A patio dug deep, built up in compacted lifts on a stable subgrade, and edged so the field cannot spread will move as one piece through the freeze and thaw. One that skipped that work will not, and the first hard winter is when you find out.",
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
        
            "Pavers are uniform, so they go down fast and come with a set thickness that keeps the field consistent. That speed is a real part of why they sit at the friendlier end. Bluestone is cut into slabs of varying size, so every piece is set by hand and the layout is a judgement call the whole way through. Flagstone is the most irregular, so the setting time and the cutting climb again.",
            "Texture and color matter more than the brochure suggests. Lighter stone stays cooler underfoot in July sun, and a busier surface hides the small leaf-and-dirt speckle between cleanings. A flat, uniform field shows every bit of dirt and every subtle low spot. Worth thinking about before you commit.",
            "There is also a middle path a lot of jobs land on: pavers for the field you walk and park on, and natural stone for the one detail people actually look at, like steps, a wall cap or a fire pit ring. You get the durability and the price of pavers where the wear is, and the stone look where the eye goes. Mixing is not a compromise; it is usually the smart money.",
            "Whichever stone you pick, one thing does not change: the base under it and the care in the joints. Cheap stone laid well outlasts expensive stone laid badly, every time, because the surface is only carrying what the base is holding. When someone proposes saving money by thinning the base to spend it on fancier stone, that is the trade to push back on.",
        "Ask what the stone is actually called and where it comes from, because the same look can be two very different products. A paver with a solid body and a consistent thickness lays flat and stays flat. A cheap import that varies in size or thickness fights the installer the whole way and shows it in the joints. The name on the pallet matters more than the photo online.",
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
        meta="What a real patio estimate should itemize, and the exact questions to ask any contractor bidding on your yard in Mansfield.",
        lede="A lump-sum price tells you nothing. The useful ones are itemized enough that you know what you're buying.",
        paras=[
            "A useful estimate names the things that decide the job: how much is excavated and hauled away, the base depth in inches, which stone and pattern, edge restraint, a stated drainage plan for your grade, and any steps, seat walls and lighting broken out separately.",
            "It also names when they start and who's on site doing the work. Those two lines tell you a lot about how the job will actually run.",
        
            "A real estimate reads like a short set of decisions, not a single number. What is coming out, how deep the dig goes, how thick the base is, what the stone is, how the edges get held, and where the water goes. If a bid skips all of that, the number is not a price, it is a guess that gets adjusted later.",
            "The other thing a good estimate does is set expectations on time and access. When the dig starts, when the stone lands, how long the yard is unusable, and whether a truck can get close enough to tip stone where it is needed. Access decides a lot of cost in town lots, and it is better to settle it on paper than on the day.",
            "A fair estimate should tell you what you are getting in plain terms: roughly how many square feet, what stone, how deep the dig, whether there is a step or a wall involved, and how long it should take. You should not have to reverse-engineer any of that from a single number. If the whole quote is one line and a total, that is not a sign of confidence; it is a sign that nothing was looked at closely.",
            "It is also reasonable to ask what happens if the job runs into something unexpected, like a hidden stump, a buried footing or a soft spot under the dig. The honest answer is that the price can change, and the trustworthy version of that is a quote that says so up front and tells you how it would be handled. A number that pretends no surprises are possible is the one to be careful with.",
        "Compare quotes on the same scope, not on the total. Two bids only mean something if they cover the same dig, the same base depth, the same stone, and the same cleanup. Ask each crew to break the job into the same parts, then set them side by side. The lowest total on a thinner base is not the cheapest quote, it is a smaller job wearing the same label.",
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
        
            "The questions we hear most are about timing, mess and how bad the yard looks in the middle of the job. The honest answer on all three: a patio project makes a mess in the middle and looks like a building site until the base is done and the stone starts going down. Then it flips fast. The last day or two is where the whole thing reads as finished.",
            "We would rather answer a question you think is too small than have you guess. That includes the ones people feel awkward asking, like whether the price can come down, whether the stone can change after the quote, or what happens if the yard turns out wetter than expected. Ask it up front and it is a conversation. Find out later and it is a problem.",
        "A few come up every single time: how much does a patio cost, how long does it take, and do I need to be home. Cost depends on size, access and the base, so anyone who throws out a firm number without seeing the yard is guessing. Time runs a few days to a couple of weeks for most patios. And no, you do not need to be home, as long as the crew can reach water and power.",
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
    key="paver-cost", tag="07. Cost", title="What a stone patio actually costs",
    h1="What a stone patio costs in Massachusetts",
    meta="A plain-language look at what a stone patio costs in Massachusetts and Rhode Island, and where cheap quotes hide the difference.",
    lede="Nobody likes a vague number, so here is how a patio price is actually built: size first, then what is under it, then how hard it is to get to.",
    paras=[
        "The honest answer on cost is that it depends on four things: how big the patio is, how deep the base has to go, how much the ground has to change to drain, and how hard it is for a machine to reach the work. A flat, open backyard with good access is a different job than a tight side yard you have to wheelbarrow through.",
        "That is why a price per square foot texted before anyone looks at the yard is a guess. Two patios the same size can differ by thousands once digging, drainage and access are counted. When you get a bid, ask what it includes. Dig depth, base thickness, edge restraint, drainage and cleanup should all be named. If a quote is just a number with no breakdown, that is the thing to question.",
        "Here is a rough shape for the area, using paver on a full-depth base. A small patio, say 10 by 12 feet, is the low end. A 16 by 20 foot patio is the middle. Anything with steps, a seat wall or a fire pit is priced as the patio plus the added structure. These are ranges, not quotes, and the only real number comes from walking the yard.",
        "Walls and steps are where budgets move fastest. Every course of a retaining wall adds both stone and labor, and any spot that needs a step instead of a slope adds cutting and a solid footing. A fire pit is a modest add-on by itself, but it needs the same base and clearances as a small patio, so it is never free.",
        "Time is the other half of the number. A simple patio with easy access is usually days, not weeks, from dig to cleanup. Add drainage, steps or a large wall and the calendar stretches. Weather pushes it further, since digging frozen or soaked ground is slower and we do not set stone in a downpour. A build in May and a build in November are not the same job.",
        "It helps to know what actually moves the number up and down. Square footage is the headline, but the grade underneath is the wildcard: a flat, dry yard with easy truck access is the cheap version, and a sloped, wet lot where everything has to be wheeled in by hand is the expensive one. The same patio can swing widely between those two yards.",
        "Material choice is the second lever. A standard paver field is the value play, and moving to bluestone or flagstone is a step up in both material and labor. Adding steps, a seat wall or a fire pit moves the price again. A good itemized quote lets you see which parts you are paying for and choose where to spend.",
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
    img="project-dining", img_alt="A stone paver patio in dappled shade, with planters along the edge.",
),
dict(
    key="patio-vs-concrete", tag="08. Choices", title="Pavers, concrete or stamped concrete",
    h1="Pavers vs concrete vs stamped concrete",
    meta="Paver patio, poured concrete or stamped concrete in Massachusetts: how they differ in cost, cracking, repairs and how they age through a hard winter.",
    lede="All three can make a flat outdoor floor. They behave very differently after a Massachusetts winter, and that is the part worth understanding before you pick.",
    paras=[
        "Poured concrete is one continuous slab. That is its strength and its weakness: when the ground moves under a slab, which it does with our freeze and thaw, the slab cracks, and a crack runs where it wants to. Stamped concrete is the same slab with a pattern pressed into the surface. It looks good on day one and ages with the same slab underneath it.",
        "Pavers are separate units set in a base on purpose. The base is built to move a little without tearing. If one paver settles or cracks, it can be lifted and reset without replacing the whole patio. Concrete cannot be repaired that way. That is the trade: pavers cost more up front and are far easier to fix later.",
    
            "Concrete is one pour and done, which is fast and looks clean on day one. Its weakness is the same as its strength: it is one rigid slab. In a climate that freezes and thaws, that slab cracks along its control joints and sometimes beyond them, and a crack never closes back up. Repairs to a cracked slab are visible by nature.",
            "Pavers are flexible. The joints between them take small movement without cracking, and if a section ever needs to come up for a repair or a utility line, the same stones go back down and read as if nothing happened. That flexibility is the main reason the two surfaces age so differently here.",
        "The practical version for a Massachusetts yard in the 30-inch frost zone: every hard surface freezes and thaws many times each winter. The question is not whether it moves but what happens when it does. A slab resists the movement and then cracks; a paver field absorbs a little at every joint and goes back where it was.",
        "The money half: concrete is lowest up front, stamped concrete climbs from there, and pavers sit above both. The second cost is where it evens out. A cracked slab means break it out and patch it, and the patch never matches. Re-setting pavers is a fraction of that, and the same stones go back down. Over ten or fifteen winters, cheaper stops being cheaper.",
        "There is a place for each. Concrete is fine for a utility slab, a garage apron, or a shed floor. Where the surface is the yard and it has to stay level through frost, a base and a surface that can move is worth the difference on day one.",
        "One more practical point on timing: concrete needs to cure and cannot be walked on for days, while pavers are ready for furniture as soon as the last one is set. If you want to use the space this season and not next, that difference matters as much as the cost. Pavers also let you lift a single unit later to reach a utility line, which a slab never does.",
    ],
    bullets=[
        ("Poured concrete", "lowest up front, cracks as one piece, hard to repair"),
        ("Stamped concrete", "pattern on a slab, same cracking behavior"),
        ("Pavers", "more up front, fixable in sections, forgiving of frost"),
    ],
    img="transform-after", img_alt="A finished paver patio beside a home.",
),
dict(
    key="winter-ready", tag="09. Seasons", title="Patios through a New England winter",
    h1="How to get a patio through a winter",
    meta="Simple, practical steps to keep a paver patio, walkway or retaining wall in good shape through a Massachusetts winter and spring thaw.",
    lede="A patio built right survives winter on its own. The things you do at the edges of the season are what keep it looking new.",
    paras=[
        "The base and the slope are doing the heavy lifting all winter, even under two feet of snow. Your job is small: keep the surface draining, do not carve it up with a steel blade, and watch the low corners when the thaw comes. Water that has somewhere to go does no damage. Water that pools and freezes is what moves things.",
        "The single most common winter mistake is scraping a paver surface with a steel snow shovel or a metal-edged plow. That scratches the finish and can catch a joint. A plastic shovel or a rubber-edged blade from the house out is plenty. Spread sand or a pet-safe melt rather than rock salt, and do not chip ice off with a bar. Come spring, a quick look at the edges and joints tells you everything is fine, and a small sweep of sand back into the joints finishes the job.",
        "Preparing a patio for winter is mostly about keeping water off it before the first hard freeze. Clear the leaves and dirt that trap moisture, make sure the surface still drains, and do not pile snow against the house or leave the plow to drag steel across the stone. Small habits decide whether spring reveals the same surface you built.",
        "What you should not do is panic about frost. A patio built to depth over a compacted base is designed for the cycles that come every year. The jobs that suffer are the ones built shallow, and nothing you do in December will fix a base that was wrong in June.",
        "Two habits do most of the work. Keep the surface clear of leaves and debris so water can find the low point, and keep the joints full of sand so the pavers stay locked. A washed-out joint is easiest to top up in the fall and hardest to fix once frost has lifted the paver.",
        "Tell the plow service the surface is pavers, and keep the blade an inch up with skid shoes on. One season of steel dragging across the surface does more damage than ten winters would. A little care in the two months of plowing protects twenty years of patio.",
        "The best time to fix a winter problem is the fall before it happens. Walk the patio after a hard rain and see where water lingers; that low spot is where frost will do its first work. A bag of sand in October to top up the joints and a few minutes clearing the drains does more for the surface than anything you can do in January, when the ground is locked up and there is nothing useful left to do.",
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
        "Ask what happens to the water. That single question does the most work. A real answer mentions slope, the direction of the grade, and where the runoff ends up. A vague answer means nobody has looked at the grade, and a patio that ignores the grade will always be fighting it.",
        "With a one-man operation the person who quotes the job is the person who builds it. That removes the mismatch you run into with bigger companies, where a salesperson measures the yard and a different crew shows up weeks later with half the story. Whoever walks your yard should be the one holding the shovel.",
        "Then ask for it in writing and compare bids line for line: depth, base, compaction, edge material, drainage, cleanup. A crew that is confident in the work puts numbers to those things without being asked twice. A crew that is not stays vague and leans on the price.",
        "A written bid is the contract, and a few lines decide how the patio ages: how deep the base goes, how it is compacted in lifts, where the edge restraint lands, and where the water drains. A rushed quote leaves those out and talks about the stone instead. If two bids are far apart, the difference is almost always what is under the pavers, not on top of them.",
        "Ask how long the job takes and who will actually be there. A one-man, owner-operated crew is on the shovel, so the answer is honest. Perfect price plus a sliding schedule is the bid you did not want. Good work takes the time it takes, and the person who quoted it should still be there at the last paver.",
        "Call at least one past customer and ask one specific question: how did it hold through two winters, or did anything get left unfinished. A vague answer tells you more than a glowing one. The best crews are small, local, and checkable, which is exactly why the references are worth the two minutes.",
        "One last tell is how they handle the yard while they work. A good crew keeps the excavated soil in one place, protects the lawn it has to cross, and leaves the site swept at the end of each day. A messy job is not just annoying; it usually means the same care is missing under the stone, where you cannot see it.",
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
        "An apron is the strip where a walk or driveway meets the road, and it takes more punishment than any other part of the run. Cars turn across it, the plow drags over it in winter and water from the street runs toward it. That is why it is worth digging and base-building even more carefully than the rest of the path.",
        "Steps are the other place detail pays off. Each tread wants a slight fall so water leaves the landing instead of standing on it, and the risers want to be consistent so the run feels steady underfoot. Small things, and they are the difference between a walk that feels finished and one that feels almost.",
        "The transition is the detail that is easiest to get wrong. A hard lip or step where the apron meets the road or the garage is where water and the plow find it. A short ramp built on its own compacted base and cut to shed water is the difference between a decade of service and a crack in the first winter.",
        "Heavy loads change the base. A walkway carries feet, but an apron carries a car or a truck, so the base is dug deeper and compacted harder. If a plow or a delivery truck crosses it, say so up front. That changes the build, not just the price.",
        "Salt is the second thing to think about, because it is hard on both concrete and pavers and worse on a surface that already takes plow abuse. Sand or a paver-safe de-icer does less damage than rock salt over a season. On an apron that sees the road plow, that one choice is the difference between a surface that still looks new after five winters and one that is chipping at the edges.",
    ],
    bullets=[
        ("Steps", "risers stay even, treads stay level, edges get restraint"),
        ("Walkways", "slope away from the house, base as deep as a patio"),
        ("Aprons", "built for plow and traffic, water sent clear"),
    ],
    img="project-walkway", img_alt="Flagstone steps and a stacked-stone wall in a planted bed.",
),
dict(
    key="fire-pit-basics", tag="13. Fire pits", title="Fire pits that last",
    h1="Fire pits: what makes one last",
    meta="How a fire pit is built in Massachusetts, what makes one last and what makes one crack, and the two choices to settle before you dig: wood or gas, and where it sits.",
    lede="A fire pit looks simple: a ring, some stone, a fire inside. What decides whether it still looks right after five winters happens in the ground under it.",
    paras=[
        "A fire pit is a small retaining wall shaped like a circle, and it fails the same way a wall fails. Water gets under the base, freezes, and lifts a course. A pit set on bare ground, or on a base that was not dug and compacted, will show the first lifted ring after one hard frost. The ring above ground is the visible part. The footing under it is the work.",
        "The first choice is wood or gas. Wood is cheap to run and you get the crackle, but you deal with ash, smoke on a still night, and cleaning it out. Gas lights with a switch and burns clean with no ash, but it costs more up front and needs a line run and a place for the burner. Neither is better; they are different jobs. Pick yours before the pit is built, because a gas pit needs the burner and the line planned into the build, not added later.",
        "Then the ring. A kit of stacked blocks is fast and repeatable. A mortared block pit with a seat wall attached looks more built-in and can double as seating. A dry-stacked natural stone ring reads more rustic and drains through the gaps. All three can last if they are footed right; the material is not the trick. Ask where the seat wall ties in and how water leaves the base.",
        "Where the pit sits is the part people rush. Keep it clear of the house, the deck, and anything with an overhang, and check the local setback rules before you dig, because they vary town to town. It wants to sit on flat ground, not on a slope, and not in the low corner where water collects. A pit that sits in the yard's wet spot will fight its footing every winter.",
        "A fire pit wants a base that drains. Crushed stone under and around the ring, dug below the frost line and compacted, keeps water moving instead of pooling against the block. Some rings get a wet-set bed and some are dry-set to let water pass through. Which one belongs on your site depends on the grade and the soil, and that is a call to make on the ground, not over the phone.",
        "Two small details separate a pit that gets used from one that does not. A smooth, level seat wall at the right height is what makes people stay out there on a cool night. And a safe clear zone of stone or gravel around the ring keeps the fire off grass and mulch, which is both a safety and a looks decision. Neither one is expensive. Both are easy to leave out.",
        "Expect the pit to change with the season. Wood ash and moisture are hard on the block over time, and a cover or a clean-out in the fall saves a lot of scrubbing come spring. A gas pit wants the burner and the line checked before the first cold night. Five minutes a year is the difference between a pit that reads as new and one that reads as neglected.",
        "If you are weighing a fire pit against a patio, they usually belong together. The pit is the reason people sit outside after dark, and the patio is where the chairs go. Build the pit into the patio layout from the start and the whole thing reads as one space instead of two. Add it later and you are cutting into a finished surface.",
    ],
    bullets=[
        ("Wood or gas", "pick before the build; a gas pit needs the line planned in"),
        ("Ring type", "kit, mortared seat wall, or dry-stacked stone"),
        ("Footing", "dug below frost, crushed stone, compacted, drains"),
        ("Placement", "flat ground, clear of overhangs, check local setback"),
    ],
    checklist=[
        "Decide wood or gas before the pit is built",
        "Keep it clear of the house, deck and any overhang",
        "Check the local setback rule in your town",
        "Foot it below frost on compacted, draining stone",
    ],
    note=("<strong>Easiest thing to get right:</strong> put the pit on flat ground you already "
          "know drains well, and it will outlast one set in the yard's low spot."),
    img="project-firepit", img_alt="A stone fire pit ring set into a paver patio with seating around it.",
),
dict(
    key="yard-grades", tag="12. Drainage", title="Where does your yard drain?",
    h1="How to read the water in your own yard",
    meta="A simple way for homeowners to watch water move across their yard after rain, and why that matters before any patio, walkway or wall project.",
    lede="Before anyone talks stone, walk your yard after a real rain. Where the water goes tells you more than any plan.",
    paras=[
        "Put on boots after the next heavy rain and walk the property. Look for the low spots, the puddle that takes a day to leave, the streak where water crosses the lawn, and the corner against the house that stays wet. You are not diagnosing anything, you are just watching. Water always takes the easiest path downhill, and that path is the same path a new patio has to work with, not against.",
        "Write down where it goes and take a few pictures. When Bryce estimates the job, those pictures answer half the questions before he arrives. If a yard has nowhere to send water, the plan has to make somewhere. If it already drains well, the build just has to respect it. Knowing which one you have puts you ahead of most homeowners before the first bid.",
        "Before any design, walk the yard after a real rain and watch where the water goes. The low spots, the way the ground falls toward or away from the house, and the direction it leaves the lot are all free information you can use before anyone quotes a project. That read often decides where a patio can sit and how high it should be.",
        "On a lot where water has nowhere obvious to go, a shallow swale or a dry run of drain stone can carry it to a better low point without a big system. Dressed with planting so it reads as part of the yard, it handles the worst storms quietly and keeps the patio surface dry, which is the whole point.",
        "The common mistake is picking the patio shape first and fitting the water in later. Read the grade, decide where the water ends up, then draw the patio. A layout that fights the fall needs soil moved in or out, and that turns a simple job silently expensive.",
        "If there is nowhere for the water to go, there is almost always a non-engineered answer: a shallow swale dressed as a planting bed, a dry run of drain stone to a low corner, or a small catch basin at the one low point. None of it is exotic, and all of it is cheaper than a soggy patio.",
        "Think about the whole yard, not just the patio. Water that leaves the patio has to go somewhere, and if the grade sends it back toward the house or pools against the foundation, the patio solved nothing. The good layouts send water away from the building and out to a low corner or the street, so the patio and the yard work together instead of against each other.",
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
<meta name="theme-color" content="#F7F4EE" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14171A" media="(prefers-color-scheme: dark)">
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
<link rel="icon" href="{BASE}/assets/img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="{BASE}/assets/img/favicon-32.png" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2314171A'/%3E%3Cg fill='%23F7F4EE'%3E%3Crect x='4' y='5' width='14' height='10' rx='1.6'/%3E%3Crect x='20' y='5' width='8' height='10' rx='1.6'/%3E%3Crect x='4' y='17' width='8' height='10' rx='1.6'/%3E%3Crect x='14' y='17' width='14' height='10' rx='1.6'/%3E%3C/g%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{BASE}/assets/img/apple-touch-icon.png">
<link rel="manifest" href="{BASE}/site.webmanifest">
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
      <p class="footer__fine">Photographs on this site are AI-generated renderings, not photos of finished Bryce\u2019s Patios jobs. They show the kind of work Bryce builds, until real job photos replace them.</p>
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
    "fire-pit-basics": ["materials", "patio-base", "winter-ready"],
}

# ── FAQ sets for the pages that never had them (WS8 depth) ─────────────────
# Google requires the visible <details class="qa"> block to match the FAQPage
# schema exactly, so both come from the same list. {town} is formatted per town.
FAQS_TOWN = [
    ("How much does a patio cost in {town}?",
     "It depends on square footage, the stone you pick and how much site work the grade needs. Paver is the friendliest budget, bluestone and flagstone climb from there. You get an itemized number after Bryce sees the yard, and the estimate is free."),
    ("Do I need a permit for patio work in {town}?",
     "Most patios and walkways under a certain size don't need one, but the line moves from town to town and some lots sit in a wetland buffer. Tell us the address when you call and we'll say which side your property falls on before anything is dug."),
    ("How far out does Bryce work from {town}?",
     "There are no hard limits. {town} is well inside the regular run from the Mansfield yard, so it's a normal job. Anything further out just needs a call first so the drive makes sense for both sides."),
]

FAQS_GUIDE = [
    ("Is this true for every yard, or does it change with the grade?",
     "Every yard is a little different, so treat this as the way the work should go rather than a fixed recipe. The grade, the soil and where the water wants to run all move the details. That is exactly what Bryce looks at before quoting."),
    ("Can I get a plain answer on my own yard?",
     "Yes. Call Bryce or text a couple of photos with the rough size and the grade. He will tell you what the job actually needs and whether a visit is worth it, with no sales script."),
    ("Does this apply anywhere in Massachusetts and Rhode Island?",
     "The base depth and frost rules here are built for this part of Massachusetts, and the same standard carries into Rhode Island work. Towns next to Mansfield are the usual run, but there are no hard limits on how far out the job goes."),
]

FAQS_HUB = {
    "learn": [
        ("I have never hired a patio contractor. Where do I start?",
         "Read the base guide first, because most of a patio is underground and the base is what separates a quote that holds up from one that does not. From there the drainage and frost guides explain why patios sink and walls lean, and the cost guide breaks down what moves a price."),
        ("Do I need to understand all of this before I call?",
         "No. The guides are here so you can tell a real quote from a thin one. If you would rather just talk it through, call Bryce and describe the yard. He will tell you what he needs to see and give you a straight answer."),
        ("Are these guides just sales material?",
         "No. They explain the work in plain words, including the parts that cost more. The point is that you can ask better questions of any contractor you talk to, not just Bryce."),
    ],
    "services": [
        ("How do I know which service my yard needs?",
         "Describe what the yard is doing, not what you think you want. If water sits, that points to drainage and base depth. If the ground drops away from the house, that points to steps, landings and a wall. Bryce will name the right job after seeing it."),
        ("Can you do more than one of these on one job?",
         "Usually yes, and it is cheaper to design them together. A patio, a walkway, a wall and a fire pit share the same base, the same drainage and the same hauling, so doing them as one plan avoids digging the yard twice."),
        ("Do you give prices over the phone?",
         "Prices here are per job, not per square foot, because two patios the same size can be different work. Send a couple of photos with the size and the grade and you will get a straight answer on whether a visit is worth it."),
    ],
    "areas": [
        ("Is my town actually inside the service area?",
         "Mansfield is home base and the twelve Massachusetts towns listed are the ones Bryce is in most weeks. Rhode Island is a short drive over the line and is on the list too, just call first to sort out what your town requires."),
        ("Does the work change from town to town?",
         "The crew and the standard do not change, the ground does. Flat yards get drainage designed into the patio; sloped or ledge lots turn into steps, landings and walls; wet spring yards get base depth and drainage worked out before anything is dug."),
        ("What if my town is not on the list?",
         "That does not mean no. There are no hard limits on how far out the work goes. Call with the address and Bryce will tell you straight whether it makes sense for both sides."),
    ],
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
    "fire-pit-basics": "fire-pits",
}
