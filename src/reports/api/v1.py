from fastapi import APIRouter, Depends

from app.tags import Tags
from reports.schemas import Report, ProjectPeriods, ReportCreate, ReportUpdate
from shared.schemas import PaginationQuery

router = APIRouter(
    prefix='/reports',
    tags=[Tags.reports],
)


@router.get('/periods', summary='Получить периоды отчетов')
def get_report_periods() -> list[ProjectPeriods]:
    pass


@router.get('', summary='Получить все отчеты')
def get_reports(pagination: PaginationQuery = Depends()) -> list[Report]:
    pass


@router.post('', status_code=201, summary='Добавить новый отчет', tags=[Tags.projects])
def send_report(body: ReportCreate):
    pass


@router.patch('/{id}', summary='Заменить отчет', tags=[Tags.projects])
def update_report(id: int, body: ReportUpdate):
    pass
