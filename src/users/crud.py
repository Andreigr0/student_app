from sqlalchemy.orm import Session

from users.models import UserModel
from users.schemas import UserCreate, UserUpdate
from users.auth_utils import hash_password


def create_user(db: Session, user: UserCreate) -> UserModel:
    hashed_password = hash_password(user.password)
    db_user = UserModel(email=user.email, hashed_password=hashed_password, login=user.login)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserModel]:
    return db.query(UserModel).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, update: UserUpdate) -> UserModel | None:
    user = get_user(db=db, user_id=user_id)
    if user is None:
        return None

    for key, value in update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    if update.password is not None:
        user.hashed_password = hash_password(update.password)

    db.commit()
    return user
