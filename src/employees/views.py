from sqlalchemy.orm import Session
from src.employees import service
from src.employees import schemas
from src.auth.security import get_current_user
from src.employees.exceptions import UserIsNotAdminException, UserNameAlreadyExists, EmailAlreadyExists, UserNotFound, DeviceNotFound, DeviceIsLoaned, LoanedDeviceOrEmpNotFound, DeleteDenied
from sqlalchemy.exc import IntegrityError

from src.dependencies import get_db

from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/create_emp/", response_model=schemas.Emp)
def create_user(emp: schemas.EmpCreate, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        new_user = service.create_emp(emp, db, current_user)
        return new_user
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EmailAlreadyExists:
        raise HTTPException(status_code=404, detail="Email already exists")
    except UserNameAlreadyExists:
        raise HTTPException(status_code=404, detail="User name already exists")


@router.get("/emp_detailed_view/", response_model=list[schemas.EmpDetailed])
def get_all_emp_detailed(db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.show_all_users_detailed(db, current_user)
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_status/", response_model=schemas.Emp)
def change_admin_status_by_name(employee_status: schemas.EmpStatusUpdate, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.change_admin_status_by_name(employee_status, db, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add_device_owner/", response_model=schemas.DeviceOwner)
def add_device_owner(owner_create: schemas.DeviceOwnerCreate, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.add_device_owner(owner_create, db, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DeviceNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DeviceIsLoaned:
        raise HTTPException(status_code=404, detail="Device already has an owner")


@router.put("/return_device/{dev_id}/{emp_id}", status_code=status.HTTP_200_OK)
def return_device(return_data: schemas.ReturnDevice, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.return_device(return_data, db, current_user)
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LoanedDeviceOrEmpNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/emp_detailed_view/{emp_id}", response_model=schemas.EmpDetailed)
def emp_detailed_view(emp_id: int, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.show_user_detailed(emp_id, db, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_employee/{emp_id}", status_code=204)
def delete_employee(emp_id: int, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.delete_employee(emp_id, db, current_user)
    except DeleteDenied as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))