from fastapi import APIRouter, Depends

from academic_performance.schemas import AcademicPerformance
from app.tags import Tags
from shared.schemas import SemesterQuery

router = APIRouter(
    prefix='/academic_performance',
    tags=[Tags.academic_performance],
)


@router.get('', summary='Получить успеваемость')
def get_academic_performance(semester: SemesterQuery = Depends()) -> AcademicPerformance:
    pass
