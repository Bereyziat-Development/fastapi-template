from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4


# Shared properties
class FileBase(BaseModel):
    name: Optional[str] = None
    mime_type: Optional[str] = "application/pdf"


# Properties to receive via API on creation
class FileCreate(FileBase):
    pass


# Properties to receive via API on update
class FileUpdate(FileBase):
    pass


class FileInDBBase(FileBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4


# Additional properties to return via API
class File(FileInDBBase):
    pass


# Additional properties stored in DB
class FileInDB(FileInDBBase):
    user_id: Optional[UUID4] = None
    client_with_picture_id: Optional[UUID4] = None
    client_under_contract_id: Optional[UUID4] = None
    filename: Optional[str] = "file_64735.pdf"
