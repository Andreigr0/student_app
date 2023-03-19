from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import TimestampMixin


class UserModel(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email_verified_at = Column(TIMESTAMP, default=None, nullable=True)

    curated_projects = relationship('ProjectsCuratorsModel', back_populates='curator')


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
