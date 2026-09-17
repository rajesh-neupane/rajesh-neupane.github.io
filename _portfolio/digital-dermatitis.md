---
title: "Spotting Hoof Lesions with YOLOv11"
excerpt: "On-farm hoof photos → detect + stage digital dermatitis. Two-stage YOLO pipeline, vet-adjudicated labels.<br/><img src='/images/dd-detection-pred.jpg'>"
collection: portfolio
---

**TL;DR:** Two-stage computer vision pipeline for digital dermatitis: YOLO detection (hoof localization → lesion detection) followed by staged classification (M0/M1/M2/M3/M4). Benchmarked ResNet-50, EfficientNet-B0, ViT-B/16, and five YOLO11-CLS variants against specialist-adjudicated ground truth.

![YOLO lesion-detection predictions on validation hooves](/images/dd-detection-pred.jpg)

## Problem
Digital dermatitis is a top cause of lameness — but staging lesions still means an expert eye on every hoof in the trimming chute. That's slow, subjective, and impossible to scale.

## What I did
*   Built a curated on-farm dataset with specialist-adjudicated lesion stages and bounding boxes
*   **Stage 1 — detection:** YOLO hoof localization → lesion detection (predictions above)
*   **Stage 2 — classification:** head-to-head benchmark — ResNet-50, EfficientNet-B0, ViT-B/16, YOLO11n/s/m/l/x-CLS
*   Reported macro precision / recall / F1 + ROC-AUC with 95% CIs; best staged classifier **ViT-B/16 (macro F1 0.69, ROC-AUC 0.84)**, ResNet-50 ROC-AUC 0.90

![Normalized confusion matrix, staged classification](/images/dd-confusion-matrix.png)

## Result
A feasibility-grade pipeline showing which architectures actually separate tricky early-stage (M1) lesions — now the blueprint for field validation. Presented at EAAP 2025; manuscript in revision.

**Stack:** Python, PyTorch, Ultralytics YOLOv11
