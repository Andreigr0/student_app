import pytest

from competencies.models import CompetencyModel


@pytest.fixture
def create_project_role_model(db_test, create_project_model):
    from projects.models import ProjectRoleModel, WorkFormat

    def _create_project_role_model() -> ProjectRoleModel:
        project = create_project_model()
        competency1, competency2 = CompetencyModel(name='Test competency 1'), CompetencyModel(name='Test competency 2')

        role = ProjectRoleModel(
            work_load='Test work load',
            work_format=WorkFormat.full_time,
        )
        role.project = project

        role.needed_competencies.append(competency1)
        role.needed_competencies.append(competency2)

        role.acquired_competencies.append(competency1)

        db_test.add(role)
        db_test.commit()

        assert role.project_id == project.id
        assert set(role.needed_competencies) == {competency1, competency2}
        assert set(role.acquired_competencies) == {competency1}

        return role

    return _create_project_role_model
