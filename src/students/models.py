from sqlalchemy import Column, Integer, Text, String, Boolean, func, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import TimestampMixin, EditorMixin
from reports.models import StudentReportModel


class StudentModel(Base, TimestampMixin, EditorMixin):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    about = Column(Text, nullable=True)
    resume = Column(Text, nullable=True)
    resume_content_type = Column(String(255), nullable=True)
    resume_file_size = Column(Integer, nullable=True)
    is_full_feedback = Column(Boolean, default=False)

    subscribed_companies = relationship('CompaniesSubscribersModel', back_populates="student")
    subject_areas = relationship('StudentsSubjectAreasModel', back_populates="student")
    competencies = relationship('StudentsCompetenciesModel', back_populates="student")
    reports = relationship(StudentReportModel, back_populates="student")

    # reviews = relationship("MemberReview",
    #                        primaryjoin="Student.contingent_person_id == MemberReview.contingent_person_id")
    # projects = relationship("Project", secondary="members")
    # invites = relationship("Invite", primaryjoin="Student.contingent_person_id == Invite.contingent_person_id")
    # bids = relationship("Bid", primaryjoin="Student.contingent_person_id == Bid.contingent_person_id")
    # project_report_periods = relationship("ProjectReportPeriod", secondary="members")
    # reports = relationship("StudentReport", primaryjoin="Student.contingent_person_id == Member.contingent_person_id")


class StudentsSubjectAreasModel(Base):
    __tablename__ = 'student_subject_area'

    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), primary_key=True)
    subject_area_id = Column(Integer, ForeignKey('subject_areas.id', ondelete='CASCADE'), primary_key=True)

    student = relationship(StudentModel, back_populates='subject_areas')
    subject_area = relationship('SubjectAreaModel', back_populates='students')


class StudentsCompetenciesModel(Base):
    __tablename__ = 'student_competence'

    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), primary_key=True)
    competency_id = Column(Integer, ForeignKey('competencies.id', ondelete='CASCADE'), primary_key=True)

    student = relationship(StudentModel, back_populates='competencies')
    competency = relationship('CompetencyModel', back_populates='students')
