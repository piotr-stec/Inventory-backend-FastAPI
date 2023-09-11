from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db
from .exceptions import InvalidCredentialsException
from .schemas import LoginResponse
from src.employees.schemas import Emp
from src.auth import security


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        emp = security.authenticate_user(login_data.username, login_data.password, db)
        return security.sing_in(emp)

    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=Emp)
def read_users_me(current_user: Emp = Depends(security.get_current_user)):
    try:
        return current_user
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))