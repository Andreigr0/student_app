import enum

from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import TimestampMixin, EditorMixin


class ProjectParticipant(enum.Enum):
    Head = (1, 'Руководитель')
    Other = (2, 'Участник')


class ProjectRoleWorkFormatEnum(enum.Enum):
    FullDay = ('FullDay', 'Полный день')
    RemoteWork = ('RemoteWork', 'Удаленная работа')
    Flexible = ('Flexible', 'Гибкий график')


class ProjectStatusEnum(enum.Enum):
    Draft = (0, 'Черновик')
    Open = (1, 'Идёт набор')
    Completed = (2, 'Команда набрана')
    Done = (3, 'Проект завершен')
    Blocked = (4, 'Снят с публикации')

    # @classmethod
    # def active(cls) -> List[int]:
    #     return [cls.Open.value, cls.Completed.value, cls.Done.value]
    #
    # @classmethod
    # def get_transition_map(cls) -> Dict[int, List[int]]:
    #     return {
    #         cls.Draft.value: [cls.Open.value],
    #         cls.Open.value: [cls.Completed.value, cls.Blocked.value],
    #         cls.Completed.value: [cls.Open.value, cls.Done.value],
    #         cls.Done.value: [],
    #         cls.Blocked.value: [cls.Open.value],
    #     }


class ProjectTypeEnum(enum.Enum):
    Software = 0
    SoftwareAndHardware = 1
    Research = 2
    Startup = 3
    Internship = 4


class ProjectView(enum.Enum):
    DigitalAcademy = (0, 'Цифровая академия')
    AdvancedEngineeringSchool = (1, 'ПИШ (Передовая инженерная школа)')
    GPO = (2, 'ГПО')


class ProjectModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    name = Column(String(255), nullable=False)
    is_visible = Column(Boolean, default=True)
    type = Column(Enum(ProjectTypeEnum), nullable=False)
    view = Column(Enum(ProjectView), nullable=False)
    status = Column(Enum(ProjectStatusEnum), nullable=False)

    description = Column(String, nullable=False)
    problem = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    task = Column(String, nullable=False)
    result = Column(String, nullable=False)
    what_will_get = Column(String, nullable=False)

    total = Column(String)
    report = Column(String)
    reason_rejection = Column(String)
    application_date = Column(TIMESTAMP)

    company = relationship("CompanyModel", back_populates="projects")
    stages = relationship("ProjectStageModel", back_populates="project")
    managers = relationship("ProjectsManagersModel", back_populates="project")
    roles = relationship("ProjectRoleModel", back_populates="project")

    # report_periods = relationship("ProjectsReportPeriodsModel", back_populates="project")
    # subject_areas = relationship("SubjectArea", secondary="project_subject_area")
    # partners = relationship("Company", secondary="partners")
    # members = relationship("Member", back_populates="project")
    # bids = relationship("Bid", secondary="project_roles")
    # curator = relationship("Curator", back_populates="project")
    curators = relationship("ProjectsCuratorsModel", back_populates="project")


class ProjectStageModel(Base, TimestampMixin):  # todo: add UserMixin
    __tablename__ = "project_stage"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    name = Column(String, nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    finish_date = Column(TIMESTAMP, nullable=False)

    project = relationship(ProjectModel, back_populates="stages")


class ProjectsManagersModel(Base, TimestampMixin):
    __tablename__ = "project_managers"

    participant = Column(Enum(ProjectParticipant), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), primary_key=True)

    project = relationship(ProjectModel, back_populates="managers")
    contact = relationship("ContactModel", back_populates="projects")


class ProjectsCuratorsModel(Base):
    __tablename__ = "curators"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete='CASCADE'), primary_key=True)
    curator_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    project = relationship(ProjectModel, back_populates="curators")
    curator = relationship("UserModel", back_populates="curated_projects")


class ProjectRoleModel(Base):
    __tablename__ = "project_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    work_format = Column(Enum(ProjectRoleWorkFormatEnum), nullable=False)
    workload = Column(Integer, nullable=False)
    filename = Column(String)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("ProjectModel", back_populates="roles")

    need_competencies = relationship("CompetencyModel", secondary="project_role_need_competency")
    will_competencies = relationship("CompetencyModel", secondary='project_role_will_competency')


project_role_need_competency_association = Table(
    'project_role_need_competency',
    Base.metadata,
    Column('project_role_id', Integer, ForeignKey('project_roles.id'), primary_key=True),
    Column('competency_id', Integer, ForeignKey('competencies.id'), primary_key=True),
)

project_role_competency_association = Table(
    'project_role_will_competency',
    Base.metadata,
    Column('project_role_id', Integer, ForeignKey('project_roles.id')),
    Column('competency_id', Integer, ForeignKey('competencies.id')),
)
