import datetime

from projects.models import ProjectStageModel
from reports.models import ReportModel


def test_create_report(db_test, create_student, create_project_model):
    student = create_student()
    project = create_project_model()

    stage = ProjectStageModel(
        name='Test stage',
        start_date=datetime.date(2021, 1, 1),
        finish_date=datetime.date(2021, 2, 1),
    )
    stage.project = project

    report = ReportModel(
        file_name='test.pdf',
        file_path='path/test.pdf',
        is_accepted=True,
    )
    report.student = student
    report.stage = stage

    db_test.add(stage)
    db_test.add(report)
    db_test.commit()

    assert report.student_id == 1
    assert report.stage_id == 1
    assert report.file_name == 'test.pdf'
    assert report.file_path == 'path/test.pdf'
    assert report.is_accepted is True
    assert report.project == project
