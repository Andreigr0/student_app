from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import EditorMixin, TimestampMixin


class CompetencyModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    students = relationship('StudentsCompetenciesModel', back_populates='competency')


class SubjectAreaModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = 'subject_areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    students = relationship('StudentsSubjectAreasModel', back_populates='subject_area')
