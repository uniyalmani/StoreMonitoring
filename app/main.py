from fastapi import FastAPI
# from app.migration import Migratetion
from app.controllers.database_initializer import init_db
from app.routes import report
from app import topic
import os

app = FastAPI()


env = os.environ

@app.on_event("startup")
def on_startup():
    topic_name = env.get('TOPIC_NAME')
    topic.create_topic(topic_name=topic_name)
    print("start")
    init_db()
    

app.include_router(report.router)



@app.get("/")
def read_root():
    return {"message": "app is running"}


