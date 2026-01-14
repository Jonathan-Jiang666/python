# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column , Integer , String , func , DateTime
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base


class AISuggestions (Base):
    __tablename__ = "ai_suggestions"
    id = Column (Integer , primary_key=True , index=True)
    user_id = Column (Integer , index=True)
    suggestion_time = Column (DateTime , server_default=func.now ())
    suggestion_type = Column (String (100) , index=True)
    content = Column (String (100000))
    related_data_ids = Column (String (100000))
    ai_model_version = Column (String (50) , index=True)
