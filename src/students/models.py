from sqlalchemy import Column, Integer, Text, String, Boolean, func, TIMESTAMP
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import TimestampMixin


class StudentModel(Base, TimestampMixin):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    # contingent_person_id = Column(Integer, index=True)
    about = Column(Text, nullable=True)
    resume = Column(Text, nullable=True)
    resume_content_type = Column(String(255), nullable=True)
    resume_file_size = Column(Integer, nullable=True)
    is_full_feedback = Column(Boolean, default=False)

    subscribed_companies = relationship('CompaniesSubscribersModel', back_populates="student")

    # creator_id = Column(Integer, nullable=True)
    # updater_id = Column(Integer, nullable=True)

    # competencies = relationship("CompetenceModel", secondary="student_competence")
    # subject_areas = relationship("SubjectArea", secondary="student_subject_area")
    # reviews = relationship("MemberReview",
    #                        primaryjoin="Student.contingent_person_id == MemberReview.contingent_person_id")
    # projects = relationship("Project", secondary="members")
    # invites = relationship("Invite", primaryjoin="Student.contingent_person_id == Invite.contingent_person_id")
    # bids = relationship("Bid", primaryjoin="Student.contingent_person_id == Bid.contingent_person_id")
    # project_report_periods = relationship("ProjectReportPeriod", secondary="members")
    # reports = relationship("StudentReport", primaryjoin="Student.contingent_person_id == Member.contingent_person_id")
    #
    # def by_contingent_person_id(cls, db, contingent_person_id: int):
    #     return db.query(cls).filter(cls.contingent_person_id == contingent_person_id).first()
