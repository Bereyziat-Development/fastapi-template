from sqlalchemy.orm import Session

from app import crud
from app.models import Item
from app.schemas import ItemCreate

from .utils import random_lower_string


def create_random_item(db: Session) -> Item:
    name = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(name=name, description=description)
    item = crud.item.create(db=db, obj_in=item_in)
    return item
