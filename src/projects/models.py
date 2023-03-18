import enum

from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import TimestampMixin


class ProjectParticipant(enum.Enum):
    Head = (1, 'Руководитель')
    Other = (2, 'Участник')


class ProjectRoleCompetenceType(enum.Enum):
    NeedTo = (0, 'Требуемые навыки')
    WillBe = (1, 'Навыки, которые получит студент по итогам проекта')


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


class ProjectModel(Base, TimestampMixin):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    # company_id = Column(Integer, ForeignKey('companies.id'))

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

    # creator_id = Column(Integer)
    # updater_id = Column(Integer)

    stages = relationship("ProjectStageModel", back_populates="project")
    # company = relationship("Company", back_populates="projects")
    # subject_areas = relationship("SubjectArea", secondary="project_subject_area")
    # partners = relationship("Company", secondary="partners")
    # roles = relationship("ProjectRole", back_populates="project")
    # report_periods = relationship("ProjectReportPeriod", back_populates="project")
    # members = relationship("Member", back_populates="project")
    # bids = relationship("Bid", secondary="project_roles")
    # curator = relationship("Curator", back_populates="project")


class ProjectStageModel(Base, TimestampMixin):  # todo: add UserMixin
    __tablename__ = "project_stage"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    name = Column(String, nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    finish_date = Column(TIMESTAMP, nullable=False)

    project = relationship(ProjectModel, back_populates="stages")
