import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlmodel import Field, SQLModel, select,  Index
from sqlalchemy import UniqueConstraint, String, Column,  DateTime
import enum




# print("sucessfull 1 ")

class StoreSchedule(SQLModel, table=True):

    __tablename__ = "store_schedule"

    id: int = Field(primary_key=True)
    store_id: str
    dayOfWeek: int
    start_time_local: str = Field(default="0:00:00", max_length=8)
    end_time_local: str = Field(default="23:59:59", max_length=8)


class StoreStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"

class StoreStatus(SQLModel, table=True):
    __tablename__ = "store_status"
    id: int = Field(primary_key=True)
    store_id: str
    timestamp_utc: datetime = Column(DateTime(timezone=True))
    status: StoreStatusEnum

    __table_args__ = (
        Index("my_index", "timestamp_utc", "store_id"),
    )


class StoreTimezone(SQLModel, table=True):
    __tablename__ = "storetimezone"
    id: int = Field(default=None, primary_key=True)
    store_id: str
    timezone_str: str = Field(default="America/Chicago")