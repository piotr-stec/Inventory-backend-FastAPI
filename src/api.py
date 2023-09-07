from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import Settings
from src.database.core import create_db
from src.devices.views import router as device_router
from src.employees.views import router as employee_router

sett = Settings()
create_db()

app = FastAPI(root_path=sett.root_path)

app.include_router(device_router)
app.include_router(employee_router)

