# backend/crud.py
from sqlalchemy.orm import Session
from .models import User, Workout, DietLog, Progress
from .schemas import UserCreate, WorkoutCreate, DietLogCreate, ProgressCreate

# User CRUD
def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        goals=user.goals,
        preferences=user.preferences
    )
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e  

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Workout CRUD
def create_workout(db: Session, workout: WorkoutCreate, user_id: int):
    db_workout = Workout(**workout.dict(), user_id=user_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

def get_workout(db: Session, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()

def get_workouts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Workout).filter(Workout.user_id == user_id).offset(skip).limit(limit).all()

# DietLog CRUD
def create_diet_log(db: Session, diet_log: DietLogCreate, user_id: int):
    db_diet_log = DietLog(**diet_log.dict(), user_id=user_id)
    db.add(db_diet_log)
    db.commit()
    db.refresh(db_diet_log)
    return db_diet_log

def get_diet_log(db: Session, diet_log_id: int):
    return db.query(DietLog).filter(DietLog.id == diet_log_id).first()

def get_diet_logs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(DietLog).filter(DietLog.user_id == user_id).offset(skip).limit(limit).all()

# Progress CRUD
def create_progress(db: Session, progress: ProgressCreate, user_id: int):
    db_progress = Progress(**progress.dict(), user_id=user_id)
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def get_progress(db: Session, progress_id: int):
    return db.query(Progress).filter(Progress.id == progress_id).first()

def get_progress_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Progress).filter(Progress.user_id == user_id).offset(skip).limit(limit).all()