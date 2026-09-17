---
title: "Early Lameness Alerts from Cow Wearables"
excerpt: "Accelerometer → ML that flags lame cows early. Clinically validated, published in PLOS ONE.<br/><img src='/images/lameness-prediction.png'>"
collection: portfolio
---

**TL;DR:** Built Random Forest / SVM / gradient-boosting models on locomotion accelerometer data to predict lameness before visual signs. Validated against vet diagnoses. Published in *PLOS ONE 2024*.

## Problem
Lameness costs ~$300+ per case and hurts welfare — but visual scoring is slow and subjective.

## What I did
*   Cleaned commercial accelerometer streams (filtering, feature engineering on gait/activity)
*   Compared RF, SVM, and boosting; tuned for sensitivity/specificity + ROC
*   Validated against clinical ground truth, not just cross-val splits

## Result
Early-detection model vets can trust → paper + framework reused for mastitis & heat-stress work.

**Stack:** Python, scikit-learn, R · **Proof:** [PLOS ONE paper](/publications/)
