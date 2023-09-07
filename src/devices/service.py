from sqlalchemy.orm import Session
from src.devices.models import Device
from src.devices.schemas import DeviceCreate


def add_device(device: DeviceCreate, db: Session) -> Device:
    new_device = Device(dev_name=device.dev_name, dev_type=device.dev_type,
                               dev_serial_number=device.dev_serial_number)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device