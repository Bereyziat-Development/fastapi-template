from enum import Enum
from typing import TYPE_CHECKING, Literal, Optional

from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from .archivable import Archivable

if TYPE_CHECKING:
    from .file import File  # noqa: F401
    from .item import Item  # noqa: F401


class Language(str, Enum):
    EN = "en"
    FR = "fr"


DEFAULT_LANGUAGE = Language.EN


class Role(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    CUSTOMER = "customer"


class Provider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"


# Modify this to match the SSO providers you are using in your project
SSOProvider = Literal[Provider.GOOGLE, Provider.FACEBOOK, Provider.GITHUB]


class User(Base, Archivable):
    # Override the table name to avoid any confusion with SQL reserved word "user" during generated migration scripts
    __tablename__ = "person"
    # Authentication
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String)
    role = Column(String, default=Role.CUSTOMER, nullable=False)
    language = Column(String, default=DEFAULT_LANGUAGE, nullable=False)
    confirmed = Column(Boolean, default=False)
    sso_confirmation_code = Column(String)
    # Personal information
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    postcode = Column(String)
    state = Column(String)
    provider = Column(String, default=Provider.EMAIL, nullable=False)
    sso_provider_id = Column(String, index=True)
    profile_pic = relationship(
        "File", backref="user", uselist=False, cascade="all, delete"
    )
    items = relationship("Item", backref="user", lazy="dynamic", cascade="all, delete")

    @hybrid_property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    @hybrid_property
    def is_moderator(self) -> bool:
        return self.role == Role.MODERATOR

    @hybrid_property
    def is_customer(self) -> bool:
        return self.role == Role.CUSTOMER

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def profile_picture_url(self) -> Optional[str]:
        return (
            self.profile_pic.user_profile_pic_url
            if self.profile_pic is not None
            else None
        )
