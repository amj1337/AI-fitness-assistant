from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import ProgressCreate, Progress
from backend.crud import create_progress, get_progress

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/", response_model=Progress)
def create_progress_entry_for_user(
    progress: ProgressCreate,
    user_id: int,  # Will come from authentication later
    db: Session = Depends(get_db)
):
    return create_progress(db=db, progress=progress, user_id=user_id)

@router.get("/{progress_id}", response_model=Progress)
def read_progress_entry(progress_id: int, db: Session = Depends(get_db)):
    db_progress = get_progress(db, progress_id=progress_id)
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    return db_progress