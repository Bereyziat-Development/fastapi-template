from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import EnvTag, settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    if settings.TAG == EnvTag.PROD:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    elif settings.TAG == EnvTag.STAG:
        # CORS set for a frontend app in staging environment deployed on any Vercel Preview - Modify this accordingly to match the pattern of your preview environment or more strictly to match the url of your staging deployment. Mobile apps do not need any specific CORS settings to be able to call the backend
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex="https://.*\.vercel\.app",  # noqa
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    elif settings.TAG == EnvTag.DEV:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        raise Exception(f"Provided TAG: {settings.TAG} is not supported")

app.include_router(api_router, prefix=settings.API_V1_STR)
