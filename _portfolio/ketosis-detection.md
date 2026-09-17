---
title: "Catching Ketosis Before It Costs Milk"
excerpt: "Breath acetone + rumen bolus + milk data → early ketosis flags, validated against blood BHB.<br/><img src='/images/ketosis-correlation.png'>"
collection: portfolio
---

**TL;DR:** Fused breath-acetone readings, Smaxtec rumen-bolus telemetry, AfiMilk records, and DHI milk data to flag ketosis early — validated against serum BHB ground truth with mixed-effects modeling. Includes an Arduino-based breath-sampling prototype.

![Correlation structure across ketosis indicators](/images/ketosis-correlation.png)

## Problem
Ketosis drains milk and fertility in early lactation, but blood testing every fresh cow is impractical — subclinical cases slip through until production already drops.

## What I did
*   Merged 4 streams by cow + date: breath acetone (ppm), milk BHB, rumen-bolus (Smaxtec), AfiMilk + DHI milk records, serum BHB as ground truth
*   Fit linear mixed models (`milk BHB ~ breath acetone + (1|cow)`) with marginal/conditional R² and cow-level validation
*   Built an Arduino breath-sampling prototype for chute-side collection

## Result
Non-invasive ketosis screening vets can run without needles — breath + milk signals that track blood BHB, packaged as a repeatable on-farm protocol.

**Stack:** Python, R (lme4), pandas, Arduino
