from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models.models import Network
from api.schemas.network_schema import NetworkCreateSchema


def get_list(connection: Session):
    return connection.query(Network).filter(Network.deleted == False).all()


def create(db: Session, create_data: NetworkCreateSchema):
    item = Network(**create_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get(db, id):
    return db.query(Network).filter(Network.id == id).first()


def update(db, id, data):
    item = get(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Degree not found")

    item.name = data.name
    db.commit()
    """
    Updates a user
    """
    return item


def delete(db, degree_id):
    degree = get(db, degree_id)
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")

    degree.deleted = True
    db.commit()
    return True
