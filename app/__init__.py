#############
## Imports ##
#############


import os
import time
from uuid import uuid4
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError

from app.logger import Rotolog
from app.config import Settings
from app.core.clients.database_client import DatabaseClient


###########################
## Logger / Config Setup ##
###########################


# Initialize config object
config = Settings()

# Create ogs directory if it does not exist
if not os.path.exists(os.path.dirname(config.log_file)):
    os.makedirs(os.path.dirname(config.log_file))

# Initialize Logger Object
logger = Rotolog(
    log_file_name=config.log_file,
    log_format=config.log_format,
    max_log_files=config.log_backup_count,
    max_log_file_size=config.log_max_bytes,
    log_level=config.log_level
)

logger.info("application started")


###################
## Clients Setup ##
###################


# Setup DatabaseClient
database_client = DatabaseClient(
    db_username=config.db_username.get_secret_value(),
    db_password=config.db_password.get_secret_value(),
    db_host=config.db_host,
    db_name=config.db_name,
    db_port=config.db_port,
)
logger.debug(f"setup databaseclient {database_client}")



#####################
## Lifespan Events ##
#####################

from app.core.models.models import UrlMappings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """    
    Establishes a database connection when entering the context and closes it when exiting.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Yields control back to the caller after setting up the database connection.
    """

    # Create DB connection
    await database_client.connect([UrlMappings, ])
    
    try:
        yield
    finally:
        # Close DB connection when exiting
        await database_client.disconnect()

###################
## Fastapi Setup ##
###################


# initialize fastapi object
app = FastAPI(
    lifespan=lifespan,
    title=config.app_name,
    version=config.app_version,
    contact={
        "name": config.app_contact_name,
        "email": config.app_contact_email,
    },
    default_response_class=ORJSONResponse,
    docs_url=None,
    redoc_url=None
)

logger.debug("fastapi object initialized")  # log fastapi initialization


################
## Middleware ##
################


# middleware to log incoming requests and outgoing responses.
@app.middleware("http")
async def log_requests(request: Request, call_next):

    """
    middleware to log incoming requests and outgoing responses.

    args:
        request (Request): the incoming request.
        call_next (callable): the next handler in the middleware chain.

    returns:
        Response: the response to be sent.
    """

    start_time = time.time()
    request_id = str(uuid4())

    # log the request received, including headers and body
    logger.info(f"[{request_id}] received - client host:{request.client.host} request:{request.method} {request.url.path} headers:{request.headers}")

    request.state.request_id = request_id
    response = await call_next(request)
    execution_time = time.time() - start_time

    # log response
    logger.info(f"[{request_id}] sent - client host:{request.client.host} request:{request.method} {request.url.path} status code:{response.status_code} execution time:{execution_time}")
    return response

logger.debug("added logging middleware")


# Middleware to handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_allow_origins,
    allow_credentials=config.cors_allow_credentials,
    allow_methods=config.cors_allow_methods,
    allow_headers=config.cors_allow_headers,
)
logger.debug("added cors middleware")


# TO-DO
if config.enforce_sentry_middleware:
    ...


################
## Setup Apis ##
################

@app.get("/ping", tags=["management"], include_in_schema=False)
async def ping():
    """
    Define a route for the "/ping" endpoint to check the health and version of the application.

    Returns:
    - ORJSONResponse: A JSON response indicating the success of the ping, the application version,
                      and a debug message to check if changes have been deployed.
    """
    # Define the content of the response
    content = {
        "success": True,
        "version": config.app_version,
        "debug_message": "1"
    }

    # Return the response with a 200 OK status code
    return ORJSONResponse(status_code=status.HTTP_200_OK, content=content)


# Add router to main FastAPI app
from app.api.api import api
app.include_router(api, prefix="")
logger.debug("added router to main FastAPI app")


############################
## API Exception Handlers ##
############################

from app.core.schema.response_schema import ErrorResponse


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: Exception):
    """
    Exception handler for RequestValidationError.

    This function handles validation errors raised by FastAPI due to invalid request data.
    It logs the error details and returns an error response.

    Args:
    - request (Request): The incoming request causing the validation error.
    - exc (Exception): The RequestValidationError raised.

    Returns:
    - ORJSONResponse: A JSON response containing the validation error details.
    """

    # Extract request_id from request state
    _request_id = request.state.request_id

    # Extract the error message from the exception and log it
    logger.error(f"[{_request_id}] {exc.args}")

    # Construct ErrorResponse
    _response_body = ErrorResponse.construct_response(
        request_id=_request_id,
        message="invalid input data",
        data=exc.args
    )

    # Return an ORJSONResponse with the ErrorResponse content and HTTP 500 status code
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_response_body.model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: Exception):
    """
    Exception handler for HTTPException.

    This function is responsible for handling HTTPException raised within the application.
    It logs the exception details and returns an error response.

    Args:
    - request (Request): The incoming request causing the exception.
    - exc (Exception): The HTTPException raised.

    Returns:
    - ORJSONResponse: A JSON response containing the error details.
    """

    # Extract request_id from request state
    _request_id = request.state.request_id

    # Extract the error message from the exception and log it
    logger.error(f"[{_request_id}] {exc.status_code} {exc.detail}")

    # Construct ErrorResponse
    _response_body = ErrorResponse.construct_response(
        request_id=_request_id,
        message=exc.detail,
        data=None
    )

    # Return an ORJSONResponse with the ErrorResponse content and HTTP 500 status code
    return ORJSONResponse(
        status_code=exc.status_code,
        content=_response_body.model_dump()
    )


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def internal_server_error_exception_handler(request: Request, exc: Exception):
    """
    Exception handler to deal with unexpected internal server errors (HTTP 500).
    
    Args:
    - request (Request): The incoming request that caused the exception.
    - exc (Exception): The exception instance caught by the handler.
    
    Returns:
    - ORJSONResponse: JSON response with an error message and HTTP 500 status code.
    
    Actions:
    - Logs the error in the log file using the logger.
    - Constructs an ErrorResponse with the error message and other metadata.
    """

    _request_id = request.state.request_id

    # Extract the error message from the exception and log it
    error_message = str(exc.with_traceback(None))
    logger.error(f"[{_request_id}] {error_message}")

    # Construct ErrorResponse
    _response_body = ErrorResponse.construct_response(
        request_id=_request_id,
        message=error_message,
        data=None
    )

    # Return an ORJSONResponse with the ErrorResponse content and HTTP 500 status code
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_response_body.model_dump()
    )
