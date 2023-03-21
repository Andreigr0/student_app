from fastapi import APIRouter, Depends

from app.tags import Tags
from attendance.schemas import Attendance
from shared.schemas import SemesterQuery

router = APIRouter(
    prefix='/attendance',
    tags=[Tags.attendance],
)


@router.get('', summary='Получить посещаемость')
def get_attendance(semester: SemesterQuery = Depends()) -> Attendance:
    pass
