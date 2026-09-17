---
title: "weather-lib: Historical Weather in 3 Lines"
excerpt: "City + date range → clean pandas DataFrame. Built after worldweatherpy broke. Sole owner, on PyPI.<br/><img src='/images/500x300.png'>"
collection: portfolio
---

**TL;DR:** Tiny Python package that downloads historical weather via API into a clean `pandas.DataFrame` — with CSV export. Sole owner · Live on PyPI · Last released Aug 2025.

```
pip install weather-lib
```

```python
from HistoricalLocationWeather import HistoricalLocationWeather
w = HistoricalLocationWeather(api_key="...", city="76446",
    start_date="2020-01-01", end_date="2024-05-31", frequency=12,
    csv_directory="./data")
df = w.retrieve_hist_data()
```

## Problem
I needed multi-year, hourly weather to model heat stress and milk yield — but `worldweatherpy` was broken and raw API JSON is painful to join with herd data.

## What I did
*   **City / postal-code → date-range fetcher** on top of World Weather Online API (1 / 3 / 6 / 12-hr frequencies)
*   **Structured output** — `date_time, tempC, humidity, precipMM, windspeedKmph, maxtempC/mintempC, sunHour, uvIndex, astronomy…` straight into pandas
*   **One-flag CSV export** + verbose mode, sane error handling for bad keys / missing columns / ragged rows

## Result
The boring data-plumbing every ag-ML project needs — packaged so the next analysis starts with modeling, not scraping.

**Stack:** Python, requests, pandas · **Links:** [PyPI: weather-lib](https://pypi.org/project/weather-lib/) · [GitHub: rajeshneupane7/weather_data_extraction](https://github.com/rajeshneupane7/weather_data_extraction)
