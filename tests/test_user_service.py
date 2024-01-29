from sqlalchemy.orm import Session
from api.services.users import user_service as user_service
from tests.conftest import engine


def test_can_get_package_versions(client):
    db = Session(autocommit=False, autoflush=False, bind=engine)
    users = user_service.get_users(db)
    db.close()
    assert len(users) > 0
