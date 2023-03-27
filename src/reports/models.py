import dataclasses

from sqlalchemy import ForeignKey, Integer, Column, String, Date, func, Boolean
from sqlalchemy.orm import relationship, Mapped, composite, mapped_column

from app.database import Base


@dataclasses.dataclass
class FileModel:
    file_name: str
    file_path: str


class ReportModel(Base):
    __tablename__ = "reports"

    stage_id = Column(Integer, ForeignKey('project_stages.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    is_accepted = Column(Boolean, nullable=False, default=False)
    publication_date = Column(Date, nullable=False, default=func.now())

    file: Mapped[FileModel] = composite(mapped_column('file_name'), mapped_column('file_path'))

    stage = relationship("ProjectStageModel", back_populates="reports")
    student = relationship("StudentModel", back_populates="reports")

    @property
    def project(self):
        return self.stage.project
