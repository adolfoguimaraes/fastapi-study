from fastapi import FastAPI

from app.api.v1.routers import router as v1_routers

app = FastAPI()

app.include_router(v1_routers, prefix="/api/v1") 