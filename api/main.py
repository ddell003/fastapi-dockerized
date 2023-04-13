from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .config import config
from .routers import UsersRouter, RolesRouter
from .utils import get_project_absolute_path


app = FastAPI(
    title="Api",
    version=__version__,
    docs_url="/api",  # disable the auto-generated docs
    redoc_url="/api/redoc",  # disable the auto-generated redocs
    openapi_url=f"{config.api_prefix}/openapi.json",
)

# add urls to list for CORS, allows a UI to connect to the api
origins = [config.allowed_origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix=config.api_prefix)
# Add additional routes below
router.include_router(UsersRouter)
router.include_router(RolesRouter)


app.mount(
    f"{config.api_prefix}/static",
    StaticFiles(directory=f"{get_project_absolute_path()}/static"),
    name="static",
)

app.include_router(router)
