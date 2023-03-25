from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.database import Base
from app.utils import EditorMixin, TimestampMixin


class CompetencyModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    students = relationship('StudentModel', secondary='students_competencies', back_populates='competencies')


class SubjectAreaModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = 'subject_areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    students = relationship('StudentModel', secondary='students_subject_areas', back_populates='subject_areas')
