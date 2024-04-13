from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Item, User
from app.schemas import ItemCreate, ItemUpdate

from .base import apply_changes


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ItemCreate, user: Optional[User]
    ) -> Item:
        db_item = self.create(db, obj_in=obj_in)
        db_item.user_id = user.id
        apply_changes(db, db_item)
        return db_item

    def get_multi_by_user(
        self, db: Session, *, user: User, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(self.model)
            .filter(Item.user_id == user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


item = CRUDItem(Item)
