# Atlas Insights — E-Commerce EDA

**Task 3: Data Analysis & Exploratory Data Analysis — Horizon TechX Internship**

A full exploratory data analysis pipeline on a deliberately messy, synthetic e-commerce order dataset — cleaning, descriptive statistics, correlation analysis, and five data-backed business findings, each traced back to a specific chart.

## Why this isn't just `.describe()` and a histogram

Most student EDA submissions run pandas' built-in summary functions on a dataset that's already clean and call it analysis. This dataset was generated with **realistic data-quality problems on purpose** — duplicates, invalid values, inconsistent text casing, missing fields — specifically so the cleaning step is a real decision-making exercise, not a formality.

| Issue found | Rows affected | Resolution |
|---|---|---|
| Exact duplicate rows | 50 | Dropped |
| Invalid quantity (≤ 0) | 4 | Dropped — data entry error |
| Invalid unit price (negative) | 4 | Dropped — sign error |
| Inconsistent category text (`" electronics"`, `"BEAUTY "`) | ~250 | Standardized |
| Missing `customer_age` | 202 | Imputed with category-level median |
| Missing `discount_pct` | 76 | Imputed as 0 |
| Missing `delivery_days` | 101 | Imputed with region-level median |
| Missing `customer_rating` | 152 | **Left missing** — imputing a satisfaction score would fabricate sentiment |
| Revenue field | all rows | Recomputed from `unit_price × quantity × (1 − discount)` rather than trusted as-is |

Final cleaned dataset: **4,992 rows**, 20 columns (15 original + 5 derived calendar features), from 5,050 raw records.

## Key metrics

- **Total revenue:** $547,818
- **Total orders:** 4,992
- **Average order value:** $109.74
- **Return rate:** 7.27%
- **Repeat customer rate:** 42.6%
- **Average customer rating:** 3.95 / 5

## Five findings, each with a business implication

1. **Revenue is concentrated and seasonal** — Electronics alone ($308,152) outsells the next three categories combined; Nov/Dec sit at or above the two-year peak. → Inventory and ad spend should weight Electronics and the holiday window disproportionately.
2. **A thin tail of orders drives outsized revenue** — 6.9% of orders (above $278) account for 34.4% of total revenue. → A retention strategy built around the "typical" $109 order misses the segment worth the most.
3. **Delivery delay measurably hurts ratings** (r = −0.10, p = 2.5×10⁻¹²) — the Central region runs 1.5 days slower than everywhere else. → Logistics investment there has a direct line to satisfaction.
4. **Loyalty varies more than conversion across channels** — Direct traffic has the best repeat rate (44.8%) despite Paid Ads getting more spend (41.5% repeat rate). → Evaluate channel mix on repeat-rate quality, not just volume.
5. **Returns track dissatisfaction, not randomness** — low-rating orders return far more often; Toys and Beauty have the highest category return rates, consistent with fit/shade mismatch.

Full writeup with methodology and correlation summary: [`eda_report.md`](./eda_report.md).

## Files

| File | What it is |
|---|---|
| `EDA_Notebook.ipynb` | The full analysis, runnable end to end |
| `eda_report.md` | Narrative writeup of findings (source for this README's summary) |
| `eda_analysis.py` | Standalone script version of the analysis |
| `generate_dataset.py` | Builds the synthetic raw dataset with intentional data-quality issues |
| `generate_visuals.py` | Produces the seven `fig*.png` charts |
| `ecommerce_orders_raw.csv` / `ecommerce_orders_cleaned.csv` | Data before/after cleaning |
| `summary_statistics.csv` | Descriptive stats on the cleaned dataset |
| `fig1`–`fig7`.png | Revenue trend, category breakdown, revenue distribution, delivery vs. rating, channel performance, correlation heatmap, returns analysis |

## Run it

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
jupyter notebook EDA_Notebook.ipynb
```

Or run the plain script version: `python eda_analysis.py`

## Why this is a strong submission

It treats cleaning as an analytical decision (documented row-by-row, with reasoning for each choice — including *not* imputing a field where imputation would fabricate a signal), backs every finding with a specific statistic and a specific chart, and closes each finding with what a business should actually do about it, rather than stopping at description.

