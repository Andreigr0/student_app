from projects.models import ProjectModel, ProjectParticipant, ProjectRoleCompetenceType, ProjectRoleWorkFormatEnum, \
    ProjectStatusEnum, ProjectTypeEnum, ProjectView
import datetime


def test_create_project_model(db_test):
    now = datetime.datetime.now()
    project = ProjectModel(
        name='test',
        is_visible=True,
        type=ProjectTypeEnum.Research,
        view=ProjectView.DigitalAcademy,
        status=ProjectStatusEnum.Done,
        description='description',
        problem='problem',
        purpose='purpose',
        task='task',
        result='result',
        what_will_get='what_will_get',
        total='total',
        report='report',
        reason_rejection='reason_rejection',
        application_date=now,
    )
    db_test.add(project)
    db_test.commit()

    assert project.id == 1
    assert project.name == 'test'
    assert project.is_visible == True
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
