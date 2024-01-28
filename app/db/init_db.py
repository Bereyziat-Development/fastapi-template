from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.models.user import Role  # noqa: F401

# from app.db.session import engine
# from app.db import base

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # base.Base.metadata.create_all(bind=engine)
    # pass
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if user is None:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.user.create(db, obj_in=user_in, role=Role.ADMIN)  # noqa: F841
