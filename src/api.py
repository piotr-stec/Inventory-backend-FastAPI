from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import Settings
from src.database.core import create_db
from src.devices.views import router as device_router
from src.employees.views import router as employee_router
from src.auth.views import router as auth_router

sett = Settings()
create_db()

app = FastAPI(root_path=sett.root_path)


origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(device_router)
app.include_router(employee_router)
app.include_router(auth_router)


