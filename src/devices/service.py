from sqlalchemy.orm import Session
from src.devices.models import Device, DeviceLocation
from src.employees.models import Employee, DeviceOwner
from src.devices.schemas import DeviceCreate, DeviceLocationCreate
from src.employees.schemas import Emp

from src.devices.exceptions import UserIsNotAdminException, DeviceNotFound, DeviceLocationNotFound


def add_device(device: DeviceCreate, db: Session, current_user: Emp):
    if current_user.is_admin:
        new_device = Device(dev_name=device.dev_name, dev_type=device.dev_type,
                            dev_serial_number=device.dev_serial_number)
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        new_device_location = DeviceLocation(dev_id=new_device.dev_id)
        db.add(new_device_location)
        db.commit()
        db.refresh(new_device_location)
        return new_device
    else:
        raise UserIsNotAdminException()


def get_all_devices(db: Session):
    return db.query(Device).all()


def get_device_by_id(dev_id: int, db: Session):
    device = db.query(Device).filter_by(dev_id=dev_id).first()
    if not device:
        raise DeviceNotFound
    else:
        return device


def change_device_location(dev_location: DeviceLocationCreate, db: Session, current_user: Emp):
    if current_user.is_admin:
        new_location = db.query(DeviceLocation).filter_by(dev_id=dev_location.dev_id).first()
        if not new_location:
            raise DeviceNotFound()
        else:
            new_location.location = dev_location.location
            db.commit()
            db.refresh(new_location)
            return new_location
    else:
        raise UserIsNotAdminException()


def show_device_detailed(dev_id: int, db: Session, current_user: Emp):
    if current_user.is_admin:
        device = get_device_by_id(dev_id, db)
        if not device:
            raise DeviceNotFound()
        else:
            device_location = db.query(DeviceLocation).filter_by(dev_id=dev_id).first()
            if not device_location:
                raise DeviceLocationNotFound()
            else:
                # setting location string
                device_location_str = ""
                if device_location.location:
                    device_location_str = device_location.location
                else:
                    device_location_str = "Device has no specified location"
                device_owner = db.query(DeviceOwner).filter_by(dev_id=dev_id).all()
                # Checking if device has owner
                for dev in device_owner:
                    if dev.is_loan:
                        owner = db.query(Employee).filter_by(emp_id=dev.emp_id).first()
                        # Response if device has active owner
                        response = {"dev_id": dev_id, "dev_name": device.dev_name, "dev_type": device.dev_type,
                                    "dev_serial_number": device.dev_serial_number,
                                    "dev_location": device_location_str,
                                    "dev_owner_id": str(dev.emp_id),
                                    "dev_owner_name": owner.emp_name,
                                    "is_loan": dev.is_loan

                                    }
                        return response
                # Response if device does not have active owner
                response = {"dev_id": dev_id, "dev_name": device.dev_name, "dev_type": device.dev_type,
                            "dev_serial_number": device.dev_serial_number,
                            "dev_location": device_location_str,
                            "dev_owner_id": "Device has no owner",
                            "dev_owner_name": "Device has no owner",
                            "is_loan": False
                            }
                return response
    else:
        raise UserIsNotAdminException()


def show_all_device_detailed(db: Session, current_user: Emp):
    if current_user.is_admin:
        devices = get_all_devices(db)
        responses = []
        for device in devices:
            device_location = db.query(DeviceLocation).filter_by(dev_id=device.dev_id).first()
            if not device_location:
                raise DeviceLocationNotFound()
            else:
                device_location_str = ""
                if device_location.location:
                    device_location_str = device_location.location
                else:
                    device_location_str = "Device has no specified location"
                device_owner = db.query(DeviceOwner).filter_by(dev_id=device.dev_id).all()
                # Checking if device has owner
                for dev in device_owner:
                    if dev.is_loan:
                        owner = db.query(Employee).filter_by(emp_id=dev.emp_id).first()
                        # Response if device has active owner
                        response = {"dev_id": device.dev_id, "dev_name": device.dev_name, "dev_type": device.dev_type,
                                    "dev_serial_number": device.dev_serial_number,
                                    "dev_location": device_location_str,
                                    "dev_owner_id": str(dev.emp_id),
                                    "dev_owner_name": owner.emp_name,
                                    "is_loan": dev.is_loan

                                    }
                        responses.append(response)
                # Response if device does not have active owner
                response = {"dev_id": device.dev_id, "dev_name": device.dev_name, "dev_type": device.dev_type,
                            "dev_serial_number": device.dev_serial_number,
                            "dev_location": device_location_str,
                            "dev_owner_id": "Device has no owner",
                            "dev_owner_name": "Device has no owner",
                            "is_loan": False
                            }
                responses.append(response)

        return responses
    else:
        raise UserIsNotAdminException()


def delete_device(dev_id: int, db: Session, current_user: Emp):
    if current_user.is_admin:
        # finding parent and children objects
        device = db.query(Device).filter_by(dev_id=dev_id).first()
        device_owner = db.query(DeviceOwner).filter_by(dev_id=dev_id).all()
        device_location = db.query(DeviceLocation).filter_by(dev_id=dev_id).first()
        if device:
            #     deleting all device_owners objects
            if device_owner:
                for dev_own in device_owner:
                    db.delete(dev_own)
                    db.commit()
            else:
                pass
            #   deleting device location
            db.delete(device_location)
            db.commit()
            #   deleting Device
            db.delete(device)
            db.commit()
            return 'Deleted'
        else:
            raise DeviceNotFound()
    else:
        raise UserIsNotAdminException()
