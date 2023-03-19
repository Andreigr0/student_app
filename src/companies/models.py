from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, func, select
from sqlalchemy.orm import relationship, column_property

from app.database import Base
import enum

from app.utils import TimestampMixin, EditorMixin
from projects.models import ProjectModel


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


class CompanyModel(Base, TimestampMixin, EditorMixin):
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
    type_activities = relationship("CompanyTypeActivitiesModel", back_populates="company")
    projects = relationship("ProjectModel", back_populates="company")

    total_project_count = column_property(
        select(func.count(ProjectModel.id))
        .where(ProjectModel.company_id == id)
        .scalar_subquery()
    )


class ContactCommunicationType(str, enum.Enum):
    phone = "phone"
    email = "email"
    telegram = "telegram"


class ContactModel(Base, TimestampMixin, EditorMixin):
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
    projects = relationship("ProjectsManagersModel", back_populates="contact")


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

    companies = relationship("CompanyTypeActivitiesModel", back_populates="type_activity")
    # students = relationship("Student", back_populates="type_activity")


class CompanyTypeActivitiesModel(Base):
    __tablename__ = "company_type_activity"

    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    type_activity_id = Column(Integer, ForeignKey('type_activity.id'), primary_key=True)

    company = relationship(CompanyModel, back_populates='type_activities')
    type_activity = relationship(TypeActivityModel, back_populates='companies')
