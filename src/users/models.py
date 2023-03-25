import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, TIMESTAMP
from sqlalchemy.orm import relationship

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


class CompanyRepresentativeModel(UserModel):
    from companies.models import CompanyModel

    __tablename__ = "company_representatives"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    birthdate = Column(Date, nullable=False)
    avatar = Column(String, nullable=True)

    company = relationship(CompanyModel, back_populates="representatives")

    __mapper_args__ = {
        "polymorphic_identity": UserType.company_representative
    }


class StudentModel(UserModel):
    __tablename__ = "students"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    birthdate = Column(Date, nullable=False)
    avatar = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": UserType.student
    }
