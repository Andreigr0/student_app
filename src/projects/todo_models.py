# from app.models.competence import competence_project_role
# from app.models.enums import ProjectRoleCompetenceType
# from app.models.mixins import TimestampMixin, UserStampMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Enum, Table, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import TimestampMixin


class Curator(Base):
    __tablename__ = "curators"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    curator_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    project = relationship("ProjectModel", back_populates="curators")
    curator = relationship("UserModel", back_populates="curated_projects")


member_review_competence_table = Table(
    'member_review_competence',
    Base.metadata,
    Column('member_review_id', Integer, ForeignKey('member_reviews.id')),
    Column('competence_id', Integer, ForeignKey('competencies.id')),
)


class ProjectManager(Base, TimestampMixin):
    __tablename__ = "project_managers"

    id = Column(Integer, primary_key=True, index=True)
    participant = Column(Enum(ProjectParticipant), nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))

    project = relationship("Project", back_populates="managers")
    contact = relationship("Contact", back_populates="projects")


class ProjectReportPeriod(Base, TimestampMixin):  # todo: add UserStampMixin
    __tablename__ = "project_report_periods"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)

    name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    finish_date = Column(String, nullable=False)

    project = relationship("Project", back_populates="report_periods")
    student_reports = relationship("StudentReport", back_populates="period")

    # @classmethod
    # def get_waiting_student_reports(cls, db, contingent_person_id: int, filter: str = ""):
    #     query = (
    #         db.query(cls)
    #         .join("project")
    #         .outerjoin("student_reports")
    #         .filter(Project.contingent_person_id == contingent_person_id)
    #         .filter(cls.member_id.is_(None))
    #     )
    #
    #     if filter == "all":
    #         date = text("CURRENT_DATE()")
    #         query = query.filter(
    #             text("(finish_date < :date OR (start_date <= :date AND finish_date >= :date))")).params(date=date)
    #     elif filter == "expired":
    #         query = query.filter(cls.finish_date < text("CURRENT_DATE()"))
    #     else:
    #         query = query.filter(cls.start_date <= text("CURRENT_DATE()")).filter(
    #             cls.finish_date >= text("CURRENT_DATE()"))
    #
    #     return query.order_by(cls.finish_date)
    #
    # @classmethod
    # def by_id(cls, db, id: int):
    #     return db.query(cls).filter(cls.id == id)
    #
    # @classmethod
    # def by_project_id(cls, db, project_id: int):
    #     return db.query(cls).filter(cls.project_id == project_id)
    #
    # @classmethod
    # def by_start_date(cls, db, date: str, operator: str):
    #     return db.query(cls).filter(text(f"start_date {operator} :date")).params(date=date)


class ProjectRole(Base):
    __tablename__ = "project_roles"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    workload = Column(Integer)
    work_format = Column(Integer)
    type = Column(Enum(ProjectRoleCompetenceType), nullable=False)

    project = relationship("Project", back_populates="project_roles")
    need_competencies = relationship("Competence", back_populates="need_project_roles")
    will_competencies = relationship("Competence", back_populates="will_project_roles")
    role = relationship("Role", back_populates="project_roles")
    bids = relationship("Bid", back_populates="project_role")


class Role(Base, TimestampMixin):  # todo: add UserMixin
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    filename = Column(String)

    def get_file_name(self) -> str:
        return f"{self.id}.svg"
