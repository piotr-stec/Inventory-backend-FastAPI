from sqlalchemy.orm import Session
from src.employees import service
from src.employees import schemas

from src.dependencies import get_db

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/", response_model=schemas.Emp)
def create_user(emp: schemas.EmpCreate, db: Session = Depends(get_db)):
    new_user = service.create_emp(emp, db)
    return new_user