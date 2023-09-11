import datetime

from sqlalchemy.orm import Session
from src.employees.schemas import EmpCreate, Emp, EmpStatusUpdate, DeviceOwnerCreate, ReturnDevice
from src.employees.models import Employee, DeviceOwner
from src.devices.models import DeviceLocation, Device
from src.auth.hashing import get_password_hash
from src.employees.exceptions import UserIsNotAdminException, EmailAlreadyExists, UserNameAlreadyExists, UserNotFound, DeviceNotFound, DeviceIsLoaned, LoanedDeviceOrEmpNotFound, DeleteDenied


def create_emp(employee: EmpCreate, db: Session, current_user: Emp):
    if current_user.is_admin:
        hashed_password = get_password_hash(employee.emp_password)
        if db.query(Employee).filter(Employee.emp_email == employee.emp_email).first():
            raise EmailAlreadyExists()
        if db.query(Employee).filter(Employee.emp_name == employee.emp_name).first():
            raise UserNameAlreadyExists()
        new_emp = Employee(emp_name=employee.emp_name, emp_first_name=employee.emp_first_name, emp_last_name=employee.emp_last_name, is_admin=employee.is_admin,
                           emp_email=employee.emp_email, emp_phone_number=employee.emp_phone_number, emp_password=hashed_password)
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return new_emp
    else:
        raise UserIsNotAdminException()


def get_all_emp(db: Session, current_user: Emp):
    if current_user.is_admin:
        employees = db.query(Employee).all()
        return employees
    else:
        raise UserIsNotAdminException()


def get_by_name(emp_name: str, db: Session) -> Employee:
    emp = db.query(Employee).filter(Employee.emp_name == emp_name).first()
    return emp


def change_admin_status_by_name(employee_status: EmpStatusUpdate, db: Session, current_user: Emp):
    if current_user.is_admin:
        emp = get_by_name(employee_status.emp_name, db)
        if not emp:
            raise UserNotFound()
        else:
            emp.is_admin = employee_status.is_admin
            db.commit()
            db.refresh(emp)
            return emp
    else:
        raise UserIsNotAdminException()


def add_device_owner(owner_create: DeviceOwnerCreate, db: Session, current_user: Emp):
    if current_user.is_admin:
        device = db.query(Device).filter_by(dev_id=owner_create.dev_id).first()
        if not device:
            raise DeviceNotFound()
        else:
            emp = db.query(Employee).filter_by(emp_id=owner_create.emp_id).first()
            if not emp:
                raise UserNotFound()
            else:
                device_owners = db.query(DeviceOwner).filter_by(dev_id=owner_create.dev_id)
                # CHECHKING IF DEVICE IS IN LOAN
                flag = False
                for loan in device_owners:
                    if loan.is_loan:
                        flag = True
                    else:
                        pass
                if not flag:
                    new_owner = DeviceOwner(dev_id=owner_create.dev_id, emp_id=owner_create.emp_id)
                    db.add(new_owner)
                    db.commit()
                    db.refresh(new_owner)
                    return new_owner
                else:
                    raise DeviceIsLoaned()
    else:
        raise UserIsNotAdminException()


def return_device(return_data: ReturnDevice, db: Session, current_user: Emp):
    if current_user.is_admin:
        device_owners = db.query(DeviceOwner).filter_by(dev_id=return_data.dev_id, emp_id=return_data.emp_id).all()
        if device_owners:
            for device in device_owners:
                if device.is_loan:
                    device.is_loan = False
                    device.return_date = datetime.date.today()
                    db.commit()
                    db.refresh(device)
                    location = db.query(DeviceLocation).filter_by(dev_id=device.dev_id).first()
                    location.location = ''
                    db.commit()
                    db.refresh(location)
                    return 'Returned'
        else:
            raise LoanedDeviceOrEmpNotFound()
    else:
        raise UserIsNotAdminException()


def show_all_users_detailed(db: Session, current_user: Emp):
    if current_user.is_admin:
        emp_all = db.query(Employee).all()
        responses = []
        for emp in emp_all:
            device_list = []
            device_owner = db.query(DeviceOwner).filter_by(emp_id=emp.emp_id)
            if not device_owner:
                pass
            else:
                for device in device_owner:
                    dev = db.query(Device).filter_by(dev_id=device.dev_id).first()
                    device_location = db.query(DeviceLocation).filter_by(dev_id=dev.dev_id).first()
                    if not device_location:
                        pass
                    else:
                        device_location_str = ""
                        if device_location.location:
                            device_location_str = device_location.location
                        else:
                            device_location_str = "Device has no secified lociation"

                    resp = {"dev_id": dev.dev_id ,
                            "dev_name": dev.dev_name,
                            "dev_type": dev.dev_type,
                            "dev_serial_number": dev.dev_serial_number,
                            "dev_location": device_location_str,
                            "is_loan": device.is_loan,
                            "start_date": device.start_date,
                            "return_date": device.return_date
                    }

                    device_list.append(resp)
            response = {
                "emp_id": emp.emp_id,
                "emp_name": emp.emp_name,
                "emp_first_name": emp.emp_first_name,
                "emp_last_name": emp.emp_last_name,
                "is_admin": emp.is_admin,
                "emp_email": emp.emp_email,
                "emp_phone_number": emp.emp_phone_number,
                "emp_devices": device_list,
            }
            responses.append(response)
        return responses
    else:
        raise UserIsNotAdminException()


def show_user_detailed(emp_id: int, db: Session, current_user: Emp):
    if current_user.is_admin:
        emp = db.query(Employee).filter_by(emp_id=emp_id).first()
        if not emp:
            raise UserNotFound()
        else:
            device_list = []
            device_owner = db.query(DeviceOwner).filter_by(emp_id=emp_id)
            if not device_owner:
                pass
            else:
                for device in device_owner:
                    dev = db.query(Device).filter_by(dev_id=device.dev_id).first()
                    device_location = db.query(DeviceLocation).filter_by(dev_id=dev.dev_id).first()
                    if not device_location:
                        pass
                    else:
                        device_location_str = ""
                        if device_location.location:
                            device_location_str = device_location.location
                        else:
                            device_location_str = "Device has no secified lociation"

                    resp = {"dev_id": dev.dev_id ,
                            "dev_name": dev.dev_name,
                            "dev_type": dev.dev_type,
                            "dev_serial_number": dev.dev_serial_number,
                            "dev_location": device_location_str,
                            "is_loan": device.is_loan
                    }
                    device_list.append(resp)
            response = {
                "emp_id": emp.emp_id,
                "emp_name": emp.emp_name,
                "emp_first_name": emp.emp_first_name,
                "emp_last_name": emp.emp_last_name,
                "is_admin": emp.is_admin,
                "emp_email": emp.emp_email,
                "emp_phone_number": emp.emp_phone_number,
                "emp_devices": device_list
            }
            return response
    else:
        raise UserIsNotAdminException()


def delete_employee(emp_id: int, db: Session, current_user: Emp):
    if current_user.is_admin:
        # finding parent and children objects
        employee = db.query(Employee).filter_by(emp_id=emp_id).first()
        device_owner = db.query(DeviceOwner).filter_by(emp_id=emp_id).all()
        if employee:
            # deleting all device_owners objects
            if device_owner:
                for dev_own in device_owner:
                    db.delete(dev_own)
                    db.commit()
            else:
                pass
            # Deleting only if current user is not user to delete
            if emp_id != current_user.emp_id:
                db.delete(employee)
                db.commit()
                return 'Deleted'
            else:
                raise DeleteDenied()

        else:
            raise UserNotFound()
    else:
        raise UserIsNotAdminException()


