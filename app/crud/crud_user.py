from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app.core.security import (
    generate_sso_confirmation_code,
    get_password_hash,
    verify_password,
)
from app.crud.base import CRUDBase
from app.models import Provider, Role, User
from app.schemas import UserCreate, UserUpdate

from .base import apply_changes


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(
        self, db: Session, *, email: str, with_archived: Optional[bool] = False
    ) -> Optional[User]:
        query = db.query(User).filter(User.email == email)
        query = self.filter_archivable(query, with_archived)
        return query.first()

    def get_by_sso_provider_id(
        self,
        db: Session,
        *,
        sso_provider_id: str,
        provider: Provider,
        with_archived: Optional[bool] = False
    ) -> Optional[User]:
        assert (
            provider != Provider.EMAIL
        ), "Email provider is not stored with an sso_provider_id"
        query = (
            db.query(User)
            .filter(User.sso_provider_id == sso_provider_id)
            .filter(User.provider == provider)
        )
        query = self.filter_archivable(query, with_archived)
        return query.first()

    def create(
        self, db: Session, *, obj_in: UserCreate, role: Optional[Role] = Role.CUSTOMER
    ) -> User:
        obj_in_data: dict = jsonable_encoder(obj_in)
        password = obj_in_data.pop("password", None)
        sso_provider_id = obj_in_data.pop("sso_provider_id", None)
        provider: Provider = obj_in.provider
        if provider == Provider.EMAIL:
            assert (
                password is not None
            ), "Invalid arguments for an Email user, missing password in UserCreate"
        else:
            assert (
                sso_provider_id is not None
            ), "Invalid arguments for an SSO user, missing sso_provider_id in UserCreate"

        password_hash = (
            get_password_hash(password) if provider == Provider.EMAIL else None
        )

        db_obj = User(
            **obj_in_data,
            role=role,
            password_hash=password_hash,
            sso_provider_id=sso_provider_id
        )  # type: ignore

        apply_changes(db, db_obj)
        return db_obj

    def update_password(self, db: Session, *, db_obj: User, new_password: str) -> User:
        db_obj.password_hash = get_password_hash(new_password)
        apply_changes(db, db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def get_by_sso_confirmation_code(
        self,
        db: Session,
        user_id: UUID4,
        sso_confirmation_code: str,
        with_archived: Optional[bool] = False,
    ) -> Optional[User]:
        user = self.get(db, id=user_id, with_archived=with_archived)
        if user.sso_confirmation_code != sso_confirmation_code:
            return None
        return user

    def update_sso_confirmation_code(self, db: Session, user: User) -> User:
        user.sso_confirmation_code = generate_sso_confirmation_code()
        apply_changes(db, user)
        return user


user = CRUDUser(User)
