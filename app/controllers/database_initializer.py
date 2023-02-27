
from sqlmodel import Session, create_engine, SQLModel
# from sqlalchemy import create_engine
from app.models.database_models import *
import os



# print("yes")

env = os.environ
mysql_root_host = env.get('MYSQL_ROOT_HOST')
mysql_username = env.get("MYSQL_USER")
mysql_port = env.get('MYSQL_PORT', 3306)
mysql_database = env.get("MYSQL_DATABASE")
mysql_password = env.get("MYSQL_PASSWORD")

URL = f"mysql://{mysql_username}:{mysql_password}@{mysql_root_host}:{mysql_port}/{mysql_database}"


engine = create_engine(URL)



def init_db():
    SQLModel.metadata.create_all(engine)

