from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

from src.database.core import Base


class Device(Base):
    __tablename__ = "dev"
    dev_id = Column(Integer, primary_key=True, index=True)
    dev_name = Column(String)
    dev_type = Column(String)
    dev_serial_number = Column(String)
    dev_date_of_purchase = Column(String)


class DeviceLocation(Base):
    __tablename__ = "devLocation"
    id = Column(Integer, primary_key=True, index=True)
    dev_id = Column(Integer, ForeignKey("dev.dev_id"))
    location = Column(String)
