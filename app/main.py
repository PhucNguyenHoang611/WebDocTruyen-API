import uvicorn
from fastapi import FastAPI
from routers.base import api_router
from config.database import create_tables

app = FastAPI(title="Website Doc Truyen Online - API", version="0.0.1")
app.include_router(api_router, prefix="/api")

create_tables()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)