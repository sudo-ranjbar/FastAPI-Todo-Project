from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.tasks.routes import router as tasks_routes
from app.users.routes import router as users_routes
from app.auth.jwt_auth import get_authenticated_user


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
            "url": "https://stackoverflow.com",
        },
    }
]

app = FastAPI(
    title="Todo Sikim FastAPI",
    description="this is a tutorial todo backend service in fastapi",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Amirhossein Ranjbar",
        "url": "https://google.com",
        "email": "amh.ranjbar@gmail.com",
    },
    license_info={"name": "MIT", "url": "https://google.com"},
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(tasks_routes, prefix="/api/v1")
app.include_router(users_routes, prefix="/api/v1")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/private")
def private_route(user=Depends(get_authenticated_user)):
    print(user.id)
    return {"msg": "this is a private route"}
