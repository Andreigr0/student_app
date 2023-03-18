# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, ForeignKey, Index, Integer, SmallInteger, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AdminMenu(Base):
    __tablename__ = 'admin_menu'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".admin_menu_id_seq'::regclass)"))
    parent_id = Column(Integer, nullable=False, server_default=text("0"))
    order = Column(Integer, nullable=False, server_default=text("0"))
    title = Column(String(50), nullable=False)
    icon = Column(String(50), nullable=False)
    uri = Column(String(255))
    permission = Column(String(255))
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))


class AdminOperationLog(Base):
    __tablename__ = 'admin_operation_log'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".admin_operation_log_id_seq'::regclass)"))
    user_id = Column(Integer, nullable=False, index=True)
    path = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    ip = Column(String(255), nullable=False)
    input = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))


class AdminPermission(Base):
    __tablename__ = 'admin_permissions'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".admin_permissions_id_seq'::regclass)"))
    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(50), nullable=False, unique=True)
    http_method = Column(String(255))
    http_path = Column(Text)
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))


t_admin_role_menu = Table(
    'admin_role_menu', metadata,
    Column('role_id', Integer, nullable=False),
    Column('menu_id', Integer, nullable=False),
    Column('created_at', TIMESTAMP(precision=0)),
    Column('updated_at', TIMESTAMP(precision=0)),
    Index('admin_role_menu_role_id_menu_id_index', 'role_id', 'menu_id'),
    schema='public'
)


t_admin_role_permissions = Table(
    'admin_role_permissions', metadata,
    Column('role_id', Integer, nullable=False),
    Column('permission_id', Integer, nullable=False),
    Column('created_at', TIMESTAMP(precision=0)),
    Column('updated_at', TIMESTAMP(precision=0)),
    Index('admin_role_permissions_role_id_permission_id_index', 'role_id', 'permission_id'),
    schema='public'
)


t_admin_role_users = Table(
    'admin_role_users', metadata,
    Column('role_id', Integer, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('created_at', TIMESTAMP(precision=0)),
    Column('updated_at', TIMESTAMP(precision=0)),
    Index('admin_role_users_role_id_user_id_index', 'role_id', 'user_id'),
    schema='public'
)


class AdminRole(Base):
    __tablename__ = 'admin_roles'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".admin_roles_id_seq'::regclass)"))
    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(50), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))


t_admin_user_permissions = Table(
    'admin_user_permissions', metadata,
    Column('user_id', Integer, nullable=False),
    Column('permission_id', Integer, nullable=False),
    Column('created_at', TIMESTAMP(precision=0)),
    Column('updated_at', TIMESTAMP(precision=0)),
    Index('admin_user_permissions_user_id_permission_id_index', 'user_id', 'permission_id'),
    schema='public'
)


class AdminUser(Base):
    __tablename__ = 'admin_users'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".admin_users_id_seq'::regclass)"))
    username = Column(String(190), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    name = Column(String(255), nullable=False)
    avatar = Column(String(255))
    remember_token = Column(String(100))
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))


class Company(Base):
    __tablename__ = 'companies'
    __table_args__ = (
        CheckConstraint('("employeeCount")::text = ANY ((ARRAY[\'0\'::character varying, \'1\'::character varying, \'2\'::character varying, \'3\'::character varying])::text[])'),
        CheckConstraint("(status)::text = ANY ((ARRAY['0'::character varying, '1'::character varying, '2'::character varying, '3'::character varying, '4'::character varying, '5'::character varying])::text[])"),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".companies_id_seq'::regclass)"))
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(30), nullable=False)
    inn = Column(BigInteger, unique=True)
    hasAccreditation = Column(Boolean, nullable=False, server_default=text("false"))
    site = Column(String(255))
    description = Column(String(200))
    logo = Column(String(255))
    employeeCount = Column(String(255))
    status = Column(String(255), nullable=False, server_default=text("'0'::character varying"))
    reasonRejection = Column(String(255))
    representativeId = Column(BigInteger)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    activeProjectCount = Column(Integer, nullable=False, server_default=text("0"))

    type_activities = relationship('TypeActivity', secondary='public.company_type_activity')
    projects = relationship('Project', secondary='public.partners')
    students = relationship('Student', secondary='public.company_subscriber')


class Competency(Base):
    __tablename__ = 'competencies'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".competencies_id_seq'::regclass)"))
    name = Column(String(50), nullable=False, unique=True)
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))

    students = relationship('Student', secondary='public.student_competence')


