import os
from logging.handlers import RotatingFileHandler
import logging

# Project layout
APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))
DATA_DIR = os.path.join(APP_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Paths for common files
def resolve_data_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)

# Timezone
TIMEZONE = os.environ.get('APP_TIMEZONE', 'Asia/Shanghai')

# iCloud / Google credentials (load from env in production)
ICLOUD_USER = os.environ.get('ICLOUD_USER')
ICLOUD_PASSWORD = os.environ.get('ICLOUD_PASSWORD')

# Database connection URL. Prefer setting via environment for production.
# Defaults to a local SQLite file under `app/data/dev.db` for development.
DATABASE_URL = os.environ.get(
    ```python
    import os
    from logging.handlers import RotatingFileHandler
    import logging

    # Project layout
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, '..'))
    DATA_DIR = os.path.join(APP_DIR, 'data')
    os.makedirs(DATA_DIR, exist_ok=True)

    # Paths for common files
    def resolve_data_path(filename: str) -> str:
        return os.path.join(DATA_DIR, filename)

    # Timezone
    TIMEZONE = os.environ.get('APP_TIMEZONE', 'Asia/Shanghai')

    # iCloud / Google credentials (load from env in production)
    ICLOUD_USER = os.environ.get('ICLOUD_USER')
    ICLOUD_PASSWORD = os.environ.get('ICLOUD_PASSWORD')

    # Google OAuth file paths (defaults to app/data)
    GOOGLE_CREDENTIALS_PATH = os.environ.get('GOOGLE_CREDENTIALS_PATH', resolve_data_path('credentials.json'))
    GOOGLE_TOKEN_PATH = os.environ.get('GOOGLE_TOKEN_PATH', resolve_data_path('token.pickle'))

    # Processed emails tracking file
    PROCESSED_EMAILS_FILE = os.environ.get('PROCESSED_EMAILS_FILE', resolve_data_path('processed_emails.json'))

    # Logging config
    LOG_FILE = os.environ.get('APP_LOG_FILE', os.path.join(APP_DIR, 'app.log'))
    LOG_LEVEL = os.environ.get('APP_LOG_LEVEL', 'INFO')

    def init_logging(level=None):
        root = logging.getLogger()
        if root.handlers:
            return
        # allow override via env or parameter
        if level is None:
            level_name = LOG_LEVEL.upper() if isinstance(LOG_LEVEL, str) else 'INFO'
            level = getattr(logging, level_name, logging.INFO)
        root.setLevel(level)
        handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(fmt)
        root.addHandler(handler)
        # also log to console
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        root.addHandler(console)

    # APScheduler / jobstore
    APSCHEDULER_JOBSTORE_URL = os.environ.get('APSCHEDULER_JOBSTORE_URL', '')

    # External API retry/backoff defaults
    EXTERNAL_API_RETRIES = int(os.environ.get('EXTERNAL_API_RETRIES', '3'))
    EXTERNAL_API_BACKOFF_SECS = float(os.environ.get('EXTERNAL_API_BACKOFF_SECS', '2'))

    # Database connection URL. Prefer setting via environment for production.
    # Defaults to a local SQLite file under `app/data/dev.db` for development.
    DATABASE_URL = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(DATA_DIR, 'dev.db')}"
    )

    ```
