from sqlalchemy import Column, func, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())


@declarative_mixin
class EditorMixin:
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    updater_id = Column(Integer, ForeignKey('users.id'), nullable=True)
