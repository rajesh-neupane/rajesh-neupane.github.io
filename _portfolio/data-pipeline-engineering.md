---
title: "One Pipeline for 4 Messy Sensor Streams"
excerpt: "Milking + rumen + accelerometer + barn data → one clean, ML-ready dataset. 10x less wrangling.<br/><img src='/images/data-pipeline.png'>"
collection: portfolio
---

**TL;DR:** Built a unified ETL that merges milking meters, rumen sensors, accelerometers, and barn loggers by timestamp + ID into ML-ready tables.

## Problem
Every analysis started with weeks of manual merging and outlier-chasing.

## What I did
*   Auto-merge on timestamps + animal IDs across 4 heterogeneous sources
*   Robust cleaning for missing values and sensor outliers
*   Standardized outputs ready for stats or ML

## Result
Cut preprocessing time dramatically — more modeling, less wrangling.

**Stack:** Python, SQL, Pandas
