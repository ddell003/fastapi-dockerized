import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.specialty_schema import SpecialtyListSchema, SpecialtySchema, SpecialtyCreateSchema, \
    SpecialtyPutRequestSchema
from api.services import specialty_service

router = APIRouter(prefix="/specialties", tags=["specialties"])


@router.get("", response_model=SpecialtyListSchema)
def get_specialties(db: Session = Depends(get_db)) -> SpecialtyListSchema:
    """
    Gets the full list of Specialties
    """
    items = specialty_service.get_list(db)
    return SpecialtyListSchema(data=items, total_count=len(items))


@router.get("/{item_id}", response_model=SpecialtySchema)
def get_specialty(item_id: uuid.UUID, db: Session = Depends(get_db)) -> SpecialtySchema:
    item = specialty_service.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Degree not found")

    return item


@router.post("", response_model=SpecialtySchema)
def create_specialty(
        data: SpecialtyCreateSchema, db: Session = Depends(get_db)
) -> SpecialtySchema:
    item = specialty_service.create(db, data)
    return item


@router.put("/{degree_id}", response_model=SpecialtySchema)
def update_specialty(
        degree_id: uuid.UUID, data: SpecialtyPutRequestSchema, db: Session = Depends(get_db)
) -> SpecialtySchema:
    return specialty_service.update(db, degree_id, data)


@router.delete("/{degree_id}", status_code=204)
def delete_specialty(degree_id: uuid.UUID, db: Session = Depends(get_db)):
    specialty_service.delete(db, degree_id)
