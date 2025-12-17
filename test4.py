from config import Config
import shopify
import os
from dotenv import load_dotenv
from pathlib import Path
from shopify.session import Session  # explicitly use the SDK Session


def initialize_shopify():
    """Initialize Shopify API session with credentials from .env"""

    # Load .env
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path)

    # Read credentials
    merchant = os.getenv("SHOPIFY_STORE_URL")          # e.g. "your-store.myshopify.com"
    api_version = os.getenv("SHOPIFY_API_VERSION", "2024-07")
    token = Config.SHOPIFY_ACCESS_TOKEN

    # Validate credentials
    if not merchant:
        raise ValueError("❌ SHOPIFY_STORE_URL not found in .env file")

    if not token:
        raise ValueError("❌ SHOPIFY_ACCESS_TOKEN not found in .env file")

    try:
        # Use the official Session signature: (shop_url, version, access_token=None)
        session = Session(merchant, api_version, token)
        shopify.ShopifyResource.activate_session(session)

        print(f"✅ Connected to Shopify store: {merchant}")
        return session

    except Exception as e:
        print(f"❌ Error connecting to Shopify: {e}")
        raise

# Initialize and fetch products
if __name__ == "__main__":
    try:
        api_session = initialize_shopify()
        products = shopify.Product.find(limit=15)
        print(f"✅ Found {len(products)} products")
    except Exception as e:
        print(f"❌ Error: {e}")

print(products[14].title)