# from app.models.competence import competence_project_role
# from app.models.enums import ProjectRoleCompetenceType
# from app.models.mixins import TimestampMixin, UserStampMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Enum, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Curator(Base):
    __tablename__ = "curators"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    curator_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="curators")


# Index("invite_contingent_person_id_index", Invite.contingent_person_id)
# Index("invite_project_role_id_index", Invite.project_role_id)


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    projectId = Column(String)
    projectRoleId = Column(Integer)
    contingentPersonId = Column(Integer)
    creatorId = Column(Integer)
    updaterId = Column(Integer)
    createdAt = Column(Integer)
    updatedAt = Column(Integer)

    project = relationship('Project', back_populates='members')
    student = relationship('Student', back_populates='members')
    review = relationship('MemberReview', back_populates='member')

    project_role = relationship('ProjectRole', back_populates='members')

    @classmethod
    def by_project_id(cls, session, project_id):
        return session.query(cls).filter(cls.projectId == project_id)

    @classmethod
    def by_contingent_person_id(cls, session, contingent_person_id):
        return session.query(cls).filter(cls.contingentPersonId == contingent_person_id)


member_review_competence_table = Table(
    'member_review_competence',
    Base.metadata,
    Column('member_review_id', Integer, ForeignKey('member_reviews.id')),
    Column('competence_id', Integer, ForeignKey('competencies.id')),
)


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    name = Column(String(255))
    is_visible = Column(Boolean)
    type = Column(Integer)
    view = Column(Integer)
    description = Column(String)
    problem = Column(String)
    purpose = Column(String)
    task = Column(String)
    result = Column(String)
    what_will_get = Column(String)
    status = Column(Integer)
    total = Column(String)
    report = Column(String)
    reason_rejection = Column(String)
    application_date = Column(String)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    company = relationship("Company", back_populates="projects")
    subject_areas = relationship("SubjectArea", secondary="project_subject_area")
    partners = relationship("Company", secondary="partners")
    roles = relationship("ProjectRole", back_populates="project")
    stages = relationship("ProjectStage", back_populates="project")
    report_periods = relationship("ProjectReportPeriod", back_populates="project")
    members = relationship("Member", back_populates="project")
    bids = relationship("Bid", secondary="project_roles")
    curator = relationship("Curator", back_populates="project")


class ProjectParticipant(PyEnum):
    Head = 1
    Other = 2

    def label(self):
        return {
            self.Head: 'Руководитель',
            self.Other: 'Участник',
        }[self]


class ProjectManager(Base):
    __tablename__ = "project_managers"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    participant = Column(Enum(ProjectParticipant), nullable=False)
    created_at = Column(func.now())
    updated_at = Column(func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="managers")
    contact = relationship("Contact", back_populates="projects")


