from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas import RoleSchema
from api.services import role as role_service

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=List[RoleSchema])
def get_roles(db: Session = Depends(get_db)) -> List[RoleSchema]:
    """
    Gets the full list of roles
    """
    return role_service.get_roles(db)