class FailedJob(Base):
    __tablename__ = 'failed_jobs'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".failed_jobs_id_seq'::regclass)"))
    uuid = Column(String(255), nullable=False, unique=True)
    connection = Column(Text, nullable=False)
    queue = Column(Text, nullable=False)
    payload = Column(Text, nullable=False)
    exception = Column(Text, nullable=False)
    failed_at = Column(TIMESTAMP(precision=0), nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Migration(Base):
    __tablename__ = 'migrations'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".migrations_id_seq'::regclass)"))
    migration = Column(String(255), nullable=False)
    batch = Column(Integer, nullable=False)


t_password_resets = Table(
    'password_resets', metadata,
    Column('email', String(255), nullable=False, index=True),
    Column('token', String(255), nullable=False),
    Column('created_at', TIMESTAMP(precision=0)),
    schema='public'
)


class PersonalAccessToken(Base):
    __tablename__ = 'personal_access_tokens'
    __table_args__ = (
        Index('personal_access_tokens_tokenable_type_tokenable_id_index', 'tokenable_type', 'tokenable_id'),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".personal_access_tokens_id_seq'::regclass)"))
    tokenable_type = Column(String(255), nullable=False)
    tokenable_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
    token = Column(String(64), nullable=False, unique=True)
    abilities = Column(Text)
    last_used_at = Column(TIMESTAMP(precision=0))
    expires_at = Column(TIMESTAMP(precision=0))
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))


class RoleIcon(Base):
    __tablename__ = 'role_icons'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".role_icons_id_seq'::regclass)"))
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)


class Student(Base):
    __tablename__ = 'students'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".students_id_seq'::regclass)"))
    contingentPersonId = Column(BigInteger, nullable=False, unique=True)
    about = Column(Text)
    resume = Column(String(255))
    isFullFeedback = Column(Boolean, nullable=False, server_default=text("true"))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    resumeContentType = Column(String(255))
    resumeFileSize = Column(Integer)

    subject_areas = relationship('SubjectArea', secondary='public.student_subject_area')


class SubjectArea(Base):
    __tablename__ = 'subject_areas'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".subject_areas_id_seq'::regclass)"))
    name = Column(String(50), nullable=False, unique=True)
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))


class TypeActivity(Base):
    __tablename__ = 'type_activities'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".type_activities_id_seq'::regclass)"))
    name = Column(String(50), nullable=False, unique=True)
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".users_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    email_verified_at = Column(TIMESTAMP(precision=0))
    password = Column(String(255), nullable=False)
    remember_token = Column(String(100))
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))


