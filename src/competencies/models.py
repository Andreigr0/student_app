from sqlalchemy import Column, Integer, ForeignKey, String

from app.database import Base


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
