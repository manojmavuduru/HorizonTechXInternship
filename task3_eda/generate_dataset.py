import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

N = 5000

categories = ['Electronics', 'Apparel', 'Home & Kitchen', 'Beauty', 'Sports', 'Books', 'Toys', 'Grocery']
category_weights = [0.22, 0.20, 0.15, 0.12, 0.10, 0.08, 0.08, 0.05]

regions = ['North', 'South', 'East', 'West', 'Central']
region_weights = [0.25, 0.22, 0.20, 0.23, 0.10]

channels = ['Organic Search', 'Paid Ads', 'Email', 'Social Media', 'Direct', 'Referral']
channel_weights = [0.28, 0.20, 0.12, 0.18, 0.15, 0.07]

payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Wallet', 'Cash on Delivery']
payment_weights = [0.38, 0.22, 0.18, 0.14, 0.08]

base_price_by_category = {
    'Electronics': 180, 'Apparel': 45, 'Home & Kitchen': 65,
    'Beauty': 30, 'Sports': 55, 'Books': 18, 'Toys': 35, 'Grocery': 22
}

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(N):
    order_id = f"ORD{100000 + i}"
    cat = np.random.choice(categories, p=category_weights)
    region = np.random.choice(regions, p=region_weights)
    channel = np.random.choice(channels, p=channel_weights)
    payment = np.random.choice(payment_methods, p=payment_weights)

    day_offset = np.random.randint(0, date_range_days)
    # seasonal boost around Nov-Dec (holiday season) and back-to-school (Aug-Sep)
    order_date = start_date + timedelta(days=day_offset)
    month = order_date.month

    base_price = base_price_by_category[cat]
    price = max(5, np.random.normal(base_price, base_price * 0.35))

    seasonal_multiplier = 1.0
    if month in [11, 12]:
        seasonal_multiplier = 1.4
    elif month in [8, 9]:
        seasonal_multiplier = 1.15

    quantity = np.random.choice([1,1,1,2,2,3,4,5], p=[0.35,0.2,0.15,0.12,0.08,0.05,0.03,0.02])
    quantity = max(1, int(quantity * (seasonal_multiplier if np.random.random() < 0.3 else 1)))

    discount_pct = np.random.choice([0, 0, 0, 5, 10, 15, 20, 25], p=[0.4,0.15,0.1,0.12,0.1,0.07,0.04,0.02])

    customer_age = int(np.clip(np.random.normal(35, 12), 18, 75))
    is_repeat_customer = np.random.choice([True, False], p=[0.42, 0.58])

    delivery_days = max(1, int(np.random.normal(4.5, 2)))
    if region == 'Central':
        delivery_days += np.random.randint(1,3)

    rating = np.random.choice([1,2,3,4,5], p=[0.04, 0.06, 0.15, 0.35, 0.40])
    # simulate a delivery-delay effect on rating
    if delivery_days > 7 and np.random.random() < 0.6:
        rating = max(1, rating - np.random.randint(1,3))

    returned = False
    if rating <= 2 and np.random.random() < 0.45:
        returned = True
    elif np.random.random() < 0.03:
        returned = True

    revenue = round(price * quantity * (1 - discount_pct/100), 2)

    rows.append({
        'order_id': order_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'category': cat,
        'region': region,
        'acquisition_channel': channel,
        'payment_method': payment,
        'unit_price': round(price, 2),
        'quantity': quantity,
        'discount_pct': discount_pct,
        'revenue': revenue,
        'customer_age': customer_age,
        'is_repeat_customer': is_repeat_customer,
        'delivery_days': delivery_days,
        'customer_rating': rating,
        'returned': returned
    })

df = pd.DataFrame(rows)

# --- inject realistic messiness ---

# 1. Missing values scattered across several columns
for col, frac in [('customer_age', 0.04), ('customer_rating', 0.03), ('delivery_days', 0.02), ('discount_pct', 0.015)]:
    idx = df.sample(frac=frac, random_state=hash(col) % 1000).index
    df.loc[idx, col] = np.nan

# 2. Inconsistent category capitalization/spacing (simulate messy source systems)
messy_idx = df.sample(frac=0.05, random_state=7).index
def mess_up_category(val):
    variants = [val.upper(), val.lower(), f" {val}", f"{val} "]
    return random.choice(variants)
df.loc[messy_idx, 'category'] = df.loc[messy_idx, 'category'].apply(mess_up_category)

# 3. Duplicate rows (common real-world issue from double form submission)
dup_rows = df.sample(frac=0.01, random_state=99)
df = pd.concat([df, dup_rows], ignore_index=True)

# 4. A few negative/invalid quantity or price entries (data entry errors)
err_idx = df.sample(n=8, random_state=21).index
df.loc[err_idx[:4], 'quantity'] = -1
df.loc[err_idx[4:], 'unit_price'] = -df.loc[err_idx[4:], 'unit_price']

# 5. Outlier prices (legit but extreme, e.g. premium electronics)
outlier_idx = df.sample(n=15, random_state=55).index
df.loc[outlier_idx, 'unit_price'] = df.loc[outlier_idx, 'unit_price'] * np.random.uniform(8, 15, size=15)
df.loc[outlier_idx, 'revenue'] = df.loc[outlier_idx, 'unit_price'] * df.loc[outlier_idx, 'quantity']

# shuffle rows so duplicates aren't conveniently at the end
df = df.sample(frac=1, random_state=3).reset_index(drop=True)

df.to_csv('ecommerce_orders_raw.csv', index=False)
print(f"Generated {len(df)} rows, {df.shape[1]} columns")
print(df.isna().sum())
print("---")
print(df.dtypes)
