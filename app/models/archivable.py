from sqlalchemy import Column, DateTime
from sqlalchemy.ext.hybrid import hybrid_property


class Archivable:
    archived_at = Column(DateTime)

    @hybrid_property
    def archived(self) -> bool:
        return self.archived_at is not None

    @archived.expression
    def archived(cls):
        return cls.archived_at != None
