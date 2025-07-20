from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import DietLogCreate, DietLog
from backend.crud import create_diet_log, get_diet_log

router = APIRouter(prefix="/diet", tags=["diet"])

@router.post("/", response_model=DietLog)
def create_diet_entry_for_user(
    diet_log: DietLogCreate,
    user_id: int,  # Will come from authentication later
    db: Session = Depends(get_db)
):
    return create_diet_log(db=db, diet_log=diet_log, user_id=user_id)

@router.get("/{diet_log_id}", response_model=DietLog)
def read_diet_entry(diet_log_id: int, db: Session = Depends(get_db)):
    db_diet_log = get_diet_log(db, diet_log_id=diet_log_id)
    if db_diet_log is None:
        raise HTTPException(status_code=404, detail="Diet entry not found")
    return db_diet_log