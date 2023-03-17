from reports.models import StudentReportModel


def test_create_student_report(db_test):
    report = StudentReportModel(
        filename='test.pdf',
        is_accepted=True,
        content_type='application/pdf',
        file_size=1000,
    )
    db_test.add(report)
    db_test.commit()

    assert report.id is not None
    assert report.filename == 'test.pdf'
    assert report.is_accepted is True
    assert report.content_type == 'application/pdf'
    assert report.file_size == 1000
