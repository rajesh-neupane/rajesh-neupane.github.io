---
title: ' Non-Parametric Test with Example'
date: 2025-11-01
permalink: /posts/non-parametric/
tags:
  - dairy
  - modeling
  - non-parametric
---

Non-parametric statistics can be thought of as a set of statistical models that minimize two things:
1. The number of assumptions.
2. The strength of these assumptions.

For example, parametric tests like the t-test require assumptions such as:
- The data is normally distributed.
- There is enough data to rely on the Central Limit Theorem.

The results of parametric tests are accurate only if these assumptions are met. Non-parametric tests, on the other hand, have relaxed assumptions, making them more robust in certain scenarios.

## Basis of Null Hypothesis Significance Testing
Before diving into non-parametric tests, it is important to understand the framework of hypothesis testing:
1. Test assumptions.
2. Parameters of interest.
3. Null hypothesis.
4. Test statistic.
5. Null distribution.

## Example: One-Sample Non-Parametric Test
Imagine we have data on the lying time of cows in a day. The typical lying time is around 12 hours. For 10 cows, the data is:

`[12, 11, 8, 7, 10, 12, 13, 5, 12, 16]`

Some cows have lying times as low as 5-6 hours, which seem like outliers. However, we cannot remove them as they are important for our analysis. We want to test the null hypothesis:

**H₀: The typical lying time is around 12 hours.**

The traditional t-test is not suitable here because:
1. The data is not normally distributed.
2. The sample size is small, so the Central Limit Theorem may not apply.

### Wilcoxon's Signed Rank Test
The Wilcoxon Signed Rank Test is a non-parametric alternative to the t-test. It tests whether the center of a distribution differs from a specified value.

#### Test Assumptions
- The sample size \( n \) comes from some cumulative distribution function (CDF):
  $$ (X_1, \dots, X_n) \sim F $$
- The distribution is continuous and symmetric.
- The parameter of interest is the center of the distribution, \( \theta \).

Each observation can be written as:
$$ X_i = \theta + \epsilon_i $$
where \( \theta \) is the center of the distribution and \( \epsilon_i \) represents noise. This assumes a symmetric distribution, like the t-distribution.

#### Null Hypothesis
The null hypothesis is:
$$ H_0: \theta = \theta_0 $$
This is analogous to the t-test, where we test:
$$ H_0: \mu = \mu_0 $$

#### Test Statistic
The test statistic is calculated as:
$$
T = \sum_{i=1}^n \text{sign}(Y_i) \cdot R(|Y_i|)
$$
where:
- \( Y_i = X_i - \theta_0 \)
- \( R(|Y_i|) \) is the rank of \( |Y_i| \).

Under the null hypothesis:
- \( E[Y_i] = 0 \)
- \( E[X_i] = \theta_0 \)

If the null hypothesis is true, \( T \) should be close to 0. If not, \( T \) will have a high positive or negative value.

#### Implementation in R
We can perform this test in R using the `wilcox.test` function:

```r
# Data
data <- c(12, 11, 8, 7, 10, 12, 13, 5, 12, 16)

# Wilcoxon Signed Rank Test
wilcox.test(data, mu = 12)
```

![Wilcoxon Test Output](/images/wilcox.png)


