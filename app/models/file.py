from typing import Optional

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.config import settings
from app.db.base_class import Base

from .archivable import Archivable


class File(Base, Archivable):
    # Name of the file to display for the user
    name = Column(String)
    mime_type = Column(String)
    # Name of the file in the filesystem on the server
    filename = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))

    @hybrid_property
    def file_path(self):
        return settings.FILE_PATH + self.filename

    @hybrid_property
    def user_profile_pic_url(self) -> Optional[str]:
        if self.user_id is not None:
            return f"{settings.SERVER_HOST}api/v1/ \
                users/{self.user_id}/profile-picture/{self.id}"
        return None