class ProjectReportPeriod(Base):
    __tablename__ = "project_report_periods"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    name = Column(String, index=True)
    start_date = Column(String, index=True)
    finish_date = Column(String, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    updater_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    created_at = Column(Integer, index=True)
    updated_at = Column(Integer, index=True)

    project = relationship("Project", back_populates="report_periods")
    student_reports = relationship("StudentReport", back_populates="period")

    @classmethod
    def get_waiting_student_reports(cls, db, contingent_person_id: int, filter: str = ""):
        query = (
            db.query(cls)
            .join("project")
            .outerjoin("student_reports")
            .filter(Project.contingent_person_id == contingent_person_id)
            .filter(cls.member_id.is_(None))
        )

        if filter == "all":
            date = text("CURRENT_DATE()")
            query = query.filter(
                text("(finish_date < :date OR (start_date <= :date AND finish_date >= :date))")).params(date=date)
        elif filter == "expired":
            query = query.filter(cls.finish_date < text("CURRENT_DATE()"))
        else:
            query = query.filter(cls.start_date <= text("CURRENT_DATE()")).filter(
                cls.finish_date >= text("CURRENT_DATE()"))

        return query.order_by(cls.finish_date)

    @classmethod
    def by_id(cls, db, id: int):
        return db.query(cls).filter(cls.id == id)

    @classmethod
    def by_project_id(cls, db, project_id: int):
        return db.query(cls).filter(cls.project_id == project_id)

    @classmethod
    def by_start_date(cls, db, date: str, operator: str):
        return db.query(cls).filter(text(f"start_date {operator} :date")).params(date=date)


class ProjectRoleCompetenceType(PyEnum):
    NeedTo = 0
    WillBe = 1

    def label(self):
        return {
            self.NeedTo: 'Требуемые навыки',
            self.WillBe: 'Навыки, которые получит студент по итогам проекта',
        }[self]


class ProjectRole(Base):
    __tablename__ = "project_roles"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    workload = Column(Integer)
    work_format = Column(Integer)

    type = Column(Enum(ProjectRoleCompetenceType), nullable=False)

    project = relationship("Project", back_populates="project_roles")
    need_competencies = relationship("Competence", secondary="project_role_competence",
                                     back_populates="need_project_roles")
    will_competencies = relationship("Competence", secondary="project_role_competence",
                                     back_populates="will_project_roles")
    role = relationship("Role", back_populates="project_roles")
    bids = relationship("Bid", back_populates="project_role")

    @staticmethod
    def suitable_by_contingent_person_id(company_id: int, contingent_person_id: int):
        # from app.models import Invite, Member, Project, ProjectRoleCompetenceType
        # from app.enums import InviteStatus, ProjectStatus

        status_list = [f"'{status}'" for status in InviteStatus.get_passives()]
        status_list = ",".join(status_list)

        return (
            ProjectRole.query
            .join(Project)
            .outerjoin(Invite, ((Invite.project_role_id == ProjectRole.id) & (
                    Invite.contingent_person_id == contingent_person_id)))
            .outerjoin(Member,
                       ((Member.project_id == Project.id) & (Member.contingent_person_id == contingent_person_id)))
            .filter(Member.id.is_(None))
            .filter(Project.company_id == company_id)
            .filter(Project.status == ProjectStatus.Open.value)
            .filter((Invite.contingent_person_id.is_(None)) | (Invite.status.in_(status_list)))
        )

    @staticmethod
    def by_id(project_role_id: int):
        return ProjectRole.query.filter_by(id=project_role_id).first()


class ProjectRoleWorkFormatEnum(str, Enum):
    FullDay = 'FullDay'
    RemoteWork = 'RemoteWork'
    Flexible = 'Flexible'

    def label(self) -> str:
        return {
            self.FullDay: 'Полный день',
            self.RemoteWork: 'Удаленная работа',
            self.Flexible: 'Гибкий график'
        }[self]

    @classmethod
    def map(cls) -> dict:
        return {e.name: e.label() for e in cls}

    @classmethod
    def values(cls) -> list:
        return [e.name for e in cls]


class ProjectRoleWorkFormat(Base):
    __tablename__ = 'project_role_work_formats'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    value = Column(ProjectRoleWorkFormatEnum, nullable=False, unique=True)


class ProjectStage(Base):
    __tablename__ = "project_stage"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("project.id"))
    name = Column(String, index=True)
    start_date = Column(DateTime)
    finish_date = Column(DateTime)
    creator_id = Column(Integer, ForeignKey(User.id))
    updater_id = Column(Integer, ForeignKey(User.id))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    project = relationship("Project", back_populates="stages")


