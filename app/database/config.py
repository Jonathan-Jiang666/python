import os
from dotenv import load_dotenv

# load environment from .env if present
load_dotenv()

# Gmail API config - prefer centralized env name
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_PATH', os.getenv('CREDENTIALS_FILE', 'credentials.json'))
