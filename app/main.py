from fastapi import FastAPI

from app.api.v1.routers import router as v1_routers

app = FastAPI(
    title="API Task Manager",
    version="1.0.0",
    contact={
        "name": "Adolfo Guimarães",
        "url": "https://github.com/adolfoguimaraes",
    },
     license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }

)

app.include_router(v1_routers, prefix="/api/v1") 