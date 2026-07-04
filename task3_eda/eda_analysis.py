"""
Task 3: Data Analysis & Exploratory Data Analysis
Horizon TechX Internship

Dataset: E-commerce order history (5,050 rows, synthetic but realistically
messy — missing values, inconsistent text casing, duplicates, data-entry
errors, and genuine outliers).

This script performs the full pipeline expected of the task:
  1. Clean and preprocess
  2. EDA with statistics and visualizations
  3. Identify trends, patterns, and insights
  4. Generate an analytical report (see eda_report.md)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

plt.rcParams['figure.dpi'] = 130
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid", {'grid.linestyle': ':', 'grid.color': '#d8d8d8'})

PALETTE = ['#2E4057', '#D9A24B', '#5B8C6E', '#A3475C', '#6C7A89', '#8FA6CB']
sns.set_palette(PALETTE)

# ============================================================
# 1. LOAD + CLEAN
# ============================================================

df_raw = pd.read_csv('ecommerce_orders_raw.csv')
print(f"Raw shape: {df_raw.shape}")

df = df_raw.copy()

# --- 1a. Fix inconsistent category text ---
df['category'] = df['category'].str.strip().str.title()

# --- 1b. Remove exact duplicate rows ---
n_dupes = df.duplicated().sum()
df = df.drop_duplicates().reset_index(drop=True)
print(f"Removed {n_dupes} duplicate rows")

# --- 1c. Fix invalid quantity/price data entry errors ---
n_bad_qty = (df['quantity'] <= 0).sum()
df = df[df['quantity'] > 0]
n_bad_price = (df['unit_price'] <= 0).sum()
df = df[df['unit_price'] > 0]
print(f"Removed {n_bad_qty} rows with invalid quantity, {n_bad_price} with invalid price")

# --- 1d. Recompute revenue cleanly post-cleaning (don't trust source revenue blindly) ---
df['revenue'] = (df['unit_price'] * df['quantity'] * (1 - df['discount_pct'].fillna(0)/100)).round(2)

# --- 1e. Parse dates, derive calendar features ---
df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.month
df['month_name'] = df['order_date'].dt.strftime('%b')
df['year'] = df['order_date'].dt.year
df['weekday'] = df['order_date'].dt.day_name()
df['quarter'] = df['order_date'].dt.quarter

# --- 1f. Handle missing values deliberately, not blanket-dropped ---
# customer_age: impute with category-level median (age likely varies by product type)
df['customer_age'] = df.groupby('category')['customer_age'].transform(
    lambda x: x.fillna(x.median())
)
# discount_pct: missing almost certainly means "no discount applied"
df['discount_pct'] = df['discount_pct'].fillna(0)
# delivery_days: impute with region median (delivery time is regional)
df['delivery_days'] = df.groupby('region')['delivery_days'].transform(
    lambda x: x.fillna(x.median())
)
# customer_rating: leave missing as-is (NaN) — imputing a satisfaction score would
# fabricate sentiment data; we exclude NaNs only when specifically analyzing ratings

print(f"\nMissing values after cleaning:\n{df.isna().sum()[df.isna().sum() > 0]}")
print(f"\nFinal cleaned shape: {df.shape}")

df.to_csv('ecommerce_orders_cleaned.csv', index=False)

# ============================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================

summary_stats = df[['unit_price', 'quantity', 'revenue', 'customer_age', 'delivery_days', 'customer_rating']].describe().round(2)
summary_stats.to_csv('summary_statistics.csv')
print("\n--- Summary statistics ---")
print(summary_stats)

# Outlier detection via IQR on revenue
Q1, Q3 = df['revenue'].quantile([0.25, 0.75])
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
outliers = df[df['revenue'] > upper_bound]
print(f"\nRevenue outliers (IQR method): {len(outliers)} orders above ${upper_bound:.2f}")
print(f"These {len(outliers)} orders ({len(outliers)/len(df)*100:.1f}% of data) contribute "
      f"${outliers['revenue'].sum():,.0f} ({outliers['revenue'].sum()/df['revenue'].sum()*100:.1f}% of total revenue)")

# ============================================================
# 3. KEY BUSINESS METRICS
# ============================================================

total_revenue = df['revenue'].sum()
avg_order_value = df['revenue'].mean()
total_orders = len(df)
return_rate = df['returned'].mean() * 100
repeat_rate = df['is_repeat_customer'].mean() * 100
avg_rating = df['customer_rating'].mean()

print(f"\n--- Key metrics ---")
print(f"Total revenue: ${total_revenue:,.2f}")
print(f"Total orders: {total_orders:,}")
print(f"Average order value: ${avg_order_value:.2f}")
print(f"Return rate: {return_rate:.2f}%")
print(f"Repeat customer rate: {repeat_rate:.2f}%")
print(f"Average customer rating: {avg_rating:.2f} / 5")

# ============================================================
# 4. CORRELATION ANALYSIS
# ============================================================

corr_cols = ['unit_price', 'quantity', 'discount_pct', 'revenue', 'customer_age', 'delivery_days', 'customer_rating']
corr_matrix = df[corr_cols].corr().round(2)
print(f"\n--- Correlation matrix ---\n{corr_matrix}")

# Statistically notable relationship to verify: delivery_days vs customer_rating
from scipy import stats
valid = df.dropna(subset=['delivery_days', 'customer_rating'])
corr_coef, p_value = stats.pearsonr(valid['delivery_days'], valid['customer_rating'])
print(f"\nDelivery days vs rating: r = {corr_coef:.3f}, p = {p_value:.2e}")

print("\nEDA core analysis complete. Generating visualizations...")
