from sqlalchemy.orm import Session

from src.devices import service
from src.devices.schemas import Device, DeviceCreate, DeviceUpdate, DeviceLocation

from src.dependencies import get_db

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/device", tags=["device"])


@router.post("/", response_model=Device)
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    added_device = service.add_device(device, db)
    return added_device