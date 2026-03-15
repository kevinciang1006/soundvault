from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.schemas import Pack, PackResponse

router = APIRouter()


@router.get("/api/packs", response_model=List[PackResponse])
def get_packs(db: Session = Depends(get_db)):
    packs = db.query(Pack).order_by(Pack.id).all()
    return packs
