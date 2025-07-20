# backend/models.py
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    goals = Column(String)
    preferences = Column(String)
    
    workouts = relationship("Workout", back_populates="user")
    diet_logs = relationship("DietLog", back_populates="user")
    progress = relationship("Progress", back_populates="user")

class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    type = Column(String(50))
    duration = Column(Integer)
    intensity = Column(String(50))
    
    user = relationship("User", back_populates="workouts")

class DietLog(Base):
    __tablename__ = "diet_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    meal = Column(String(100))
    calories = Column(Integer)
    macros = Column(String(100))
    
    user = relationship("User", back_populates="diet_logs")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    weight = Column(Float)
    body_fat = Column(Float)
    
    user = relationship("User", back_populates="progress")

