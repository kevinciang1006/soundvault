from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.db import get_db
from models.schemas import Sample, SampleResponse, SamplesListResponse, PlayCountResponse

router = APIRouter()


@router.get("/api/samples", response_model=SamplesListResponse)
def get_samples(
    genre: Optional[str] = Query(None),
    bpm_min: float = Query(0),
    bpm_max: float = Query(300),
    key: Optional[str] = Query(None),
    sample_type: Optional[str] = Query(None),
    pack_id: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    sort: str = Query("trending"),
    limit: int = Query(20),
    offset: int = Query(0),
    db: Session = Depends(get_db),
):
    query = db.query(Sample)

    if genre:
        query = query.filter(Sample.genre == genre)
    if bpm_min > 0:
        query = query.filter(Sample.bpm >= bpm_min)
    if bpm_max < 300:
        query = query.filter(Sample.bpm <= bpm_max)
    if key:
        query = query.filter(Sample.key == key)
    if sample_type:
        query = query.filter(Sample.sample_type == sample_type)
    if pack_id is not None:
        query = query.filter(Sample.pack_id == pack_id)
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            Sample.filename.ilike(search_term) |
            Sample.pack_name.ilike(search_term) |
            Sample.genre.ilike(search_term)
        )

    if sort == "trending":
        query = query.order_by(Sample.play_count.desc())
    elif sort == "newest":
        query = query.order_by(Sample.created_at.desc())
    elif sort == "bpm_asc":
        query = query.order_by(Sample.bpm.asc())
    elif sort == "bpm_desc":
        query = query.order_by(Sample.bpm.desc())
    else:
        query = query.order_by(Sample.play_count.desc())

    total = query.count()
    samples = query.offset(offset).limit(limit).all()

    return SamplesListResponse(total=total, samples=samples)


@router.get("/api/samples/{sample_id}", response_model=SampleResponse)
def get_sample(sample_id: int, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    return sample


@router.post("/api/samples/{sample_id}/play", response_model=PlayCountResponse)
def increment_play_count(sample_id: int, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    sample.play_count += 1
    db.commit()
    db.refresh(sample)
    return PlayCountResponse(play_count=sample.play_count)
