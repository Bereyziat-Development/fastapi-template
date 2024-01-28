from datetime import datetime
from typing import Optional


class Archivable:
    archived_at: Optional[datetime]
    archived: Optional[bool]
