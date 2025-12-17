from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

print("ENV PATH:", env_path)
print("ENV EXISTS:", env_path.exists())

print("Shop:", os.getenv("SHOPIFY_STORE_URL"))
print("Token loaded:", bool(os.getenv("SHOPIFY_ACCESS_TOKEN")))