t_company_subscriber = Table(
    'company_subscriber', metadata,
    Column('companyId', ForeignKey('public.companies.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('studentId', ForeignKey('public.students.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    UniqueConstraint('companyId', 'studentId'),
    schema='public'
)


t_company_type_activity = Table(
    'company_type_activity', metadata,
    Column('companyId', ForeignKey('public.companies.id', ondelete='CASCADE'), nullable=False),
    Column('typeActivityId', ForeignKey('public.type_activities.id', ondelete='CASCADE'), nullable=False, index=True),
    UniqueConstraint('companyId', 'typeActivityId'),
    schema='public'
)


class Contact(Base):
    __tablename__ = 'contacts'
    __table_args__ = (
        CheckConstraint('("communicationType")::text = ANY ((ARRAY[\'0\'::character varying, \'1\'::character varying, \'2\'::character varying])::text[])'),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".contacts_id_seq'::regclass)"))
    companyId = Column(ForeignKey('public.companies.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    fio = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255))
    telegram = Column(String(255))
    communicationType = Column(String(255), nullable=False)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    company = relationship('Company')


class Project(Base):
    __tablename__ = 'projects'
    __table_args__ = (
        CheckConstraint("(status)::text = ANY ((ARRAY['0'::character varying, '1'::character varying, '2'::character varying, '3'::character varying, '4'::character varying])::text[])"),
        CheckConstraint("(type)::text = ANY ((ARRAY['0'::character varying, '1'::character varying, '2'::character varying, '3'::character varying, '4'::character varying])::text[])"),
        CheckConstraint("(view)::text = ANY ((ARRAY['0'::character varying, '1'::character varying, '2'::character varying])::text[])"),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".projects_id_seq'::regclass)"))
    companyId = Column(ForeignKey('public.companies.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String(300), nullable=False)
    isVisible = Column(Boolean, nullable=False, server_default=text("false"))
    type = Column(String(255))
    view = Column(String(255))
    description = Column(String(1000))
    problem = Column(Text)
    purpose = Column(Text)
    task = Column(Text)
    result = Column(Text)
    whatWillGet = Column(Text)
    status = Column(String(255), nullable=False, server_default=text("'0'::character varying"))
    total = Column(Text)
    report = Column(String(255))
    reasonRejection = Column(String(255))
    applicationDate = Column(Date)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    duration = Column(SmallInteger)

    company = relationship('Company')
    subject_areas = relationship('SubjectArea', secondary='public.project_subject_area')


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".roles_id_seq'::regclass)"))
    name = Column(String(50), nullable=False, unique=True)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    iconId = Column(ForeignKey('public.role_icons.id', ondelete='CASCADE'))

    role_icon = relationship('RoleIcon')


t_student_competence = Table(
    'student_competence', metadata,
    Column('studentId', ForeignKey('public.students.id', ondelete='CASCADE'), nullable=False),
    Column('competenceId', ForeignKey('public.competencies.id', ondelete='CASCADE'), nullable=False, index=True),
    UniqueConstraint('studentId', 'competenceId'),
    schema='public'
)


t_student_subject_area = Table(
    'student_subject_area', metadata,
    Column('studentId', ForeignKey('public.students.id', ondelete='CASCADE'), nullable=False),
    Column('subjectAreaId', ForeignKey('public.subject_areas.id', ondelete='CASCADE'), nullable=False, index=True),
    UniqueConstraint('studentId', 'subjectAreaId'),
    schema='public'
)


class Curator(Base):
    __tablename__ = 'curators'
    __table_args__ = (
        UniqueConstraint('projectId', 'curatorId'),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".curators_id_seq'::regclass)"))
    projectId = Column(ForeignKey('public.projects.id', ondelete='CASCADE'), nullable=False)
    curatorId = Column(Integer, nullable=False)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))

    project = relationship('Project')


t_partners = Table(
    'partners', metadata,
    Column('projectId', ForeignKey('public.projects.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('companyId', ForeignKey('public.companies.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    UniqueConstraint('projectId', 'companyId'),
    schema='public'
)


class ProjectManager(Base):
    __tablename__ = 'project_managers'
    __table_args__ = (
        CheckConstraint("(participant)::text = ANY ((ARRAY['1'::character varying, '2'::character varying])::text[])"),
        UniqueConstraint('projectId', 'contactId'),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".project_managers_id_seq'::regclass)"))
    projectId = Column(ForeignKey('public.projects.id', ondelete='CASCADE'), nullable=False)
    contactId = Column(ForeignKey('public.contacts.id', ondelete='CASCADE'), nullable=False)
    participant = Column(String(255), nullable=False, server_default=text("'1'::character varying"))
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))

    contact = relationship('Contact')
    project = relationship('Project')


