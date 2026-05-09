
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker,declarative_base
import os

load_dotenv()    # 读取配置文件的内容到环境变量
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

# 创建数据库引擎

# print(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

engine = create_engine(
    # "mysql+pymysql://root:123456@localhost/fastapi_project0420",
    f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}',
    pool_size=10
)
# 创建基类
Base = declarative_base()
# 创建会话工厂
Session = sessionmaker(bind=engine)
# 创建会话
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()