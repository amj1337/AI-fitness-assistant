# backend/schemas.py
from pydantic import BaseModel
from datetime import date

# User schemas
class UserBase(BaseModel):
    name: str
    email: str
    goals: str
    preferences: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# Workout schemas
class WorkoutBase(BaseModel):
    date: date
    type: str
    duration: int
    intensity: str

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

# DietLog schemas
class DietLogBase(BaseModel):
    date: date
    meal: str
    calories: int
    macros: str

class DietLogCreate(DietLogBase):
    pass

class DietLog(DietLogBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

# Progress schemas
class ProgressBase(BaseModel):
    date: date
    weight: float
    body_fat: float

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    user_id: int
    message: str