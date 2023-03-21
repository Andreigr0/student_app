from fastapi import APIRouter, Depends

from app.tags import Tags
from reviews.schemas import ReviewDetails

router = APIRouter(
    prefix='/reviews',
    tags=[Tags.reviews],
)


@router.get('/{id}', summary='Получить отзыв')
def get_review(id: int) -> ReviewDetails:
    pass
