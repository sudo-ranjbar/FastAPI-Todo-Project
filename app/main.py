from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup")
    yield
    print("Application Shutdown")

tags_metadata = [
    {
        "name": "tasks",
        "descriptions": "Operations related to tasks management",
        "externalDocs": {
            "descriptions": "More about tasks",
            "url": "https://stackoverflow.com"
        }
    }
]

app = FastAPI(
    title="Todo Sikim FastAPI",
    description="this is a tutorial todo backend service in fastapi",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name":"Amirhossein Ranjbar",
        "url": "https://google.com",
        "email": "amh.ranjbar@gmail.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://google.com"
    },
    lifespan=lifespan, openapi_tags=tags_metadata)

app.include_router(tasks_routes, prefix="/api/v1")