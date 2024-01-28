from app.models import File
from app.schemas.file import FileCreate, FileUpdate

from .base import CRUDBase

file = CRUDBase[File, FileCreate, FileUpdate](File)
