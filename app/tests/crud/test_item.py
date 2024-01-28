from sqlalchemy.orm import Session

from app import crud
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_item(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    user = create_random_user(db)
    item = crud.item.create_with_user(db=db, obj_in=item_in, user=user)
    assert item.name == name
    assert item.description == description
    assert item.user_id == user.id


def test_get_item(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    user = create_random_user(db)
    item = crud.item.create_with_user(db=db, obj_in=item_in, user=user)
    stored_item = crud.item.get(db=db, id=item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.name == stored_item.name
    assert item.description == stored_item.description
    assert item.user_id == stored_item.user_id


def test_update_item(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    user = create_random_user(db)
    item = crud.item.create_with_user(db=db, obj_in=item_in, user=user)
    description2 = random_lower_string()
    item_update = ItemUpdate(description=description2)
    item2 = crud.item.update(db=db, db_obj=item, obj_in=item_update)
    assert item.id == item2.id
    assert item.name == item2.name
    assert item2.description == description2
    assert item.user_id == item2.user_id


def test_delete_item(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    user = create_random_user(db)
    item = crud.item.create_with_user(db=db, obj_in=item_in, user=user)
    item2 = crud.item.remove(db=db, obj=item)
    item3 = crud.item.get(db=db, id=item.id)
    assert item3 is None
    assert item2.id == item.id
    assert item2.name == name
    assert item2.description == description
    assert item2.user_id == user.id
