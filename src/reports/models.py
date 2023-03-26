from sqlalchemy import ForeignKey, Integer, Column, String, Date, func, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class ReportModel(Base):
    __tablename__ = "reports"

    stage_id = Column(Integer, ForeignKey('project_stages.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    is_accepted = Column(Boolean, nullable=False, default=False)
    publication_date = Column(Date, nullable=False, default=func.now())

    stage = relationship("ProjectStageModel", back_populates="reports")
    student = relationship("StudentModel", back_populates="reports")

    @property
    def project(self):
        return self.stage.project
