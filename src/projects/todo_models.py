# from app.models.competence import competence_project_role
# from app.models.enums import ProjectRoleCompetenceType
# from app.models.mixins import TimestampMixin, UserStampMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Enum, Table, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import TimestampMixin, EditorMixin

member_review_competence_table = Table(
    'member_review_competence',
    Base.metadata,
    Column('member_review_id', Integer, ForeignKey('member_reviews.id')),
    Column('competence_id', Integer, ForeignKey('competencies.id')),
)


