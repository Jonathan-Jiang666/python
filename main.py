from app.database.db import Base, engine, SessionLocal
Base.metadata.create_all(bind=engine)
db = SessionLocal()
print("导入成功，数据库连接可用")
db.close()