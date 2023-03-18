from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
import enum

from app.utils import TimestampMixin, EditorMixin


class CompanyEmployeeCount(enum.Enum):
    small = (0, '<20')
    middle = (1, '21-50')
    large = (2, '51-100')
    huge = (3, '>100')


class CompanyStatus(enum.Enum):
    recent = (0, 'Новая')
    active = (1, 'Активна')
    moderation = (2, 'На модерации')
    requestToDelete = (3, 'На удалении')
    deleted = (4, 'Удалена')
    blocked = (5, 'Заблокирована')


class CompanyModel(Base, TimestampMixin):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True)
    name = Column(String, nullable=False)
    inn = Column(Integer, nullable=True, unique=True)
    has_accreditation = Column(Boolean, default=False, nullable=False)
    site = Column(String)
    logo = Column(String)
    description = Column(String)
    employee_count = Column(Enum(CompanyEmployeeCount), nullable=False)
    status = Column(Enum(CompanyStatus), nullable=False, default=CompanyStatus.recent)
    reason_rejection = Column(String)
    active_project_count = Column(Integer, default=0)

    contacts = relationship('ContactModel', back_populates="company")
    subscribers = relationship('CompaniesSubscribersModel', back_populates="company")

    # type_activities = relationship(
    #     "TypeActivity", secondary="company_type_activity", back_populates="companies"
    # )
    # projects = relationship("Project", back_populates="company")


class ContactCommunicationType(str, enum.Enum):
    phone = "phone"
    email = "email"
    telegram = "telegram"


class ContactModel(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, nullable=False)
    email = Column(String, nullable=True)
    position = Column(String, nullable=True)
    telegram = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    communication_type = Column(Enum(ContactCommunicationType), nullable=True)

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship(CompanyModel, back_populates='contacts')

    # creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    # updater_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    # created_at = Column(Integer)
    # updated_at = Column(Integer)


class CompaniesSubscribersModel(Base):
    __tablename__ = "company_subscriber"

    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)

    company = relationship(CompanyModel, back_populates='subscribers')
    student = relationship('StudentModel', back_populates='subscribed_companies')


class TypeActivityModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = "type_activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # students = relationship("Student", back_populates="type_activity")
