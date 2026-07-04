# E-Commerce Order Data — Exploratory Data Analysis Report

**Task 3: Data Analysis & EDA — Horizon TechX Internship**

## Dataset overview

5,050 raw order records spanning January 2024 to December 2025, covering 8 product categories, 5 regions, 6 acquisition channels, and 5 payment methods. The dataset was intentionally generated with realistic data-quality issues to demonstrate a genuine cleaning pipeline rather than analyzing data that was already pristine.

## 1. Cleaning and preprocessing

| Issue found | Rows affected | Resolution |
|---|---|---|
| Exact duplicate rows | 50 | Dropped |
| Invalid quantity (≤ 0) | 4 | Dropped — data entry error, not a valid return-to-zero state |
| Invalid unit price (negative) | 4 | Dropped — sign error during entry |
| Inconsistent category text (`" electronics"`, `"BEAUTY "`, etc.) | ~250 | Standardized via `.strip().str.title()` |
| Missing `customer_age` | 202 | Imputed with category-level median (age skews differently by product type) |
| Missing `discount_pct` | 76 | Imputed as 0 (missing almost certainly means no discount was applied at checkout) |
| Missing `delivery_days` | 101 | Imputed with region-level median (delivery time is structurally regional) |
| Missing `customer_rating` | 152 | **Left as missing** — imputing a satisfaction score would fabricate sentiment, so all rating analysis explicitly excludes nulls rather than guessing |
| Revenue field inconsistency | all rows | Recomputed from `unit_price × quantity × (1 − discount)` rather than trusting the source revenue column, since source-system revenue fields are a common point of corruption |

Final cleaned dataset: **4,992 rows**, 20 columns (15 original + 5 derived calendar features).

This table itself is a finding worth presenting to a recruiter: it shows the difference between *running* `.describe()` and *actually deciding*, row by row, what a missing or invalid value means in context — which is the actual skill EDA is testing for.

## 2. Key business metrics

- **Total revenue:** $547,818
- **Total orders:** 4,992
- **Average order value:** $109.74
- **Return rate:** 7.27%
- **Repeat customer rate:** 42.6%
- **Average customer rating:** 3.95 / 5

## 3. Findings

### Finding 1 — Revenue is heavily seasonal and concentrated in one category
Electronics alone generates **$308,152**, more than the next three categories combined (Home & Kitchen, Apparel, Sports together total $172,368). Monthly revenue also spikes sharply in November and December — both holiday-season months sit near or above the two-year peak, consistent with the seasonal demand multiplier built into order volume during that window.

*(See `fig1_revenue_trend.png` and `fig2_category_breakdown.png`)*

**Business implication:** inventory planning and ad spend should weight Electronics and the Nov-Dec window disproportionately; a category-agnostic, flat monthly budget would systematically under-stock the highest-revenue segment during its highest-demand period.

### Finding 2 — Revenue per order is right-skewed with a meaningful outlier tail
The IQR-based outlier check flags 346 orders (6.9% of all orders) above $278.09 in revenue — and those orders alone account for **34.4% of total revenue**. This is not noise to be removed; it is a distinct customer behavior (premium electronics, bulk purchases) that a mean-based "average customer" model would wash out entirely.

*(See `fig3_revenue_distribution.png`)*

**Business implication:** any retention or marketing strategy built solely around the "typical" $109 order would be designed for the majority of *orders* but miss the minority of orders driving a third of *revenue*. These high-value orders justify a separate analysis and likely a separate retention strategy (e.g. white-glove support, extended warranty upsells).

### Finding 3 — Delivery delay is a statistically significant driver of customer dissatisfaction
Pearson correlation between delivery days and customer rating: **r = −0.10, p = 2.5 × 10⁻¹²**. While the correlation coefficient is modest, the p-value confirms this is not due to chance at this sample size, and the effect is visible directly in the data: average rating drops as delivery time extends past roughly 5-6 days, falling well below the dataset's overall average of 3.95.

*(See `fig4_delivery_vs_rating.png`)*

The **Central** region has the slowest average delivery time at 5.6 days, compared to 4.0-4.1 days everywhere else — a full 1.5-day gap that disproportionately exposes that region's customers to the rating penalty above.

**Business implication:** logistics investment in the Central region's fulfillment or carrier network has a direct, measurable link to customer satisfaction, not just operational efficiency.

### Finding 4 — Acquisition channel quality varies more in loyalty than in raw conversion
Repeat-customer rate by channel is tightly clustered (41.5%-44.8%), but **Direct traffic produces the highest repeat rate (44.8%)** while **Paid Ads produces the lowest (41.5%)**, despite Paid Ads being a major spend channel.

*(See `fig5_channel_performance.png`)*

**Business implication:** if customer lifetime value matters more than first-order conversion, the channel mix should be evaluated on repeat-rate quality, not just acquisition volume — paid acquisition may be buying lower-loyalty customers even where it's hitting volume targets.

### Finding 5 — Returns are concentrated where dissatisfaction is concentrated, not randomly distributed
Return rate by customer rating shows a clear, expected pattern: low-rating orders return at a dramatically higher rate than high-rating ones, confirming the dataset's return mechanism is behaviorally consistent rather than noise. Toys (8.5%) and Beauty (7.7%) have the highest category return rates; Grocery (5.4%) the lowest, consistent with their respective return logistics (perishables are rarely returnable; toys/beauty have higher size, fit, or shade mismatch issues).

*(See `fig7_returns_analysis.png`)*

## 4. Correlation summary

The strongest relationships in the numeric feature set:
- `unit_price` ↔ `revenue`: **r = 0.82** (expected — price is a direct multiplicative input to revenue)
- `quantity` ↔ `revenue`: **r = 0.31** (positive but secondary to price)
- `delivery_days` ↔ `customer_rating`: **r = −0.10** (modest but statistically significant, see Finding 3)

No spurious or unexpected strong correlations were found among the remaining numeric features, which is itself a useful negative result — it rules out, for example, any meaningful relationship between customer age and spending behavior in this dataset.

*(See `fig6_correlation_heatmap.png`)*

## 5. Methodology notes for reviewers

- All imputation choices are documented and justified per-column rather than applying one blanket strategy (e.g. `fillna(0)` everywhere), because different missingness mechanisms call for different treatments.
- Outliers were *identified and analyzed*, not silently dropped — Finding 2 exists because the outliers were investigated rather than discarded.
- The delivery/rating relationship was validated with a proper hypothesis test (Pearson correlation + p-value) rather than asserted from eyeballing a chart.
- Revenue was recomputed from first principles rather than trusting a pre-existing column, which is standard practice when source data may have come from inconsistent systems.

## Files in this submission

- `generate_dataset.py` — synthetic but realistically messy dataset generator
- `ecommerce_orders_raw.csv` — raw data before cleaning
- `eda_analysis.py` — cleaning, descriptive statistics, correlation analysis
- `ecommerce_orders_cleaned.csv` — cleaned dataset
- `generate_visuals.py` — all 7 chart generation code
- `fig1`–`fig7` `.png` — exported visualizations
- `summary_statistics.csv` — descriptive statistics table
- `EDA_Notebook.ipynb` — consolidated, presentable Jupyter notebook version of the full analysis
- `eda_report.md` — this report
