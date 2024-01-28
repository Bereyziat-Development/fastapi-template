from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserCreate, UserUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "password_hash")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(db, email=email, password=password)
    assert user is None


def test_get_user(db: Session) -> None:
    user = create_random_user(db)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    user = create_random_user(db)
    new_email = random_email()
    new_first_name = random_lower_string()
    new_last_name = random_lower_string()
    user_in_update = UserUpdate(
        email=new_email, first_name=new_first_name, last_name=new_last_name
    )
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2 is not None
    assert user.id == user_2.id
    assert user_2.email == new_email
    assert user_2.first_name == new_first_name
    assert user_2.last_name == new_last_name


def test_archive_user(db: Session) -> None:
    user = create_random_user(db)
    archived_user = crud.user.archive(db, obj=user)
    assert archived_user is not None
    assert archived_user.archived is True
    assert archived_user.id == user.id


def test_unarchive_user(db: Session) -> None:
    user = create_random_user(db)
    archived_user = crud.user.archive(db, obj=user)
    assert archived_user is not None
    assert archived_user.archived is True
    assert archived_user.id == user.id
    unarchived_user = crud.user.unarchive(db, obj=archived_user)
    assert unarchived_user is not None
    assert unarchived_user.archived is False
    assert unarchived_user.id == user.id
