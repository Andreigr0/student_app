from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class StudentReportModel(Base):
    __tablename__ = "student_reports"

    id = Column(Integer, primary_key=True, index=True)
    # period_id = Column(Integer, ForeignKey("project_report_periods.id"), nullable=False, index=True)
    # member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    is_accepted = Column(Boolean, nullable=False)
    content_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)

    # createdAt = Column(DateTime, nullable=False)
    # updatedAt = Column(DateTime, nullable=False)
    # member = relationship("Member", back_populates="student_reports")
    # project_report_period = relationship("ProjectReportPeriod", back_populates="student_reports")
    #
    # @classmethod
    # def by_period_id(cls, db, period_id: int):
    #     return db.query(cls).filter(cls.periodId == period_id)
    #
    # @classmethod
    # def by_member(cls, db, project_id: int, contingent_person_id: int):
    #     return (
    #         db.query(cls)
    #         .join(Member, cls.memberId == Member.id)
    #         .filter(Member.projectId == project_id, Member.contingentPersonId == contingent_person_id)
    #     )
    #
    # @classmethod
    # def by_id(cls, db, id: int):
    #     return db.query(cls).filter(cls.id == id)
    #
    # @classmethod
    # def by_is_accepted(cls, db, status: bool):
    #     return db.query(cls).filter(cls.isAccepted == status)
    #
    # @classmethod
    # def by_contingent_person_id(cls, db, contingent_person_id: int):
    #     return (
    #         db.query(cls)
    #         .select_from(cls)
    #         .join(Member, cls.memberId == Member.id)
    #         .filter(Member.contingentPersonId == contingent_person_id)
    #     )
    #
    # @classmethod
    # def by_member_id(cls, db, member_id: int):
    #     return db.query(cls).filter(cls.memberId == member_id)
