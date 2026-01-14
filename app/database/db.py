
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Database connection (MySql)
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/personal_ai_assistant"

# Crate a database engine
#echo=True 会在控制台输出所有SQL语句，用于调试
#future = Ture,启用SQLALchemy 2.0的一些新特征
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory
#bind = engine,绑定到前面创建的数据库引擎
#autoflush=False,禁止自动刷新
#autocommit = false,禁止自动提交，需手动提交
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#ORM basic class ,it's core class , it be used to create ORM model
# Base是所有ORM的模型基础类
#定义的每个数据库基础表都需要继承这个类
Base = declarative_base()