class ProjectStatusEnum(enum.Enum):
    Draft = 0
    Open = 1
    Completed = 2
    Done = 3
    Blocked = 4

    def label(self) -> str:
        return {
            self.Draft: 'Черновик',
            self.Open: 'Идёт набор',
            self.Completed: 'Команда набрана',
            self.Done: 'Проект завершен',
            self.Blocked: 'Снят с публикации',
        }[self]

    @classmethod
    def map(cls) -> Dict[int, str]:
        return {e.value: e.label() for e in cls}

    @classmethod
    def values(cls) -> List[int]:
        return [e.value for e in cls]

    @classmethod
    def active(cls) -> List[int]:
        return [cls.Open.value, cls.Completed.value, cls.Done.value]

    @classmethod
    def get_transition_map(cls) -> Dict[int, List[int]]:
        return {
            cls.Draft.value: [cls.Open.value],
            cls.Open.value: [cls.Completed.value, cls.Blocked.value],
            cls.Completed.value: [cls.Open.value, cls.Done.value],
            cls.Done.value: [],
            cls.Blocked.value: [cls.Open.value],
        }


class ProjectStatus(Base):
    __tablename__ = "project_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False, unique=True)
    description = Column(String(255))

    @hybrid_property
    def label(self) -> str:
        return ProjectStatusEnum(self.value).label()


class ProjectTypeEnum(PyEnum):
    Software = 0
    SoftwareAndHardware = 1
    Research = 2
    Startup = 3
    Internship = 4


class ProjectType(Base):
    __tablename__ = "project_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(ProjectTypeEnum), nullable=False)

    @staticmethod
    def map():
        return {e.value: e.name for e in ProjectTypeEnum}

    @staticmethod
    def values():
        return [e.value for e in ProjectTypeEnum]

    def label(self):
        return self.type.name


class ProjectView(PyEnum):
    DigitalAcademy = 0
    AdvancedEngineeringSchool = 1
    GPO = 2

    def label(self) -> str:
        return {
            self.DigitalAcademy: 'Цифровая академия',
            self.AdvancedEngineeringSchool: 'ПИШ (Передовая инженерная школа)',
            self.GPO: 'ГПО',
        }[self]

    @classmethod
    def map(cls) -> dict[int, str]:
        return {e.value: e.label() for e in cls}

    @classmethod
    def values(cls) -> list[int]:
        return [e.value for e in cls]


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    updater_id = Column(Integer, ForeignKey("users.id"))
    icon_id = Column(Integer, ForeignKey("role_icons.id"), nullable=True)
    created_at = Column(text, default=text("(now() at time zone 'utc')"))
    updated_at = Column(text, default=text("(now() at time zone 'utc')"))

    icon = relationship("RoleIcon", back_populates="roles")


class RoleIcon(Base):
    __tablename__ = "role_icons"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    updater_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column('createdAt', datetime, default=datetime.utcnow)
    updated_at = Column('updatedAt', datetime, default=datetime.utcnow)

    def get_file_name(self) -> str:
        return f"{self.id}.svg"


class StudentSubjectArea(Base):
    __tablename__ = 'student_subject_area'
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    subject_area_id = Column(Integer, ForeignKey('subject_areas.id'), primary_key=True)


class SubjectArea(Base, HasUserStampsTrait):
    __tablename__ = 'subject_areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    creator_id = Column(Integer, ForeignKey('users.id'))
    updater_id = Column(Integer, ForeignKey('users.id'))

    students = relationship('Student', secondary=StudentSubjectArea.__tablename__)

    @classmethod
    def by_contingent_id(cls, db, contingent_id: int):
        return cls.query.join(cls.students).filter(Student.contingent_person_id == contingent_id)


class Subscriber(Base):
    __tablename__ = "company_subscriber"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    student_id = Column(Integer, index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    @classmethod
    def by_company_id(cls, db, company_id: int):
        return db.query(cls).filter(cls.company_id == company_id).all()

    @classmethod
    def by_student_id_and_company_id(cls, db, student_id: int, company_id: int):
        return db.query(cls).filter(
            cls.student_id == student_id, cls.company_id == company_id
        ).first()


class TypeActivity(Base):
    __tablename__ = "type_activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Define the relationship to Student model
    students = relationship("Student", back_populates="type_activity")


