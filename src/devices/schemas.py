from datetime import date
from typing import Optional
from pydantic import BaseModel


class DeviceBase(BaseModel):
    dev_name: str
    dev_type: str
    dev_serial_number: str


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    dev_id: int
    dev_date_of_purchase = str


class Device(DeviceBase):
    dev_id: int

    class Config:
        orm_mode = True


class DeviceDetailLocation(BaseModel):
    dev_id: int
    dev_name: str
    dev_type: str
    dev_serial_number: str
    dev_location: str
    is_loan: bool
    start_date: Optional[date] = None
    return_date: Optional[date] = None


class DeviceDetail(Device):
    dev_location: str
    dev_owner_id: str
    dev_owner_name: str
    is_loan: bool


class DeviceLocationBase(BaseModel):
    dev_id: int
    location: str


class DeviceLocationCreate(DeviceLocationBase):
    pass


class DeviceLocation(DeviceLocationBase):
    id: int

    class Config:
        orm_mode = True



