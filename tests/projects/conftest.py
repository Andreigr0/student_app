import datetime

import pytest

from projects.models import ProjectModel, ProjectTypeEnum, ProjectView, ProjectStatusEnum


@pytest.fixture
def create_project_model(db_test, faker):
    def _create() -> (ProjectModel, datetime.datetime):
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
        return project, now

    return _create
