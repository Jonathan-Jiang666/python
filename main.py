from app.database.db import Base, engine, SessionLocal
import logging

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
db = SessionLocal()
logger.info("Database metadata created and session opened successfully")
db.close()