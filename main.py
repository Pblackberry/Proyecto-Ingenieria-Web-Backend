from fastapi import FastAPI
import uvicorn
from Controllers.LoginController import router as login_router
app = FastAPI()
app.include_router(login_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)