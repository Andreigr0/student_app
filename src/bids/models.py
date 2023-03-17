from sqlalchemy import Integer, Column, ForeignKey, String, func, Enum, Boolean, TIMESTAMP
import enum

from app.database import Base


class BidStatus(enum.Enum):
    new = (1, 'Новая')
    viewed = (2, 'Просмотрено')
    revoked = (3, 'Отозвано')
    expired = (4, 'Истёк срок')
    inTeam = (5, 'В команде')
    refusal = (6, 'Отказ компании')

    # @classmethod
    # def values(cls) -> list[int]:
    #     return [status.id for status in cls.query.all()]
    #
    # @classmethod
    # def get_actives(cls) -> list[int]:
    #     return [cls.New, cls.Viewed, cls.InTeam]
    #
    # @classmethod
    # def get_passives(cls) -> list[int]:
    #     return [cls.Expired, cls.Revoked, cls.Refusal]
    #
    # @classmethod
    # def get_transition_map(cls) -> dict[int, list[int]]:
    #     return {
    #         cls.New: [cls.Revoked, cls.Viewed, cls.Expired],
    #         cls.Viewed: [cls.Expired, cls.InTeam, cls.Refusal],
    #         cls.Revoked: [],
    #         cls.Expired: [],
    #         cls.Refusal: [],
    #         cls.InTeam: [],
    #     }
    #
    # @classmethod
    # def available_to_student(cls) -> list[int]:
    #     return [cls.Revoked]
    #
    # @classmethod
    # def available_to_company(cls) -> list[int]:
    #     return [cls.Viewed, cls.InTeam, cls.Refusal]


class BidModel(Base):
    __tablename__ = 'bids'

    id = Column(Integer, primary_key=True)
    # projectRoleId = Column(Integer, ForeignKey('project_roles.id'))
    # contingentPersonId = Column(Integer, ForeignKey('students.contingentPersonId'))
    status = Column(Enum(BidStatus), nullable=False, default=BidStatus.new)
    about = Column(String)
    experience = Column(String)
    reason = Column(String)
    refusal_reason = Column(String, nullable=True)
    is_archival = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    # student = relationship('Student', backref='bids')
    # projectRole = relationship('ProjectRole', backref='bids')

    # @classmethod
    # def by_contingent_person_id(cls, query, contingent_person_id):
    #     return query.filter(cls.contingentPersonId == contingent_person_id)
    #
    # @classmethod
    # def byContingentPersonIdAndProjectRoleId(cls, query, contingentPersonId, projectRoleId):
    #     return query.filter(cls.contingentPersonId == contingentPersonId, cls.projectRoleId == projectRoleId)
    #
    # @classmethod
    # def isActive(cls, query):
    #     return query.filter(cls.status.in_(BidStatus.getActives()))
    #
    # @classmethod
    # def byCompanyId(cls, query, companyId):
    #     return query.join(ProjectRole).join(Project).filter(Project.companyId == companyId)
    #
    # @classmethod
    # def byProjectId(cls, query, projectId):
    #     return query.join(ProjectRole).filter(ProjectRole.projectId == projectId)
