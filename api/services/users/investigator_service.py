from fastapi import HTTPException
from sqlalchemy.orm import Session, with_polymorphic

from api.helpers.utils import unique_id
from api.models.enums import UserType, UserContactType
from api.models.models import Investigator, Address, User, Email, Fax, Phone


def create(db: Session, create_data):
    user_data = {
        "first_name": create_data.first_name,
        "last_name": create_data.last_name,
        "middle_name": create_data.middle_name,
        "username": create_data.username,
        "password": create_data.password,
        "type": UserType.investigator
    }

    if create_data.address:
        address = Address(**create_data.address.dict())
        db.add(address)
        db.commit()
        db.refresh(address)
        user_data["address_id"] = address.id

    if not user_data["username"]:
        user_data["username"] = unique_id()
    if not user_data["password"]:
        user_data["password"] = unique_id()

    investigator = Investigator(**user_data)

    db.add(investigator)
    db.commit()
    db.refresh(investigator)

    if create_data.emails:
        for item in create_data.emails:
            create_user_contact(db, Email(**item.dict()), UserContactType.email, investigator.id)

        for item in create_data.fax_numbers:
            create_user_contact(db, Fax(**item.dict()), UserContactType.fax, investigator.id)

        for item in create_data.phone_numbers:
            create_user_contact(db, Phone(**item.dict()), UserContactType.phone, investigator.id)


    return investigator


def create_user_contact(db, new_item, type, user_id):
    new_item.type = type
    new_item.user_id = user_id
    db.add(new_item)
    db.commit()


def get_list(db):
    query = db.query(with_polymorphic(User, [Investigator]))
    query = query.join(Investigator.address, aliased=True, isouter=True)
    query = query.join(User.contacts, aliased=True, isouter=True)
    query = query.filter(User.deleted.is_(False)).all()

    return query


def get(db, item_id):
    return db.query(with_polymorphic(User, [Investigator])).filter(Investigator.id == item_id).first()


def delete(db, item_id):
    user = get(db, item_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted = True
    db.commit()
    return True
