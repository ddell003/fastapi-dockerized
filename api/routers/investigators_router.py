import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.investigator_schema import InvestigatorCreateSchema, InvestigatorListSchema, InvestigatorSchema
from api.schemas.network_schema import NetworkListSchema, NetworkSchema, NetworkCreateSchema, NetworkPutRequestSchema
from api.services import network_service
from api.services.users import investigator_service

router = APIRouter(prefix="/investigators", tags=["investigators"])


#
@router.get("", response_model=InvestigatorListSchema)
def get_investigators(db: Session = Depends(get_db)):
    """
    Gets the full list of users
    """
    items = investigator_service.get_list(db)
    return InvestigatorListSchema(data=items, total_count=len(items))


@router.get("/{item_id}", response_model=InvestigatorSchema)
def get_investigator(item_id: uuid.UUID, db: Session = Depends(get_db)) -> InvestigatorSchema:
    item = investigator_service.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")

    return item


@router.post("", response_model=InvestigatorSchema, status_code=201)
def create_network(data: InvestigatorCreateSchema, db: Session = Depends(get_db)) -> InvestigatorSchema:
    item = investigator_service.create(db, data)
    return item


@router.put("/{network_id}", response_model=NetworkSchema)
def update_network(item_id: uuid.UUID, data: NetworkPutRequestSchema, db: Session = Depends(get_db)) -> NetworkSchema:
    return network_service.update(db, item_id, data)


@router.delete("/{item_id}", status_code=204)
def delete_investigator(item_id: uuid.UUID, db: Session = Depends(get_db)):
    investigator_service.delete(db, item_id)
