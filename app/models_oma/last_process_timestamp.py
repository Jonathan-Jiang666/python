from sqlalchemy import Column, String, func, DateTime
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base
class LastProcessTimeStamp (Base):
    __tablename__ = "last_processed"
    table_name = Column (String(200), primary_key=True, nuallable=False)
    last_timestamp = Column(DateTime, server_default=func.now())
