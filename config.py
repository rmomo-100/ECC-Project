import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API tokens and credentials"""
    
    # Shopify Configuration
    # SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
    # SHOPIFY_API_PASSWORD = os.getenv('SHOPIFY_API_PASSWORD')
    SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
    
    # Meta/Facebook Configuration
    # META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
    # META_APP_ID = os.getenv('META_APP_ID')
    # META_APP_SECRET = os.getenv('META_APP_SECRET')
    
    # Database Configuration
    # DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    @staticmethod
    def validate_tokens():
        """Validate that all required tokens are set"""
        required_tokens = ['SHOPIFY_ACCESS_TOKEN'] #,'META_ACCESS_TOKEN']
        missing = [token for token in required_tokens if not getattr(Config, token)]
        
        if missing:
            print(f"⚠️  Warning: Missing tokens: {', '.join(missing)}")
            return False
        return True