class ProjectReportPeriod(Base):
    __tablename__ = 'project_report_periods'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".project_report_periods_id_seq'::regclass)"))
    projectId = Column(ForeignKey('public.projects.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    startDate = Column(Date, nullable=False)
    finishDate = Column(Date, nullable=False)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    project = relationship('Project')


class ProjectRole(Base):
    __tablename__ = 'project_roles'
    __table_args__ = (
        CheckConstraint('("workFormat")::text = ANY ((ARRAY[\'0\'::character varying, \'1\'::character varying, \'2\'::character varying])::text[])'),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".project_roles_id_seq'::regclass)"))
    projectId = Column(ForeignKey('public.projects.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    roleId = Column(ForeignKey('public.roles.id', ondelete='CASCADE'), nullable=False, index=True)
    workload = Column(String(255), nullable=False)
    workFormat = Column(String(255), nullable=False)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    project = relationship('Project')
    role = relationship('Role')


class ProjectStage(Base):
    __tablename__ = 'project_stages'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".project_stages_id_seq'::regclass)"))
    projectId = Column(ForeignKey('public.projects.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    startDate = Column(Date, nullable=False)
    finishDate = Column(Date, nullable=False)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    project = relationship('Project')


t_project_subject_area = Table(
    'project_subject_area', metadata,
    Column('projectId', ForeignKey('public.projects.id', ondelete='CASCADE'), nullable=False),
    Column('subjectAreaId', ForeignKey('public.subject_areas.id', ondelete='CASCADE'), nullable=False, index=True),
    UniqueConstraint('projectId', 'subjectAreaId'),
    schema='public'
)


class Bid(Base):
    __tablename__ = 'bids'
    __table_args__ = (
        CheckConstraint("(status)::text = ANY ((ARRAY['1'::character varying, '2'::character varying, '3'::character varying, '4'::character varying, '5'::character varying, '6'::character varying])::text[])"),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".bids_id_seq'::regclass)"))
    projectRoleId = Column(ForeignKey('public.project_roles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    contingentPersonId = Column(ForeignKey('public.students.contingentPersonId', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    status = Column(String(255), nullable=False, server_default=text("'1'::character varying"))
    about = Column(Text, nullable=False)
    experience = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    refusalReason = Column(Text)
    isArchival = Column(Boolean, nullable=False, server_default=text("false"))
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    student = relationship('Student')
    project_role = relationship('ProjectRole')


class Invite(Base):
    __tablename__ = 'invites'
    __table_args__ = (
        CheckConstraint("(status)::text = ANY ((ARRAY['1'::character varying, '2'::character varying, '3'::character varying, '4'::character varying, '5'::character varying, '6'::character varying, '7'::character varying, '8'::character varying])::text[])"),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".invites_id_seq'::regclass)"))
    projectRoleId = Column(ForeignKey('public.project_roles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    contingentPersonId = Column(BigInteger, nullable=False, index=True)
    text = Column(Text, nullable=False)
    isArchival = Column(Boolean, nullable=False, server_default=text("false"))
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)
    status = Column(String(255), nullable=False, server_default=text("'1'::character varying"))

    project_role = relationship('ProjectRole')


class Member(Base):
    __tablename__ = 'members'
    __table_args__ = (
        UniqueConstraint('projectId', 'contingentPersonId'),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".members_id_seq'::regclass)"))
    projectId = Column(ForeignKey('public.projects.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    projectRoleId = Column(ForeignKey('public.project_roles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    contingentPersonId = Column(ForeignKey('public.students.contingentPersonId', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    student = relationship('Student')
    project = relationship('Project')
    project_role = relationship('ProjectRole')


t_project_role_competence = Table(
    'project_role_competence', metadata,
    Column('projectRoleId', ForeignKey('public.project_roles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('competenceId', ForeignKey('public.competencies.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Column('type', String(255), nullable=False, index=True),
    CheckConstraint("(type)::text = ANY ((ARRAY['0'::character varying, '1'::character varying])::text[])"),
    UniqueConstraint('projectRoleId', 'competenceId', 'type'),
    schema='public'
)


class MemberReview(Base):
    __tablename__ = 'member_reviews'
    __table_args__ = (
        CheckConstraint("(score)::text = ANY ((ARRAY['1'::character varying, '2'::character varying, '3'::character varying, '4'::character varying, '5'::character varying])::text[])"),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".member_reviews_id_seq'::regclass)"))
    memberId = Column(ForeignKey('public.members.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    contingentPersonId = Column(ForeignKey('public.students.contingentPersonId', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    startDate = Column(Date, nullable=False)
    finishDate = Column(Date, nullable=False)
    hours = Column(Integer, nullable=False)
    score = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    student = relationship('Student')
    member = relationship('Member')


class StudentReport(Base):
    __tablename__ = 'student_reports'
    __table_args__ = (
        UniqueConstraint('memberId', 'periodId'),
        {'schema': 'public'}
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".student_reports_id_seq'::regclass)"))
    memberId = Column(ForeignKey('public.members.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    periodId = Column(ForeignKey('public.project_report_periods.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    contentType = Column(String(255), nullable=False)
    fileSize = Column(Integer, nullable=False)
    isAccepted = Column(Boolean, nullable=False, server_default=text("false"))
    createdAt = Column(TIMESTAMP(precision=0))
    updatedAt = Column(TIMESTAMP(precision=0))
    creatorId = Column(BigInteger)
    updaterId = Column(BigInteger)

    member = relationship('Member')
    project_report_period = relationship('ProjectReportPeriod')


t_member_review_competence = Table(
    'member_review_competence', metadata,
    Column('memberReviewId', ForeignKey('public.member_reviews.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('competenceId', ForeignKey('public.competencies.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('contingentPersonId', ForeignKey('public.students.contingentPersonId', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    UniqueConstraint('memberReviewId', 'contingentPersonId', 'competenceId'),
    schema='public'
)
