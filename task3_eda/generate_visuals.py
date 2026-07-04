import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

plt.rcParams['figure.dpi'] = 130
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#444444'
sns.set_style("whitegrid", {'grid.linestyle': ':', 'grid.color': '#dddddd'})

INK = '#2E4057'
AMBER = '#D9A24B'
GREEN = '#5B8C6E'
RED = '#A3475C'
GRAY = '#6C7A89'
BLUE = '#8FA6CB'
PALETTE = [INK, AMBER, GREEN, RED, GRAY, BLUE]

df = pd.read_csv('ecommerce_orders_cleaned.csv', parse_dates=['order_date'])
month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# ============================================================
# FIGURE 1: Revenue trend over time (monthly), with seasonal highlight
# ============================================================
fig, ax = plt.subplots(figsize=(11, 5))
monthly = df.groupby([df['order_date'].dt.to_period('M')])['revenue'].sum()
monthly.index = monthly.index.to_timestamp()
ax.plot(monthly.index, monthly.values, color=INK, linewidth=2, marker='o', markersize=4)
ax.fill_between(monthly.index, monthly.values, color=INK, alpha=0.06)

# highlight holiday season months
for d, v in monthly.items():
    if d.month in [11, 12]:
        ax.plot(d, v, 'o', color=AMBER, markersize=7, zorder=5)

