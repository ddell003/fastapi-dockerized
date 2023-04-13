from sqlalchemy.orm import Session
from api.schemas.role import RoleCreateSchema
from tests.conftest import engine
from api.services import role as role_service


def test_can_create_role(client):

    role_data = {
        "name": "admin",
        "active": True,
    }
    db = Session(autocommit=False, autoflush=False, bind=engine)
    new_role = role_service.create_role(db, RoleCreateSchema(**role_data))
    db.close()
    assert role_data["name"] == new_role.name


def test_can_get_roles(client):
    db = Session(autocommit=False, autoflush=False, bind=engine)
    roles = role_service.get_roles(db)
    db.close()
    assert len(roles) > 0


def test_connect_user_roles(client):
    role_data = {
        "name": "role1",
        "active": True,
    }
    db = Session(autocommit=False, autoflush=False, bind=engine)
    new_role = role_service.create_role(db, RoleCreateSchema(**role_data))
    db.close()

    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0

    db = Session(autocommit=False, autoflush=False, bind=engine)
    role_service.connect_users(
        db, user_id=response.json()["data"][0]["id"], role_id=new_role.id
    )
    db.close()
