from fastapi import APIRouter, Depends
from starlette import status

from app.tags import Tags
from invitations.schemas import Invitation, InvitationsQueryParams, InvitationsFilters, InvitationDetails

router = APIRouter(
    prefix='/invitations',
    tags=[Tags.invitations],
)


@router.get('/filters', summary='Получить доступные фильтры для приглашений')
def get_invitations_filters() -> InvitationsFilters:
    pass


@router.get('', summary='Получить все приглашения')
def get_invitations(filters: InvitationsQueryParams = Depends()) -> list[Invitation]:
    pass


@router.get('/{id}', summary='Приглашение X')
def get_invitation_details(id: int) -> InvitationDetails:
    pass


@router.patch('/{id}/accept', status_code=status.HTTP_202_ACCEPTED, summary='Принять приглашение')
def accept_invitation(id: int):
    pass


@router.delete('/{id}/refuse', status_code=status.HTTP_202_ACCEPTED, summary='Отказаться от приглашения')
def refuse_invitation(id: int, reason: str):
    pass


@router.patch('/{id}/archive', summary='Убрать в архив')
def archive_invitation(id: int) -> bool:
    pass
