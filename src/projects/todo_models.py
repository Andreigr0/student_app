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
