---
title: "Why Do Milking Robots Fail?"
excerpt: "715K Lely records + DairyComp → which cows fail, when, and what it costs. Published in J. Dairy Sci.<br/><img src='/images/failed-milking-flow.png'>"
collection: portfolio
---

**TL;DR:** Characterized failed milking events in a voluntary (robotic) milking system — harmonizing 715K Lely rows across 2,153 cows with DairyComp management records into a 614K-row analysis set. Rate-ratio + negative-binomial modeling of when failures spike. Published in the *Journal of Dairy Science* 2026.

![Lely + DairyComp harmonization pipeline](/images/failed-milking-flow.png)

## Problem
Failed milkings stress cows, waste robot capacity, and distort yield records — but nobody had quantified *which* cows fail, *when*, and how management events drive it.

## What I did
*   **Harmonized two messy streams** — Lely telemetry (715K rows) + DairyComp (165K rows, 12K cows + events) → 613 cows / 614K rows joined on cow ID + event windows
*   **Modeled failure rates** — rate ratios by parity / stage / season, truncated negative-binomial validation, odds-ratio checks
*   **Tied failures to welfare + management** — pen moves, parity, and time patterns that managers can actually act on

![Failed milkings by week — where the spikes live](/images/failed-milking-weeks.png)

## Result
First systematic picture of robot-milking failures and their management levers — peer-reviewed in JDS, presented at ADSA. Directly informs robot settings and pen-management decisions.

**Stack:** R, Python, SQL · **Proof:** [J. Dairy Sci. 2026](/publications/) · ADSA oral presentation
