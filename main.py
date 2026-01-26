import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Controllers.LoginController import router as login_router
from Controllers.Administrator.EmpleadoAdministrator import router as empleador_router
from Controllers.Administrator.HorarioAdiministrator import router as horario_router
from Controllers.Core.EmployeeReportController import router as report_router
app = FastAPI()

origins = [
    "http://localhost:5173", 
    "https://frontend-ingweb.onrender.com"
]

env_origins = os.getenv("ALLOWED_ORIGINS")

if env_origins:
    origins.extend(env_origins.split(","))

app.include_router(login_router)
app.include_router(empleador_router)
app.include_router(horario_router)
app.include_router(report_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)