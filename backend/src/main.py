import os
import sys
sys.path.insert(0, os.getcwd())

import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from endpoints import inference, status
from utils.custom_logger import logger
from utils.custom_error_handlers import BaseSystemError, PydanticError


# Create API Application
app = FastAPI()

@app.exception_handler(PydanticError)
async def validation_exception_handler(request, err) -> JSONResponse:
    """
    Pydantic model exceptions will be caught here
    :param request: Request to endpoint
    :param err: Error message caught in lower level
    :return: JSONResponse with error message
    """
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    logger.error(base_error_message)
    return JSONResponse(status_code=400,
                        content={"message": f"{base_error_message}: Error in data format", "detail": f"{err}"})


@app.exception_handler(BaseSystemError)
async def unknown_exception_handler(request, err):
    """
    All non-defined exceptions will be caught here
    :param request: Request to endpoint
    :param err: Error message caught in lower level
    :return: JSONResponse with error message
    """
    base_error_message = f"Unknown error. Failed to execute: {request.method}: {request.url}"
    logger.error(base_error_message)
    return JSONResponse(status_code=400,
                        content={"message": f"{base_error_message}", "detail": f"{err}"})


# Add endpoints
app.include_router(status.router)
app.include_router(inference.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=config("API_PORT", default=8000, cast=int),
                log_level=config("LOG_LEVEL", default="info", cast=str),
                reload=True)
