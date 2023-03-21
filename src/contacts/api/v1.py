from fastapi import APIRouter, Query

from app.tags import Tags
from contacts.schemas import Department, PersonDetails

router = APIRouter(
    prefix='/contacts',
    tags=[Tags.contacts],
)


@router.get('', summary='Получить контакты')
def get_contacts(query: str | None = Query(default=None,
                                           description='Фильтрация по названию сотрудника или подразделения')) -> Department:
    pass


@router.get('/{id}', summary='Получить информацию о сотруднике')
def get_contact(id: int) -> PersonDetails:
    pass
