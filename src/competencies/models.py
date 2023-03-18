from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import EditorMixin, TimestampMixin


class CompetenceModel(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # creator_id = Column(Integer, ForeignKey("users.id"))
    # updater_id = Column(Integer, ForeignKey("users.id"))

    # students = relationship("Student", secondary="student_competence")

    # @classmethod
    # def by_contingent_id(cls, db, contingent_id: int):
    #     return db.query(cls).filter(cls.students.any(contingent_person_id=contingent_id)).all()


class SubjectAreaModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = 'subject_areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    students = relationship('StudentsSubjectAreasModel', back_populates='subject_area')
