---
title: "blupf90-wrapper: R-style Formulas for BLUPF90 Genetics"
excerpt: "pip install blupf90-wrapper — fit animal models with R-style formulas instead of hand-writing par files. Sole owner, on PyPI.<br/><img src='/images/500x300.png'>"
collection: portfolio
---

**TL;DR:** Unofficial Python wrapper for the BLUPF90 family (`renumf90`, `blupf90+`). Write `body_weight ~ contemporary_group + ped(animal)` — get par-file rendering, SLURM submission, and typed results. Sole owner · Live on PyPI · Last released Aug 2026.

```
pip install blupf90-wrapper
```

```python
import blupf90 as bf
model = bf.univariate(
    "body_weight ~ contemporary_group + sex + cov(age_days) + ped(animal) + pe(animal)",
    data="phenotypes.txt", pedigree="pedigree.txt", columns="phenotypes.cols.txt",
)
result = model.fit()
print(result.h2)  # +0.40 +/- 0.02
```

## Problem
BLUPF90 is the standard for genetic evaluation — but its file-based `renum_*.par` interface is unforgiving: column numbers must match exactly, random-effect blocks must be ordered, `OPTION se_covar_function` is hand-written, and multi-trait batches become bash + sed soup.

## What I did
*   **R / statsmodels-style formula grammar** — `ped()`, `pe()`, `cov()`, `leg()`, `rrm_ped()`, `rrm_pe()` → correct `cross` / `cov` / random-group blocks automatically
*   **Auto par-file rendering** — column indexing, effect ordering, multi-trait `(CO)VARIANCES` + heritability / correlation `se_covar_function` blocks
*   **One-command scale-up** — `univariate_set` / `bivariate_set` → single `sbatch --array` job, per-model folders, `collect()` + `write_tsv()` for publication tables
*   **Log → typed Result** — parses `blup_vc.log` into `.h2`, `.rg`, `.Va`, `.Vpe`, `.Ve` with SEs; random-regression (Legendre) support for growth / lactation curves
*   **Zero-dependency core** — pure Python rendering + parsing; BLUPF90 binaries only needed to actually run

## Result
Package quantitative geneticists actually use for everyday lab work *and* reproducible papers — every run leaves a self-contained folder (par file, symlinks, logs, parsed summary).

**Stack:** Python, NumPy (RRM only), SLURM/HPC · **Links:** [PyPI: blupf90-wrapper](https://pypi.org/project/blupf90-wrapper/) · [GitHub: rajeshneupane7/blupf90-wrapper](https://github.com/rajeshneupane7/blupf90-wrapper) · **Proof:** 5★ on GitHub, MIT-licensed (wrapper only — BLUPF90 itself © UGA, used under its own terms)
