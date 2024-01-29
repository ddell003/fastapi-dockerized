from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models.models import Specialty
from api.schemas.specialty_schema import SpecialtyCreateSchema


def get_list(connection: Session):
    return connection.query(Specialty).filter(Specialty.deleted == False).all()


def create(db: Session, create_data: SpecialtyCreateSchema):
    item = Specialty(**create_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get(db, id):
    return db.query(Specialty).filter(Specialty.id == id).first()


def update(db, id, data):
    degree = get(db, id)
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")

    degree.name = data.name
    db.commit()
    """
    Updates a user
    """
    return degree


def delete(db, degree_id):
    degree = get(db, degree_id)
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")

    degree.deleted = True
    db.commit()
    return True
