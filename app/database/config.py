import os
from dotenv import load_dotenv

#loading the variable environment
load_dotenv()

#Gmail API config
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE','credentials.json')
