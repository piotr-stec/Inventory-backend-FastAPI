from sqlalchemy.orm import Session
from src.employees.schemas import EmpCreate
from src.employees.models import Employee
from src.auth.hashing import get_password_hash


def create_emp(employee: EmpCreate, db: Session):
    hashed_password = get_password_hash(employee.emp_password)
    new_emp = Employee(emp_name=employee.emp_name, emp_first_name=employee.emp_first_name, emp_last_name=employee.emp_last_name, is_admin=employee.is_admin,
                       emp_email=employee.emp_email, emp_phone_number=employee.emp_phone_number, emp_password=hashed_password)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp