import datetime

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


class DeviceLocationBase(BaseModel):
    dev_id: int
    location: str


class DeviceLocationBaseCreate(DeviceLocationBase):
    pass


class DeviceLocation(DeviceLocationBase):
    id: int

    class Config:
        orm_mode = True


