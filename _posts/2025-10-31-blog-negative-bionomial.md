---
title: 'Negative Bionomial Modeling'
date: 2025-10-31
permalink: /posts/nb/
tags:
  - dairy
  - modeling
  - cows
---

Tuitorial : Negative Bionomial modeling

# Modeling Failed Milkings Using a Truncated Negative Binomial Model in R  

## 📘 Introduction  

In precision dairy management, robotic milking systems generate a wealth of data — from milk yield and milking frequency to failure events. One interesting application of statistical modeling in this context is **estimating the pattern of failed milkings over time**.  

Failures in robotic milking (for instance, when a robot fails to attach correctly or a cow refuses milking) are **count data**, often **overdispersed** (variance greater than the mean) and **truncated** (e.g., robots can’t have negative failures, and sometimes zero failures aren’t recorded).  

The **Truncated Negative Binomial (TNB)** model provides a powerful way to model such data, accounting for both overdispersion and truncation.  

---

## 🐄 Use Case: Failed Milkings per Week  

Let’s imagine a scenario where we want to analyze **the number of failed milkings per week** for a specific cow being milked by a particular robot.  

For example:  
- We have 10 weeks of data for Cow #124.  
- Each week, the robot records the number of failed milkings.  
- Occasionally, data with zero failures is not logged (a typical truncation case).  

To demonstrate this, we’ll **simulate** such data using **Monte Carlo simulation** in R.  

---

## 🔢 Step 1: Simulating Failed Milking Data  

We’ll assume that the underlying process follows a **negative binomial distribution**, but that we only observe values **greater than zero** (i.e., truncated at 0).

```r
# Load required libraries
library(VGAM)     # for truncated negative binomial
library(dplyr)
library(ggplot2)

set.seed(123)

# Parameters
N_WEEKS <- 1000          # number of simulated weeks
MU <- 2.5                # mean failed milkings
SIZE <- 1.5              # dispersion parameter

# Generate negative binomial data
failures <- rnbinom(N_WEEKS, size = SIZE, mu = MU)

# Apply truncation (remove zeros)
failures_trunc <- failures[failures > 0]

# Visualize
df <- data.frame(Failures = failures_trunc)
ggplot(df, aes(x = Failures)) +
  geom_histogram(binwidth = 1, fill = "#69b3a2", color = "white") +
  theme_minimal() +
  labs(title = "Simulated Failed Milkings (Truncated at 0)",
       x = "Number of Failed Milkings per Week",
       y = "Frequency")
```

![Histogram of Failed Milkings](/images/nb_image.png)

## Step 2 Fitting the  truncated Negative binomial model

We have not fiitted any  explanatory variables here so, we will get  only estimated mean and dispersion parameter under trancation form this
```r
# Fit the model
nb <- glmmTMB(
  Failures ~ 1,
  family = truncated_nbinom2,
  data = df
)
summary(nb)
```

when we examine the summary: we get 
!['summary nb model'](/images/summary_nb.png)



## Model Evaluation

Here, we can see the **dispersion parameter**:

$$
d = 1.36
$$

which is very close to the value we used to generate the data:  
`size = 1.5`

---

We also obtained the **model intercept**, which represents the modeled mean (on the log scale):

$$
\text{Intercept} = 0.88
$$

Exponentiating this intercept gives us the modeled mean number of failures per week (as fitted to generate the simulation):

$$
\mu = e^{0.88} = 2.43
$$

---

✅ **Conclusion:**  
The fitted truncated negative binomial model successfully recovered the underlying parameters (mean ≈ 2.5 and dispersion ≈ 1.5) used to simulate the data.

| Parameter         | True (Simulated)   | Estimated         | Comment      |
| ----------------- | ------------------ | ----------------- | ------------ |
| Mean (μ)          | 2.5                | 2.43              | Very close ✅ |
| Dispersion (size) | 1.5                | 1.36              | Very close ✅ |
| Model family      | Truncated NB       | Correctly chosen  | ✅            |
| Residuals         | (check via DHARMa) | Should be uniform | ✅            |


## Model Validation Using Simulated Residuals

Now we can move a little bit further to **validate our model** by examining the residuals using the `DHARMa` package in R.

```r
library(DHARMa)
res <- simulateResiduals(model_tnb)
plot(res)
```

---

### Why Use Simulated Residuals?

In traditional linear regression, residuals (the difference between observed and predicted values) are expected to be normally distributed with constant variance.  
However, this assumption **breaks down for non-Gaussian models**, such as Poisson, negative binomial, or truncated distributions.  
In these cases, raw residuals can be misleading because they:
- Are not normally distributed,
- Depend on the fitted mean–variance relationship,
- Cannot easily be compared across observations.

---

### The Advantage of Simulated Residuals (DHARMa)

The **`DHARMa`** package overcomes these limitations by generating **simulated (standardized) residuals** through a Monte Carlo process:

1. It **simulates new response values** from the fitted model many times.  
2. For each observed value, it computes the **proportion of simulated values** that are smaller.  
3. These proportions are then **converted to a uniform (0–1)** distribution.

If the model is correctly specified, the simulated residuals should follow a **uniform distribution**.  
Any systematic deviation from uniformity (for example, clustering, skewness, or trends with predictors) indicates a **model misfit**.

---

### Benefits Over Traditional Residuals

| Aspect | Traditional Residuals | Simulated Residuals (DHARMa) |
|--------|-----------------------|-------------------------------|
| Distribution assumption | Normal errors | Distribution-free (uniform expected) |
| Works with | Linear models | Any GLM or GLMM (e.g., Poisson, NB, truncated) |
| Detects overdispersion | Indirectly | Direct tests available |
| Zero-inflation detection | Difficult | Built-in diagnostic tests |
| Interpretability | Model-dependent | Standardized and comparable |

---

✅ **In summary:**  
Using simulated residuals allows for a more robust and interpretable diagnostic check, especially when dealing with **count data**, **non-normal error structures**, or **truncated distributions** like our truncated negative binomial model.

!['Residual nb'](/images/residual_nb.png)

@misc{neupane2025,
  title        = {Using Truncated Negative Binomial Models for Analyzing Failed Milkings in Dairy Robots: A Monte Carlo Simulation Approach},
  author       = {Neupane, Rajesh},
  year         = {2025},
  howpublished = {Rajesh neupane Blog},
  url          = {https://rajesh-neupane.github.io/}
}