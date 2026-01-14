
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .. import config
import logging

logger = logging.getLogger(__name__)

# Database connection URL is provided by app/config.py (reads env by default)
DATABASE_URL = getattr(config, 'DATABASE_URL', None)
if not DATABASE_URL:
	logger.error('DATABASE_URL is not configured. Set DATABASE_URL env or update app/config.py')
	raise RuntimeError('DATABASE_URL is not configured')

# Build engine with appropriate args for sqlite vs other DBs
engine_kwargs = {"echo": True, "future": True}
if DATABASE_URL.startswith('sqlite'):
	engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, **engine_kwargs)
else:
	engine = create_engine(DATABASE_URL, **engine_kwargs)

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# ORM base class for models
Base = declarative_base()