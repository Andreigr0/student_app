from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class CompanyModel(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    description = Column(String, nullable=False)
    has_accreditation = Column(Boolean, nullable=False, default=False)

    # todo: add later
    # competencies = relationship("CompetencyModel", back_populates="company")
    # projects = relationship("ProjectModel", back_populates="company")

    # # Calculated fields: active projects count, total projects count
    # active_projects_count = Column(Integer, nullable=False, default=0)
    # total_projects_count = Column(Integer, nullable=False, default=0)

    representatives = relationship("CompanyRepresentativeModel", back_populates="company")
