from companies.models import ContactModel, CompanyModel
from competencies.models import CompetencyModel
from projects.models import ProjectModel, ProjectParticipant, ProjectRoleWorkFormatEnum, \
    ProjectStatusEnum, ProjectTypeEnum, ProjectView, ProjectStageModel, ProjectsManagersModel, ProjectsCuratorsModel, \
    ProjectRoleModel
import datetime


def test_create_project_model(db_test, create_project_model):
    project, now = create_project_model()

    assert project.id == 1
    assert project.name == 'test'
    assert project.is_visible is True
    assert project.type == ProjectTypeEnum.Research
    assert project.view == ProjectView.DigitalAcademy
    assert project.status == ProjectStatusEnum.Done
    assert project.description == 'description'
    assert project.problem == 'problem'
    assert project.purpose == 'purpose'
    assert project.task == 'task'
    assert project.result == 'result'
    assert project.what_will_get == 'what_will_get'
    assert project.total == 'total'
    assert project.report == 'report'
    assert project.reason_rejection == 'reason_rejection'
    assert project.application_date == now
    assert project.company_id == 1


def test_create_project_stage_model(db_test, create_project_model):
    project, _ = create_project_model()

    start_date = datetime.datetime.now()
    finish_date = datetime.datetime.now()
    stage = ProjectStageModel(
        project_id=project.id,
        name='test',
        start_date=start_date,
        finish_date=finish_date,
    )
    stage.project = project
    db_test.add(stage)
    db_test.commit()

    assert stage.id == 1
    assert stage.project_id == project.id
    assert stage.name == 'test'
    assert stage.start_date == start_date
    assert stage.finish_date == finish_date
    assert stage.project == project


def test_create_project_managers_model(db_test, create_project_model, create_company_model):
    project, _ = create_project_model()

    company = create_company_model()
    contact = ContactModel(fio='test', company_id=company.id)

    project_managers = ProjectsManagersModel(participant=ProjectParticipant.Head)
    project_managers.contact = contact
    project.managers.append(project_managers)

    db_test.add(project)
    db_test.commit()

    assert project.managers[0].contact == contact
    assert project.managers[0].participant == ProjectParticipant.Head


def test_create_projects_curators_model(db_test, create_project_model, create_user_model):
    project, _ = create_project_model()

    user, _ = create_user_model()

    projects_curators = ProjectsCuratorsModel()
    projects_curators.curator = user
    project.curators.append(projects_curators)

    db_test.add(project)
    db_test.commit()

    assert project.curators[0].curator == user
    assert project.curators[0].project == project


def test_create_project_role_model(db_test, create_project_model, faker):
    project, _ = create_project_model()
    need_competence = CompetencyModel(name=faker.word())
    will_competence = CompetencyModel(name=faker.word())

    role = ProjectRoleModel(
        project_id=project.id,
        name='test',
        work_format=ProjectRoleWorkFormatEnum.RemoteWork,
        workload=1,
        filename='filename',
    )
    role.need_competencies.append(need_competence)
    role.will_competencies.append(will_competence)
    db_test.add(role)
    db_test.commit()

    assert project.roles[0] == role

    assert role.id == 1
    assert role.project_id == project.id
    assert role.name == 'test'
    assert role.work_format == ProjectRoleWorkFormatEnum.RemoteWork
    assert role.workload == 1
    assert role.filename == 'filename'

    assert role.need_competencies[0] == need_competence
    assert role.need_competencies[0].id == 1

    assert role.will_competencies[0] == will_competence
    assert role.will_competencies[0].id == 2
