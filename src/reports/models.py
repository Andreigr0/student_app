from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import TimestampMixin


class StudentReportModel(Base, TimestampMixin):
    __tablename__ = "student_reports"

    id = Column(Integer, primary_key=True, index=True)

    # period_id = Column(Integer, ForeignKey("project_report_periods.id"), nullable=False, index=True)
    # member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)

    filename = Column(String, nullable=False)
    is_accepted = Column(Boolean, nullable=False)
    content_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)

    # member = relationship("Member", back_populates="student_reports")
    # project_report_period = relationship("ProjectReportPeriod", back_populates="student_reports")
