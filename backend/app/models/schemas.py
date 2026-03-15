from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

from database.db import Base


# SQLAlchemy ORM Models

class Pack(Base):
    __tablename__ = "packs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    creator = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    sample_count = Column(Integer, default=0)
    cover_color = Column(String, nullable=False)
    cover_color_2 = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Sample(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)
    pack_id = Column(Integer, nullable=False)
    pack_name = Column(String, nullable=False)
    pack_creator = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    sample_type = Column(String, nullable=False)  # loop, one_shot, vocal, fx
    bpm = Column(Float, nullable=False)
    key = Column(String, nullable=False)
    duration_seconds = Column(Float, nullable=False)
    is_premium = Column(Boolean, default=False)
    play_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


# Pydantic Response Models

class PackResponse(BaseModel):
    id: int
    name: str
    creator: str
    genre: str
    sample_count: int
    cover_color: str
    cover_color_2: str

    class Config:
        from_attributes = True


class SampleResponse(BaseModel):
    id: int
    pack_id: int
    pack_name: str
    pack_creator: str
    filename: str
    genre: str
    sample_type: str
    bpm: float
    key: str
    duration_seconds: float
    is_premium: bool
    play_count: int

    class Config:
        from_attributes = True


class SamplesListResponse(BaseModel):
    total: int
    samples: List[SampleResponse]


class AnalysisResponse(BaseModel):
    bpm: float
    key: str
    duration_seconds: float
    filename: str


class PlayCountResponse(BaseModel):
    play_count: int
