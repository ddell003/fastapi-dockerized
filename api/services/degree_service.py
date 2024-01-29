from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models.models import Degree
from api.schemas.degree_schema import DegreeCreateSchema


def get_degrees(connection: Session):
    return connection.query(Degree).filter(Degree.deleted == False).all()


def create_degree(db: Session, create_data: DegreeCreateSchema):
    item = Degree(**create_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_degree(db, degree_id):
    return db.query(Degree).filter(Degree.id == degree_id).first()


def update(db, degree_id, data):
    degree = get_degree(db, degree_id)
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")

    degree.name = data.name
    db.commit()
    """
    Updates a user
    """
    return degree


def delete(db, degree_id):
    degree = get_degree(db, degree_id)
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")

    degree.deleted = True
    db.commit()
    return True
