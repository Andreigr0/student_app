from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, object_session

from app.database import Base
from projects.models import ProjectsCompaniesModel, ProjectStatus, ProjectModel, ProjectCompanyType
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
    site = Column(String, nullable=False)

    projects = relationship("ProjectsCompaniesModel", back_populates="company")
    competencies = relationship("CompetencyModel", secondary=companies_competencies)

    @property
    def active_projects_count(self):
        return (
            object_session(self)
            .query(func.count('*'))
            .select_from(ProjectsCompaniesModel.__table__)
            .where(ProjectsCompaniesModel.company_id == self.id)
            .join(ProjectModel, ProjectsCompaniesModel.project_id == ProjectModel.id)
            .where(ProjectsCompaniesModel.type == ProjectCompanyType.organizer)
            .where(ProjectModel.status.in_([ProjectStatus.under_recruitment, ProjectStatus.recruited]))
            .scalar()
        )

    @property
    def total_projects_count(self):
        return (
            object_session(self)
            .query(func.count('*'))
            .select_from(ProjectsCompaniesModel.__table__)
            .where(ProjectsCompaniesModel.company_id == self.id)
            .join(ProjectModel, ProjectsCompaniesModel.project_id == ProjectModel.id)
            .where(ProjectsCompaniesModel.type == ProjectCompanyType.organizer)
            .scalar()
        )

    representatives = relationship("CompanyRepresentativeModel", back_populates="company")
    proj = association_proxy("projects", "project")


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
