from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

from .archivable import Archivable


class Item(Base, Archivable):
    name = Column(String)
    description = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))
