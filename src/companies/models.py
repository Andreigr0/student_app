from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.orm import relationship

from app.database import Base
from users.models import UserModel, UserType

companies_competencies = Table(
    "companies_competencies",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("competency_id", Integer, ForeignKey("competencies.id"), primary_key=True),
)


class CompanyModel(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    description = Column(String, nullable=False)
    has_accreditation = Column(Boolean, nullable=False, default=False)

    projects = relationship("ProjectsCompaniesModel", back_populates="company")
    competencies = relationship("CompetencyModel", secondary=companies_competencies)

    # # Calculated fields: active projects count, total projects count
    # active_projects_count = Column(Integer, nullable=False, default=0)
    # total_projects_count = Column(Integer, nullable=False, default=0)

    representatives = relationship("CompanyRepresentativeModel", back_populates="company")


class CompanyRepresentativeModel(UserModel):
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
