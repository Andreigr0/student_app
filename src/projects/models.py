import enum

from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey, Boolean, Table, and_
from sqlalchemy.orm import relationship

from app.database import Base


class ProjectStatus(str, enum.Enum):
    """Статус проекта (Черновик, Идёт набор, Команда набрана, Завершен, Снят с публикации)"""
    draft = 'draft'
    under_recruitment = 'under_recruitment'
    recruited = 'recruited'
    finished = 'finished'
    withdrawn = 'withdrawn'


class ProjectType(str, enum.Enum):
    """Тип проекта (Стартап, Стажировка, Научно-исследовательский)"""
    startup = 'startup'
    internship = 'internship'
    research = 'research'
    software = 'software'
    software_and_hardware = 'software_and_hardware'


class WorkFormat(str, enum.Enum):
    """Формат работы (полный день, удаленная работа, гибкий график)"""
    full_time = 'full_time'
    remote = 'remote'
    flexible = 'flexible'


class ProjectKind(str, enum.Enum):
    """Вид проекта (Цифровая академия, Передовая инженерная школа (ПИШ), Государственная проектная организация (ГПО))"""
    digital_academy = 'digital_academy'
    pish = 'pish'
    gpo = 'gpo'


class ProjectPosition(str, enum.Enum):
    """Должность в проекте"""
    student = 'student'
    curator = 'curator'
    company = 'company'


project_competencies = Table(
    "project_competencies",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("competency_id", Integer, ForeignKey("competencies.id"), primary_key=True),
)


class ProjectStageModel(Base):
    __tablename__ = "project_stages"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)

    project = relationship("ProjectModel", back_populates="stages")
    reports = relationship("ReportModel", back_populates="stage")


project_roles_needed_competencies = Table(
    "project_roles_needed_competencies",
    Base.metadata,
    Column("project_role_id", Integer, ForeignKey("project_roles.id"), primary_key=True),
    Column("competency_id", Integer, ForeignKey("competencies.id"), primary_key=True),
)

project_roles_acquired_competencies = Table(
    "project_roles_acquired_competencies",
    Base.metadata,
    Column("project_role_id", Integer, ForeignKey("project_roles.id"), primary_key=True),
    Column("competency_id", Integer, ForeignKey("competencies.id"), primary_key=True),
)


class ProjectRoleModel(Base):
    __tablename__ = "project_roles"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    work_load = Column(String, nullable=False)
    work_format = Column(Enum(WorkFormat), nullable=False)

    needed_competencies = relationship("CompetencyModel", secondary=project_roles_needed_competencies)
    acquired_competencies = relationship("CompetencyModel", secondary=project_roles_acquired_competencies)

    project = relationship("ProjectModel", back_populates="roles")
    members = relationship("ProjectsMembersModel", back_populates="role")
    reviews = relationship("ReviewModel", back_populates="role")


class ProjectTeamStatus(str, enum.Enum):
    accepted = "accepted"
    rejected = "rejected"
    refused_invitation = "refused_invitation"
    withdrawn = "withdrawn"
    applied = "applied"


class ProjectsMembersModel(Base):
    __tablename__ = "projects_members"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("project_roles.id"), nullable=True)

    user = relationship("UserModel", back_populates="projects")
    project = relationship("ProjectModel", back_populates="team")
    role = relationship("ProjectRoleModel", back_populates="members")

    description = Column(String, nullable=False)
    position = Column(Enum(ProjectPosition), nullable=False)
    status = Column(Enum(ProjectTeamStatus), nullable=False)


class ProjectCompanyType(str, enum.Enum):
    """Тип компании в проекте (Организатор, Партнер)"""
    organizer = "organizer"
    partner = "partner"


class ProjectsCompaniesModel(Base):
    __tablename__ = "projects_companies"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), primary_key=True)

    project = relationship("ProjectModel", back_populates="projects_companies")
    company = relationship("CompanyModel", back_populates="projects_companies")
    type = Column(Enum(ProjectCompanyType), nullable=False)


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(Enum(ProjectStatus), nullable=False)
    start_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)

    type = Column(Enum(ProjectType), nullable=True)
    kind = Column(Enum(ProjectKind), nullable=True)
    is_only_for_digital_academy = Column(Boolean, nullable=False, default=False)
    description = Column(String, nullable=False)

    solving_problems = Column(String, nullable=False)
    goals = Column(String, nullable=False)
    tasks = Column(String, nullable=False)
    results = Column(String, nullable=False)
    what_will_participant_get = Column(String, nullable=False)

    stages = relationship(ProjectStageModel, back_populates="project")
    roles = relationship(ProjectRoleModel, back_populates="project")
    competencies = relationship("CompetencyModel", secondary=project_competencies, back_populates="projects")
    projects_companies = relationship(ProjectsCompaniesModel, back_populates="project")

    team = relationship(ProjectsMembersModel, back_populates="project")

    organizers = relationship(
        ProjectsCompaniesModel,
        primaryjoin=and_(ProjectsCompaniesModel.project_id == id,
                         ProjectsCompaniesModel.type == ProjectCompanyType.organizer))

    @property
    def company(self):
        return self.organizers[0].company if self.organizers else None
