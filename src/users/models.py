from sqlalchemy import Column, Integer, String, TIMESTAMP

from app.database import Base
from app.utils import TimestampMixin


class UserModel(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email_verified_at = Column(TIMESTAMP, default=None, nullable=True)
