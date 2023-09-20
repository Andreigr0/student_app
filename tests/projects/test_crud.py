from projects import crud
from projects.models import ProjectStatus, ProjectRoleModel, WorkFormat
from projects.schemas import ProjectsQueryParams
from shared.schemas import PaginationQuery


def test_get_projects(db_test, create_project_model, create_project_role_model):
    for _ in range(10):
        create_project_model()
        create_project_role_model()

    filters = ProjectsQueryParams(
        # statuses=[ProjectStatus.draft, ProjectStatus.under_recruitment,
        # ProjectStatus.recruited, ProjectStatus.finished, ProjectStatus.withdrawn],
    )

    projects = crud.get_projects(
        db=db_test,
        pagination=PaginationQuery(page=2, per_page=5),
        filters=filters,
    )
    assert len(projects) == 5
    assert projects[0].id == 6


def test_get_projects_filtered_by_roles(db_test, create_project_model):
    for _ in range(10):
        create_project_model()

    for i in range(1, 5):
        role = ProjectRoleModel(project_id=i, work_load='work load', work_format=WorkFormat.full_time)
        role2 = ProjectRoleModel(project_id=i, work_load='work load 2', work_format=WorkFormat.remote)
        db_test.add_all([role, role2])
        db_test.commit()

    projects = crud.get_projects(
        db=db_test,
        pagination=PaginationQuery(),
        filters=ProjectsQueryParams(roles=[1, 2, 3]),
    )
    assert len(projects) == 2
    assert projects[0].id == 1
    assert projects[0].roles[0].id == 1
    assert projects[0].roles[1].id == 2

    assert projects[1].id == 2
    assert projects[1].roles[0].id == 3
