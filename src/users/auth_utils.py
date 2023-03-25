from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from users import crud
from users.models import UserModel
from users.schemas import TokenData

SECRET_KEY = '192029edef6c99a349ea731dbf668b07719bd0ce95d82dcde49a258561baee2e'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> bool | UserModel:
    user: UserModel = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def not_authorized_user(token=Header(default=None, alias='Authorization')) -> None:
    exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are already authorized')

    if token is not None:
        raise exception


async def authorized_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
    )

    if token is None:
        raise credentials_exception

    try:
        payload = decode_token(token)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, token_data.username)

    if user is None:
        raise credentials_exception

    return user
