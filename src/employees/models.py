from datetime import date
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date

from src.database.core import Base


class Employee(Base):
    __tablename__ = "emp"
    emp_id = Column(Integer, primary_key=True, index=True)
    emp_name = Column(String, unique=True)
    emp_first_name = Column(String)
    emp_last_name = Column(String)
    is_admin = Column(Boolean, default=False)
    emp_phone_number = Column(String)
    emp_email = Column(String, unique=True)
    emp_password = Column(String)


class DeviceOwner(Base):
    __tablename__ = 'device_owners'
    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("emp.emp_id"))
    dev_id = Column(Integer, ForeignKey("dev.dev_id"))
    is_loan = Column(Boolean, default=True)
    start_date = Column(Date, default=date.today)
    return_date = Column(Date, nullable=True)