---
title: "From Raw Accelerometer to Behavior Labels"
excerpt: "End-to-end pipeline: raw wearables → features → XGBoost / RF / LSTM / Transformers, validated cow-by-cow.<br/><img src='/images/accel-workflow.png'>"
collection: portfolio
---

**TL;DR:** Production-style pipeline that turns raw dairy accelerometer files into behavior predictions — modular data I/O, feature engineering, and a model zoo (XGBoost, Random Forest, LSTM, RNN, Transformers) with Optuna tuning and leave-one-subject-out validation.

![End-to-end smart-dairy accelerometer workflow](/images/accel-workflow.png)

## Problem
Every new accelerometer study started from scratch: custom file readers, one-off features, models evaluated on random splits that leak across cows — and collapse on new animals.

## What I did
*   **Modular pipeline** — `data_io` → `feature_pipeline` → `experiment_engine`: reusable from notebook to SLURM
*   **Model zoo shootout** — XGBoost / Random Forest vs LSTM / RNN / Transformers across window lengths and feature sets
*   **Honest validation** — leave-one-subject-out + Optuna tuning, so scores reflect new-cow performance

## Result
Drop-in codebase the lab now reuses across lameness, heat-stress, and behavior projects — plus a clear answer on when deep sequence models beat gradient boosting for barn wearables.

**Stack:** Python, PyTorch, scikit-learn, XGBoost, Optuna · **Code:** [rajeshneupane7/accelrometer_codes](https://github.com/rajeshneupane7/accelrometer_codes)
