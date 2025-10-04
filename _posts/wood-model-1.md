title: 'wood modeling of lactation curve'
date: 2025-10-04
permalink: /posts/wood-modeling/
tags:
  - dairy
  - modeling
  - cows
---

# Tutorial: Simulating and Fitting Lactation Curves with the Wood Model

## 1. Introduction
The lactation curve of a dairy cow represents the daily milk yield (DMY) over the course of lactation. A well-known parametric model for describing this curve is the **Wood model** (Wood, 1967), which captures the rise, peak, and gradual decline of milk yield.  

This tutorial demonstrates how to simulate lactation data, fit the Wood model using Python, and extract key performance metrics such as **peak yield**, **peak lactation time**, and **persistency**.

---

## 2. The Wood Model

The Wood model is expressed as:

\[
σ_t = a \cdot t^b \cdot e^{-ct}
\]

Where:
- \(σ_t\) = DMY (kg/day) at lactation day \(t\)  
- \(a\) = scaling factor (initial yield)  
- \(b\) = growth parameter (rate to peak)  
- \(c\) = decline parameter (post-peak)  

---

### 2.1 Derived Metrics
From the fitted parameters, we can compute important lactation traits:

- **Peak Lactation Time**  
\[
t_{peak} = \frac{b}{c}
\]

- **Peak Yield**  
\[
σ_{max} = a \cdot \left(\frac{b}{c}\right)^b \cdot e^{-b}
\]

- **Persistency (P)**  
\[
P = \frac{σ(t_{peak}+30)}{σ(t_{peak})} \times 100\%
\]  

Typical persistency values are 94–96%, meaning a 4–6% monthly decline.

---

## 3. Implementation in Python

We use the [`lmfit`](https://lmfit.github.io/lmfit-py/) package for nonlinear regression.

```python
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model

# Define Wood model function
def wood_model(t, a, b, c):
    return a * (t**b) * np.exp(-c*t)

# Simulate lactation data
np.random.seed(42)
days = np.arange(1, 305)  # 305-day lactation
true_params = dict(a=20, b=0.2, c=0.003)
milk_yield = wood_model(days, **true_params) + np.random.normal(0, 1, size=len(days))

# Fit model
model = Model(wood_model)
params = model.make_params(a=15, b=0.1, c=0.001)  # initial guesses
result = model.fit(milk_yield, params, t=days)

print(result.fit_report())

```
