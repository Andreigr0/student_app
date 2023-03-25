import enum

from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP

from app.database import Base


class UserType(str, enum.Enum):
    company_representative = "company_representative"
    student = "student"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(UserType), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email_verified_at = Column(TIMESTAMP, default=None, nullable=True)

    __mapper_args__ = {
        "polymorphic_on": type
    }
