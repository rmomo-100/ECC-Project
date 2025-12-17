import pandas as pd

# -----------------------------
# Load Olist Data
# -----------------------------
orders = pd.read_csv("olist_orders_dataset.csv", parse_dates=[
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
])

order_items = pd.read_csv("olist_order_items_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")
#orders = pd.read_csv("olist_orders_dataset.csv")
##payments = pd.read_csv("olist_order_payments_dataset.csv")

# -----------------------------
# SHOPIFY CUSTOMERS
# -----------------------------
shopify_customers = (
    orders.merge(customers, on="customer_id", how="left")
    .groupby("customer_unique_id", as_index=False)
    .agg(
        created_at=("order_purchase_timestamp", "min"),
        total_orders=("order_id", "nunique")
    )
)

shopify_customers = shopify_customers.merge(
    customers,
    on="customer_unique_id",
    how="left"
)

shopify_customers = shopify_customers[[
    "customer_unique_id",
    "customer_city",
    "customer_state",
    "customer_zip_code_prefix",
    "created_at",
    "total_orders"
]]

shopify_customers.columns = [
    "customer_id",
    "city",
    "state",
    "zip",
    "created_at",
    "total_orders"
]

shopify_customers["country"] = "BR"

# -----------------------------
# SHOPIFY ORDERS
# -----------------------------
order_revenue = (
    order_items.groupby("order_id", as_index=False)
    .agg(
        subtotal_price=("price", "sum"),
        shipping_price=("freight_value", "sum")
    )
)

shopify_orders = (
    orders.merge(customers, on="customer_id", how="left")
    .merge(order_revenue, on="order_id", how="left")
)

shopify_orders["total_price"] = (
    shopify_orders["subtotal_price"] + shopify_orders["shipping_price"]
)

shopify_orders = shopify_orders[[
    "order_id",
    "customer_unique_id",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_status",
    "subtotal_price",
    "shipping_price",
    "total_price",
    "order_delivered_customer_date"
]]

shopify_orders.columns = [
    "order_id",
    "customer_id",
    "order_created_at",
    "order_processed_at",
    "order_status",
    "subtotal_price",
    "shipping_price",
    "total_price",
    "delivery_date"
]

shopify_orders["currency"] = "BRL"

# -----------------------------
# SHOPIFY ORDER LINE ITEMS
# -----------------------------
shopify_line_items = order_items[[
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "price",
    "freight_value"
]]

shopify_line_items["quantity"] = 1

shopify_line_items.columns = [
    "order_id",
    "line_item_id",
    "product_id",
    "seller_id",
    "price",
    "shipping_price",
    "quantity"
]


# -----------------------------
# SHOPIFY FULFILLMENTS
# -----------------------------
shopify_fulfillments = orders[[
    "order_id",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]]

def fulfillment_status(row):
    if pd.notnull(row["order_delivered_customer_date"]):
        return "fulfilled"
    elif pd.notnull(row["order_delivered_carrier_date"]):
        return "in_transit"
    else:
        return "unfulfilled"

shopify_fulfillments["fulfillment_status"] = shopify_fulfillments.apply(
    fulfillment_status, axis=1
)

shopify_fulfillments.columns = [
    "order_id",
    "shipped_at",
    "delivered_at",
    "estimated_delivery",
    "fulfillment_status"
]


# -----------------------------
# SAVE TO CSV
# -----------------------------
shopify_customers.to_csv("shopify_customers.csv", index=False)
shopify_orders.to_csv("shopify_orders.csv", index=False)
shopify_line_items.to_csv("shopify_order_line_items.csv", index=False)
#shopify_products.to_csv("shopify_products.csv", index=False)
shopify_fulfillments.to_csv("shopify_fulfillments.csv", index=False)
#shopify_payments.to_csv("shopify_payments.csv", index=False)

print("✅ Shopify-style CSV files successfully created.")
