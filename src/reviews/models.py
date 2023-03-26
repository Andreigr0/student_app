from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship

from app.database import Base


class ReviewModel(Base):
    __tablename__ = "reviews"

    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, primary_key=True)
    role_id = Column(Integer, ForeignKey('project_roles.id'), nullable=False, primary_key=True)
    score = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    spent_hours = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)

    student = relationship("StudentModel", back_populates="reviews")
    role = relationship("ProjectRoleModel", back_populates="reviews")

    @property
    def project(self):
        return self.role.project

    @property
    def company(self):
        from projects.models import ProjectCompanyType
        organizer_companies = [company for company in self.project.companies if
                               company.type == ProjectCompanyType.organizer]
        return organizer_companies[0] if organizer_companies else None
