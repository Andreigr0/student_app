from projects.models import ProjectModel, ProjectParticipant, ProjectRoleCompetenceType, ProjectRoleWorkFormatEnum, \
    ProjectStatusEnum, ProjectTypeEnum, ProjectView, ProjectStageModel
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
