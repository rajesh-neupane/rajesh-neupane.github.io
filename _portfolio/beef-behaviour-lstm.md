---
title: "Cow Behavior Classifier: LSTM vs Transformers"
excerpt: "High-frequency accelerometer → RNN / LSTM / Transformer shootout for behavior monitoring.<br/><img src='/images/beef-behaviour.png'>"
collection: portfolio
---

**TL;DR:** Benchmarked RNN, LSTM, BiLSTM, and Transformers on granular accelerometer data to classify beef-cow behaviors in commercial settings.

## Problem
Noisy, high-frequency sensor data — which architecture actually holds up on-farm?

## What I did
*   Denoised signals (low-pass filters, aggregation) for commercial + research herds
*   Head-to-head test: RNN vs LSTM vs BiLSTM vs Transformers
*   Evaluated for precision-livestock deployment, not just accuracy

## Result
Clear playbook for which time-series model to use for real-time behavior monitoring.

**Stack:** Python, PyTorch, TensorFlow
