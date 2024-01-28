from sqlalchemy.orm import Session

from app.db.base_class import ModelType

FILE_PATH = "/app/app/files/"


def apply_changes(db: Session, db_item: ModelType) -> None:
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
