---
title: Folder structure scan
layout: page
permalink: /folder-structure-scan/
---

This page documents a small repository scanner included in this project: `scripts/scan_repo.py`.

What it does

- Scans the repository for common issues that affect Jekyll sites and general projects.
- Checks for markdown files that appear to lack YAML front matter.
- Lists files with spaces in their names (which can break static site generators).
- Finds large files (>5 MB) which may bloat your repo.
- Detects duplicate post slugs in `_posts/` (possible filename conflicts).
- Reports uncommitted git changes.

How to run

From the repository root run:

```bash
python3 scripts/scan_repo.py
```

This writes a `scan-report.txt` file at the repository root and prints a short summary to stdout.

When to use

- Before publishing or deploying the static site.
- Before creating a pull request to catch generated files accidentally included.
- As part of a CI check (you can run the script in CI and fail if critical issues are found).

Next steps

If the scan reports issues you don't expect (for example, generated `_site/` files), consider regenerating or cleaning the working tree and committing only source files. If you need help interpreting the report or automatically fixing common problems, open an issue or ask for assistance.
