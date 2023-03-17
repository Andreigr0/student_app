from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey

from app.database import Base
import enum


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


class CompanyModel(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    has_accreditation = Column(Boolean, default=False)
    site = Column(String, nullable=True)
    description = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    inn = Column(Integer, nullable=True)
    employee_count = Column(Enum(CompanyEmployeeCount), nullable=False)
    status = Column(Enum(CompanyStatus), nullable=False, default=CompanyStatus.recent)
    reason_rejection = Column(String, nullable=True)

    # representative_id = Column(Integer, ForeignKey("representatives.id"), nullable=True)

    active_project_count = Column(Integer, default=0)

    # creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # updater_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(Integer, nullable=True)
    updated_at = Column(Integer, nullable=True)

    # search_vector = Column(
    #     TSVectorType("name", "description", "site"),
    #     nullable=True,
    #     index=True,
    # )

    # type_activities = relationship(
    #     "TypeActivity", secondary="company_type_activity", back_populates="companies"
    # )
    # subscribers = relationship(
    #     "Student", secondary="company_subscriber", back_populates="subscribed_companies"
    # )
    # projects = relationship("Project", back_populates="company")
    # contacts = relationship("Contact", back_populates="company")
    #
    # @classmethod
    # def by_id(cls, db, company_id: int):
    #     return db.query(cls).filter(cls.id == company_id).first()
    #
    # @classmethod
    # def by_email(cls, db, email: str):
    #     return db.query(cls).filter(cls.email == email).first()
    #
    # @classmethod
    # def by_representative_id(cls, db, representative_id: int):
    #     return db.query(cls).filter(cls.representative_id == representative_id).first()
    #
    # @classmethod
    # def by_active_status(cls, db):
    #     return db.query(cls).filter(cls.status == 1)
    #
    # @classmethod
    # def filter(cls, db, query_filter):
    #     return query_filter.apply(db.query(cls))
