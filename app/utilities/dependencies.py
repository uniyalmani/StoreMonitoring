from fastapi import Request
from sqlmodel import Session
from app.controllers.database_initializer import engine





def get_session():
    """creating session for each request"""
    with Session(engine) as session:
        yield session