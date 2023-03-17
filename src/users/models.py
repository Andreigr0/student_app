from sqlalchemy import Column, Integer, String, TIMESTAMP

from app.database import Base
from app.utils import TimestampMixin


class UserModel(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email_verified_at = Column(TIMESTAMP, default=None, nullable=True)


class MemberModel(Base, TimestampMixin):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    projectId = Column(String)
    projectRoleId = Column(Integer)
    contingentPersonId = Column(Integer)

    # creatorId = Column(Integer)
    # updaterId = Column(Integer)

    # project = relationship('Project', back_populates='members')
    # student = relationship('Student', back_populates='members')
    # review = relationship('MemberReview', back_populates='member')
    # project_role = relationship('ProjectRole', back_populates='members')

    @classmethod
    def by_project_id(cls, session, project_id):
        return session.query(cls).filter(cls.projectId == project_id)

    @classmethod
    def by_contingent_person_id(cls, session, contingent_person_id):
        return session.query(cls).filter(cls.contingentPersonId == contingent_person_id)
