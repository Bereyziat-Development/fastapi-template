import re

from sqlalchemy.orm import Session

from app.db.base_class import ModelType

FILE_PATH = "/app/app/files/"


def apply_changes(db: Session, db_item: ModelType) -> None:
    db.add(db_item)
    db.commit()
    db.refresh(db_item)


def to_snake_case(class_name):
    # Insert an underscore between two consecutive uppercase letters or lowercase followed by uppercase
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", class_name)
    # Insert an underscore between lowercase and uppercase
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
