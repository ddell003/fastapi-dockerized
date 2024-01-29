import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.degree_schema import DegreeSchema, DegreeCreateSchema, DegreePutRequestSchema, DegreeListSchema
from api.services import degree_service

router = APIRouter(prefix="/degrees", tags=["degrees"])


@router.get("", response_model=DegreeListSchema)
def get_degrees(db: Session = Depends(get_db)) -> DegreeListSchema:
    """
    Gets the full list of degrees
    """
    items = degree_service.get_degrees(db)
    return DegreeListSchema(data=items, total_count=len(items))


@router.get("/{degree_id}", response_model=DegreeSchema)
def get_degree(degree_id: uuid.UUID, db: Session = Depends(get_db)) -> DegreeSchema:
    item = degree_service.get_degree(db, degree_id)
    if not item:
        raise HTTPException(status_code=404, detail="Degree not found")

    return item


@router.post("", response_model=DegreeSchema)
def create_degree(
        data: DegreeCreateSchema, db: Session = Depends(get_db)
) -> DegreeSchema:
    item = degree_service.create_degree(db, data)
    return item


@router.put("/{degree_id}", response_model=DegreeSchema)
def update_degree(
        degree_id: uuid.UUID, data: DegreePutRequestSchema, db: Session = Depends(get_db)
) -> DegreeSchema:
    return degree_service.update(db, degree_id, data)


@router.delete("/{degree_id}", status_code=204)
def delete_degree(degree_id: uuid.UUID, db: Session = Depends(get_db)):
    degree_service.delete(db, degree_id)
