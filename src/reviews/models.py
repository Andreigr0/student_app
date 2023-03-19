from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, func, Date


class MemberReviewModel(Base):
    __tablename__ = 'member_reviews'

    id = Column(Integer, primary_key=True, index=True)
    # member_id = Column(Integer, ForeignKey('members.id'))
    # contingent_person_id = Column(Integer, ForeignKey('students.contingent_person_id'))

    start_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=False)
    hours = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    text = Column(String, nullable=False)

    # competencies = relationship("Competence", secondary=member_review_competence_table, backref="member_reviews")
    # student = relationship("Student", backref="member_reviews")
    # member = relationship("Member", backref="member_reviews")
    # project = relationship("Project", secondary='members', backref="member_reviews")

    # @staticmethod
    # def avg_score(query):
    #     return query.with_entities(func.avg(MemberReview.score)).scalar()
