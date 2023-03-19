from fastapi import APIRouter

from app.tags import Tags
from curriculum.schemas import Curriculum, SubjectDetails, LiteratureDetails

router = APIRouter(
    prefix='/curriculum',
    tags=[Tags.curriculum],
)


@router.get('')
def get_curriculum() -> Curriculum:
    pass


@router.get('/{id}')
def get_subject(id: int) -> SubjectDetails:
    pass


@router.get('/{id}/literature')
def get_subject_literature(id: int) -> LiteratureDetails:
    pass
