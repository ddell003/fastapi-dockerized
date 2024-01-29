import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.network_schema import NetworkListSchema, NetworkSchema, NetworkCreateSchema, NetworkPutRequestSchema
from api.services import network_service

router = APIRouter(prefix="/networks", tags=["networks"])


@router.get("", response_model=NetworkListSchema)
def get_networks(db: Session = Depends(get_db)) -> NetworkListSchema:
    """
    Gets the full list of networks
    """
    items = network_service.get_list(db)
    return NetworkListSchema(data=items, total_count=len(items))


@router.get("/{item_id}", response_model=NetworkSchema)
def get_network(item_id: uuid.UUID, db: Session = Depends(get_db)) -> NetworkSchema:
    item = network_service.get(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.post("", response_model=NetworkSchema)
def create_network(data: NetworkCreateSchema, db: Session = Depends(get_db)) -> NetworkSchema:
    item = network_service.create(db, data)
    return item


@router.put("/{network_id}", response_model=NetworkSchema)
def update_network(item_id: uuid.UUID, data: NetworkPutRequestSchema, db: Session = Depends(get_db)) -> NetworkSchema:
    return network_service.update(db, item_id, data)


@router.delete("/{item_id}", status_code=204)
def delete_degree(item_id: uuid.UUID, db: Session = Depends(get_db)):
    network_service.delete(db, item_id)
