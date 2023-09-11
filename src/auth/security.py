from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session

from src.employees.service import get_by_name
from ..employees.models import Employee
from src.auth.exceptions import InvalidCredentialsException, InactiveUserException
from .hashing import verify_password, get_password_hash
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from src.dependencies import get_db

from .schemas import TokenData, LoginResponse

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authenticate_user(emp_name: str, password: str, db: Session):
    emp = get_by_name(emp_name, db)
    if not emp:
        return False
    if not verify_password(password, emp.emp_password):
        return False
    return emp


def sing_in(emp: Employee) -> LoginResponse:
    if isinstance(emp, Employee):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": emp.emp_name}, expires_delta=access_token_expires)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = create_refresh_token(data={"sub": emp.emp_name}, expires_delta=refresh_token_expires)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "type": "bearer",
        }
    else:
        raise InvalidCredentialsException()  #


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Employee | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        emp_name: str = payload.get("sub")
        token_type: str = payload.get("type")
        if emp_name is None or token_type is None:
            raise InvalidCredentialsException()
        token_data = TokenData(username=emp_name, type=token_type)
    except JWTError:
        raise InvalidCredentialsException()
    emp = get_by_name(emp_name=token_data.username, db=db)
    if emp is None:
        raise InvalidCredentialsException()
    return emp


async def get_active_user(current_user: Employee = Depends(get_current_user)):
    if current_user is None:
        raise InactiveUserException()
    return current_user