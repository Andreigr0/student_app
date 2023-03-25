import datetime

from competencies.models import CompetencyModel
from projects.models import ProjectStageModel, ProjectsMembersModel, ProjectTeamStatus, \
    ProjectsCompaniesModel, ProjectCompanyType
from projects.models import ProjectStatus, ProjectType, ProjectKind, WorkFormat, ProjectPosition


def test_create_project_model(create_project_model):
    project = create_project_model()

    assert project.id == 1
    assert project.name == 'Test project'
    assert project.status == ProjectStatus.under_recruitment
    assert project.start_date == datetime.date(2021, 1, 1)
    assert project.finish_date == datetime.date(2021, 2, 1)
    assert project.type == ProjectType.research
    assert project.kind == ProjectKind.digital_academy
    assert project.is_only_for_digital_academy is True
    assert project.description == 'Test description'
    assert project.solving_problems == 'Test solving problems'
    assert project.goals == 'Test goals'
    assert project.tasks == 'Test tasks'
    assert project.results == 'Test results'
    assert project.what_will_participant_get == 'Test what will participant get'


def test_create_project_competencies(create_project_model, db_test):
    project = create_project_model()

    competency1 = CompetencyModel(name='Test competency 1')
    competency2 = CompetencyModel(name='Test competency 2')

    project.competencies.append(competency1)
    project.competencies.append(competency2)

    db_test.add(project)
    db_test.commit()

    assert project.competencies == [competency1, competency2]


def test_create_project_stage_model(db_test, create_project_model):
    project = create_project_model()

    stage = ProjectStageModel(
        name='Test stage',
        start_date=datetime.date(2021, 1, 1),
        finish_date=datetime.date(2021, 2, 1),
    )
    stage.project = project
    db_test.add(stage)
    db_test.commit()

    assert stage.id == 1
    assert stage.name == 'Test stage'
    assert stage.start_date == datetime.date(2021, 1, 1)
    assert stage.finish_date == datetime.date(2021, 2, 1)
    assert stage.project_id == 1


def test_create_project_role_model(db_test, create_project_role_model):
    role = create_project_role_model()

    assert role.id == 1
    assert role.work_load == 'Test work load'
    assert role.work_format == WorkFormat.full_time
    assert len(role.needed_competencies) == 2
    assert len(role.acquired_competencies) == 1


def test_create_projects_companies(db_test, create_project_model, create_company):
    project = create_project_model()
    company1, company2 = create_company(), create_company()

    association1 = ProjectsCompaniesModel(company=company1, type=ProjectCompanyType.organizer)
    association2 = ProjectsCompaniesModel(company=company2, type=ProjectCompanyType.partner)

    project.companies.append(association1)
    project.companies.append(association2)

    db_test.add(project)
    db_test.commit()

    assert len(project.companies) == 2
    assert project.companies[0].company == company1
    assert project.companies[0].type == ProjectCompanyType.organizer
    assert project.companies[1].company == company2
    assert project.companies[1].type == ProjectCompanyType.partner


def test_create_members(db_test, create_project_model, create_student, create_company_representative,
                        create_project_role_model):
    project = create_project_model()
    role = create_project_role_model()
    student, company = create_student(), create_company_representative()

    member1 = ProjectsMembersModel(
        description='Test description',
        position=ProjectPosition.student,
        status=ProjectTeamStatus.rejected,
    )
    member1.user = student
    member1.role = role

    member2 = ProjectsMembersModel(
        description='Test description',
        position=ProjectPosition.curator,
        status=ProjectTeamStatus.accepted,
    )
    member2.user = company

    project.team.append(member1)
    project.team.append(member2)

    db_test.add(project)
    db_test.commit()

    assert set(project.team) == {member1, member2}
    assert project.team[0].role == role
    assert project.team[0].user == student
    assert project.team[0].description == 'Test description'
    assert project.team[0].position == ProjectPosition.student
    assert project.team[0].status == ProjectTeamStatus.rejected

    assert project.team[1].role is None
    assert project.team[1].user == company
    assert project.team[1].position == ProjectPosition.curator
    assert project.team[1].status == ProjectTeamStatus.accepted