ax.set_title('Monthly revenue (2024–2025)', fontsize=14, fontweight='bold', pad=14, color='#1a1a1a')
ax.set_ylabel('Revenue ($)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
ax.spines[['top','right']].set_visible(False)
ax.text(0.01, -0.18, 'Amber markers = Nov/Dec (holiday season)', transform=ax.transAxes,
        fontsize=9, color=GRAY, style='italic')
plt.tight_layout()
plt.savefig('fig1_revenue_trend.png', bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 2: Revenue by category (bar) + order count (secondary context)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

cat_rev = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
bars = axes[0].barh(cat_rev.index[::-1], cat_rev.values[::-1], color=INK, height=0.6)
axes[0].set_title('Total revenue by category', fontsize=13, fontweight='bold', color='#1a1a1a')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
axes[0].spines[['top','right']].set_visible(False)
for bar in bars:
    w = bar.get_width()
    axes[0].text(w + 3000, bar.get_y() + bar.get_height()/2, f'${w/1000:.0f}k',
                 va='center', fontsize=9, color='#333')

cat_orders = df.groupby('category').size().sort_values(ascending=False)
bars2 = axes[1].barh(cat_orders.index[::-1], cat_orders.values[::-1], color=AMBER, height=0.6)
axes[1].set_title('Order count by category', fontsize=13, fontweight='bold', color='#1a1a1a')
axes[1].spines[['top','right']].set_visible(False)
for bar in bars2:
    w = bar.get_width()
    axes[1].text(w + 15, bar.get_y() + bar.get_height()/2, f'{int(w)}',
                 va='center', fontsize=9, color='#333')

plt.tight_layout()
plt.savefig('fig2_category_breakdown.png', bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 3: Revenue distribution + outliers (boxplot by category)
# ============================================================
fig, ax = plt.subplots(figsize=(11, 5.5))
order = df.groupby('category')['revenue'].median().sort_values(ascending=False).index
sns.boxplot(data=df, x='category', y='revenue', order=order, ax=ax,
            color=BLUE, fliersize=3, linewidth=1.1,
            flierprops=dict(marker='o', markerfacecolor=RED, markeredgecolor='none', alpha=0.5))
ax.set_yscale('log')
ax.set_title('Revenue distribution by category (log scale, outliers visible)', fontsize=13, fontweight='bold', color='#1a1a1a')
ax.set_xlabel('')
ax.set_ylabel('Revenue ($, log scale)')
ax.spines[['top','right']].set_visible(False)
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('fig3_revenue_distribution.png', bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 4: Delivery days vs customer rating (the key insight)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
rating_by_delivery = df.dropna(subset=['customer_rating']).groupby('delivery_days')['customer_rating'].mean()
ax.bar(rating_by_delivery.index, rating_by_delivery.values, color=[
    GREEN if d <= 5 else (AMBER if d <= 8 else RED) for d in rating_by_delivery.index
], width=0.7)
ax.axhline(df['customer_rating'].mean(), color=GRAY, linestyle='--', linewidth=1.3, label=f'Overall avg ({df["customer_rating"].mean():.2f})')
ax.set_title('Average customer rating by delivery time', fontsize=13, fontweight='bold', color='#1a1a1a')
ax.set_xlabel('Delivery time (days)')
ax.set_ylabel('Average rating (1-5)')
ax.set_ylim(0, 5.5)
ax.legend(frameon=False, fontsize=10)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('fig4_delivery_vs_rating.png', bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 5: Acquisition channel performance (revenue + repeat rate)
# ============================================================
fig, ax1 = plt.subplots(figsize=(11, 5.5))
chan = df.groupby('acquisition_channel').agg(
    revenue=('revenue', 'sum'),
    repeat_rate=('is_repeat_customer', 'mean')
).sort_values('revenue', ascending=False)

x = np.arange(len(chan))
bars = ax1.bar(x, chan['revenue'], color=INK, width=0.5, label='Total revenue')
ax1.set_ylabel('Total revenue ($)', color=INK)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f'${v/1000:.0f}k'))
ax1.set_xticks(x)
ax1.set_xticklabels(chan.index, rotation=20, ha='right')
ax1.spines[['top']].set_visible(False)

ax2 = ax1.twinx()
ax2.plot(x, chan['repeat_rate']*100, color=AMBER, marker='D', markersize=7, linewidth=2, label='Repeat customer rate')
ax2.set_ylabel('Repeat customer rate (%)', color=AMBER)
ax2.set_ylim(0, 100)
ax2.spines[['top']].set_visible(False)

ax1.set_title('Revenue and customer loyalty by acquisition channel', fontsize=13, fontweight='bold', color='#1a1a1a')
fig.legend(loc='upper right', bbox_to_anchor=(0.99, 0.97), frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig('fig5_channel_performance.png', bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 6: Correlation heatmap
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6.5))
corr_cols = ['unit_price', 'quantity', 'discount_pct', 'revenue', 'customer_age', 'delivery_days', 'customer_rating']
corr = df[corr_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5, cbar_kws={'shrink':0.8}, ax=ax,
            annot_kws={'fontsize':9})
ax.set_title('Correlation matrix — numeric features', fontsize=13, fontweight='bold', color='#1a1a1a', pad=12)
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.savefig('fig6_correlation_heatmap.png', bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 7: Return rate by category and rating
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

return_by_cat = df.groupby('category')['returned'].mean().sort_values(ascending=False) * 100
bars = axes[0].bar(return_by_cat.index, return_by_cat.values, color=RED, alpha=0.85)
axes[0].set_title('Return rate by category', fontsize=12.5, fontweight='bold', color='#1a1a1a')
axes[0].set_ylabel('Return rate (%)')
axes[0].spines[['top','right']].set_visible(False)
plt.setp(axes[0].get_xticklabels(), rotation=30, ha='right')

rating_return = df.dropna(subset=['customer_rating']).groupby('customer_rating')['returned'].mean() * 100
axes[1].bar(rating_return.index.astype(int), rating_return.values, color=GREEN, alpha=0.85, width=0.6)
axes[1].set_title('Return rate by customer rating', fontsize=12.5, fontweight='bold', color='#1a1a1a')
axes[1].set_xlabel('Customer rating')
axes[1].set_ylabel('Return rate (%)')
axes[1].spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('fig7_returns_analysis.png', bbox_inches='tight')
plt.close()

print("All 7 visualizations generated successfully.")
