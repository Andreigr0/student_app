import enum

from sqlalchemy import Column, Integer, Enum, String, Boolean, TIMESTAMP, func

from app.database import Base


class InvitationStatus(enum.Enum):
    new = (1, 'Новое')
    viewed = (2, 'Просмотрено')
    revoked = (3, 'Отозвано')
    expired = (4, 'Истёк срок')
    consent = (5, 'Согласие')
    refusal = (6, 'Отказ компании')
    in_team = (7, 'В команде')
    rejection = (8, 'Отказ студента')

    # @staticmethod
    # def getActives():
    #     return [
    #         InviteStatus.New.value,
    #         InviteStatus.Viewed.value,
    #         InviteStatus.Consent.value,
    #         InviteStatus.InTeam.value,
    #     ]
    #
    # @staticmethod
    # def getPassives():
    #     return [
    #         InviteStatus.Revoked.value,
    #         InviteStatus.Expired.value,
    #         InviteStatus.Refusal.value,
    #         InviteStatus.Rejection.value,
    #     ]
    #
    # @staticmethod
    # def getTransitionMap():
    #     return {
    #         InviteStatus.New.value: [
    #             InviteStatus.Revoked.value,
    #             InviteStatus.Viewed.value,
    #             InviteStatus.Expired.value,
    #         ],
    #         InviteStatus.Viewed.value: [
    #             InviteStatus.Consent.value,
    #             InviteStatus.Rejection.value,
    #         ],
    #         InviteStatus.Revoked.value: [],
    #         InviteStatus.Expired.value: [],
    #         InviteStatus.Consent.value: [
    #             InviteStatus.InTeam.value,
    #             InviteStatus.Refusal.value,
    #             InviteStatus.Expired.value,
    #         ],
    #         InviteStatus.Refusal.value: [],
    #         InviteStatus.InTeam.value: [],
    #         InviteStatus.Rejection.value: [],
    #     }
    #
    # @staticmethod
    # def getTransitionMapByStatus(status):
    #     return InviteStatus.getTransitionMap().get(status, [])
    #
    # @staticmethod
    # def availableToStudent():
    #     return [
    #         InviteStatus.Viewed.value,
    #         InviteStatus.Consent.value,
    #         InviteStatus.Rejection.value,
    #     ]
    #
    # @staticmethod
    # def availableToCompany():
    #     return [
    #         InviteStatus.New.value,
    #         InviteStatus.Revoked.value,
    #         InviteStatus.InTeam.value,
    #         InviteStatus.Refusal.value,
    #         InviteStatus.Consent.value,
    #     ]


class InvitationModel(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True, index=True)
    # project_role_id = Column(Integer, ForeignKey("project_roles.id"), nullable=False)
    # contingent_person_id = Column(Integer, nullable=False)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.new, nullable=False)
    text = Column(String)
    is_archival = Column(Boolean, nullable=False, default=False)

    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    # creator_id = Column(Integer)
    # updater_id = Column(Integer)

    # project_role = relationship("ProjectRole", back_populates="invites")
    # student = relationship("Student", foreign_key=[contingent_person_id], back_populates="invites")

    @classmethod
    def by_contingent_person_id(cls, contingent_person_id: int):
        return cls.query.filter(cls.contingent_person_id == contingent_person_id)

    # @classmethod
    # def by_company_id(cls, company_id: int):
    #     return cls.query.join(ProjectRole).join(Project).filter(Project.company_id == company_id)

    @classmethod
    def by_contingent_person_id_and_project_role_id(cls, contingent_person_id: int, project_role_id: int):
        return cls.query.filter(cls.contingent_person_id == contingent_person_id,
                                cls.project_role_id == project_role_id)

    # @classmethod
    # def is_active(cls):
    #     return cls.query.filter(cls.status.in_(InviteStatus.get_actives()))

    # @classmethod
    # def filter(cls, query_filter):
    #     return query_filter.apply(cls.query)

    # @classmethod
    # def by_project_id(cls, project_id: int):
    #     return cls.query.join(ProjectRole).filter(ProjectRole.project_id == project_id)
