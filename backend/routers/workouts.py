from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import WorkoutCreate, Workout
from backend.crud import create_workout, get_workout

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post("/", response_model=Workout)
def create_workout_for_user(
    workout: WorkoutCreate, 
    user_id: int,  # Assuming you'll get user_id from auth later
    db: Session = Depends(get_db)
):
    return create_workout(db=db, workout=workout, user_id=user_id)

@router.get("/{workout_id}", response_model=Workout)
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    db_workout = get_workout(db, workout_id=workout_id)
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return db_workout