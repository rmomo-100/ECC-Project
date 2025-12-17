import pandas as pd
import numpy as np

np.random.seed(42)

orders = pd.read_csv(
    "shopify_orders.csv",
    parse_dates=["order_created_at"]
)

orders["order_date"] = orders["order_created_at"].dt.date

daily_revenue = (
    orders.groupby("order_date", as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("total_price", "sum")
    )
)

daily_revenue["avg_order_value"] = (
    daily_revenue["total_revenue"]
    / daily_revenue["total_orders"].replace(0, np.nan)
)


campaigns = pd.DataFrame({
    "campaign_id": ["META_CAMP_1", "META_CAMP_2", "META_CAMP_3", "META_CAMP_4"],
    "campaign_name": [
        "Prospecting - Broad",
        "Prospecting - Lookalike",
        "Retargeting - Website",
        "Retargeting - Cart"
    ],
    "objective": ["conversions"] * 4,
    "platform": ["Instagram", "Facebook", "Instagram", "Facebook"]
})

meta_ads_daily = daily_revenue.assign(key=1).merge(
    campaigns.assign(key=1), on="key"
).drop("key", axis=1)

# Revenue attributed to Meta (35–50%)
meta_ads_daily["meta_revenue"] = (
    meta_ads_daily["total_revenue"]
    * np.random.uniform(0.35, 0.50, len(meta_ads_daily))
)

# Split revenue across campaigns
meta_ads_daily["purchase_value"] = (
    meta_ads_daily["meta_revenue"] / 4
)

# ROAS between 2.2–3.8
meta_ads_daily["roas"] = np.random.uniform(2.2, 3.8, len(meta_ads_daily))
meta_ads_daily["spend"] = meta_ads_daily["purchase_value"] / meta_ads_daily["roas"]

# Conversion rate 2–3.5%
meta_ads_daily["purchases"] = (
    meta_ads_daily["purchase_value"]
    / meta_ads_daily["avg_order_value"]
).replace([np.inf, -np.inf], np.nan)

meta_ads_daily["purchases"] = (
    meta_ads_daily["purchases"]
    .fillna(0)
    .round()
    .astype(int)
)


meta_ads_daily["clicks"] = (
    meta_ads_daily["purchases"]
    / np.random.uniform(0.02, 0.035, len(meta_ads_daily))
)

meta_ads_daily["clicks"] = (
    meta_ads_daily["clicks"]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
    .round()
    .astype(int)
)

meta_ads_daily["impressions"] = (
    meta_ads_daily["clicks"]
    / np.random.uniform(0.008, 0.015, len(meta_ads_daily))
)

meta_ads_daily["impressions"] = (
    meta_ads_daily["impressions"]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
    .round()
    .astype(int)
)


fact_meta_ads_daily = meta_ads_daily[[
    "order_date",
    "campaign_id",
    "campaign_name",
    "objective",
    "spend",
    "impressions",
    "clicks",
    "purchases",
    "purchase_value",
    "platform"
]]

fact_meta_ads_daily.columns = [
    "ad_date",
    "campaign_id",
    "campaign_name",
    "objective",
    "spend",
    "impressions",
    "clicks",
    "purchases",
    "purchase_value",
    "platform"
]

fact_meta_ads_daily["channel"] = "Meta"

# Assign each order to a Meta campaign
orders_meta = orders.copy()
orders_meta["campaign_id"] = np.random.choice(
    campaigns["campaign_id"],
    size=len(orders_meta)
)

orders_meta["attributed_revenue"] = (
    orders_meta["total_price"]
    * np.random.uniform(0.35, 0.50, len(orders_meta))
)

bridge_meta_orders = orders_meta[[
    "order_id",
    "customer_id",
    "order_date",
    "campaign_id",
    "attributed_revenue"
]]

bridge_meta_orders["attribution_model"] = "last_click"
bridge_meta_orders["channel"] = "Meta"

fact_meta_ads_daily.to_csv("fact_meta_ads_daily.csv", index=False)
bridge_meta_orders.to_csv("bridge_meta_orders.csv", index=False)

print("✅ Synthetic Meta Ads data generated successfully.")
#print(meta_ads_daily[["spend", "purchase_value", "purchases", "clicks", "impressions"]].describe())
