from sqlalchemy.orm import Session

from src.employees import schemas
from src.devices import service
from src.devices.schemas import Device, DeviceCreate, DeviceUpdate, DeviceLocation, DeviceLocationCreate, DeviceDetail
from src.auth.security import get_current_user
from src.devices.exceptions import UserIsNotAdminException, DeviceNotFound, DeviceLocationNotFound
from src.dependencies import get_db

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/device", tags=["device"])


@router.post("/add_device/", response_model=Device)
def add_device(device: DeviceCreate, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        added_device = service.add_device(device, db, current_user)
        return added_device
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/device_detailed_view/", response_model=list[DeviceDetail])
def get_all_devices_detailed(db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.show_all_device_detailed(db, current_user)
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/device_detailed_view/{dev_id}", response_model=DeviceDetail)
def device_detailed_view(dev_id: int, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        detailed_view = service.show_device_detailed(dev_id, db, current_user)
        return detailed_view
    except DeviceNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DeviceLocationNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.get("/{dev_id}", response_model=Device)
# def get_device_by_id(dev_id: int, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
#     try:
#         device = service.get_device_by_id(dev_id, db)
#         return device
#     except DeviceNotFound as e:
#         raise HTTPException(status_code=400, detail=str(e))


@router.put("/change_device_location/", response_model=DeviceLocation)
def change_device_location(dev_location: DeviceLocationCreate, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        new_location = service.change_device_location(dev_location, db, current_user)
        return new_location
    except DeviceNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/device_delete/{dev_id}", status_code=204)
def delete_device(dev_id: int, db: Session = Depends(get_db), current_user: schemas.Emp = Depends(get_current_user)):
    try:
        return service.delete_device(dev_id, db, current_user)
    except DeviceNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserIsNotAdminException as e:
        raise HTTPException(status_code=400, detail=str(e))


