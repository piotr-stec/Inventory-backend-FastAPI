from pydantic import BaseModel, EmailStr, validator
from datetime import date
from src.devices.schemas import DeviceDetailLocation


class EmpBase(BaseModel):
    emp_name: str
    emp_first_name: str
    emp_last_name: str
    is_admin: bool = False
    emp_email: EmailStr
    emp_phone_number: str


class EmpCreate(EmpBase):
    emp_password: str

    @validator('emp_password')
    def password_must_contain_number(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain a number')
        return v

    @validator('emp_password')
    def password_must_contain_uppercase(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain an uppercase letter')
        return v

    @validator('emp_password')
    def password_must_contain_lowercase(cls, v):
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain a lowercase letter')
        return v

    @validator('emp_password')
    def password_must_contain_special_character(cls, v):
        if not any(not char.isalnum() for char in v):
            raise ValueError('Password must contain a special character')
        return v


class EmpUpdate(EmpBase):
    emp_id: int


class EmpStatusUpdate(BaseModel):
    emp_name: str
    is_admin: bool = True


class Emp(EmpBase):
    emp_id: int

    class Config:
        orm_mode = True


class DeviceOwnerBase(BaseModel):
    emp_id: int
    dev_id: int


class ReturnDevice(BaseModel):
    dev_id: int
    emp_id: int





class DeviceOwnerCreate(DeviceOwnerBase):
    pass


class DeviceOwner(DeviceOwnerBase):
    id: int

    class Config:
        orm_mode = True


# class ReturnDeviceResponseView(DeviceOwner):
#     is_loan: bool
#     start_date: date
#     return_date: date


class EmpDetailed(BaseModel):
    emp_id: int
    emp_name: str
    emp_first_name: str
    emp_last_name: str
    is_admin: bool
    emp_email: EmailStr
    emp_phone_number: str
    emp_devices: list[DeviceDetailLocation]
