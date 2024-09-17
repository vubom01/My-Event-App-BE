import logging.config
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware


from app.api.api import router
from app.core.config import settings
from app.helpers.exception_handler import fastapi_error_handler, CustomException, http_exception_handler, \
    validation_exception_handler

sys.path = ['', '..'] + sys.path[1:]

logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs"
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router, prefix=settings.API_PREFIX)
    application.add_exception_handler(Exception, fastapi_error_handler)
    application.add_exception_handler(CustomException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)

    return application


app = get_application()

if __name__ == '__main__':
    uvicorn.run("main:app", port=settings.RUNNING_PORT, reload=True, access_log=False)