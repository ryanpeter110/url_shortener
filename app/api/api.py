#############
## Imports ##
#############

from typing import Union

from fastapi import APIRouter, Body, Header, status, Request
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException

from pymongo.errors import DuplicateKeyError

from app import config, logger
from app.core.schema.request_schema import SystemShortenUrlRequest, CustomShortenUrlRequest
from app.core.schema.response_schema import ShortenUrlResponse
from app.core.models.models import UrlMappings
from app.utils.utils import create_short_key


##########
## APIs ##
##########

# Setup Router
api = APIRouter(default_response_class=ORJSONResponse)



# Routes
@api.post(
    "/shorten_url",
)
async def shorten_url(
    *,
    x_custom_shorten:bool = Header(False, alias="x-custom-shorten"),
    req_body : Union[SystemShortenUrlRequest, CustomShortenUrlRequest] = Body(...),
    request: Request,
):

    """
    Endpoint to shorten a URL.

    Args:
        x_custom_shorten (bool): Flag to indicate if custom shortening is requested.
        req_body (Union[SystemShortenUrlRequest, CustomShortenUrlRequest]): Request body
                                             containing target URL and optional custom key.
        request (Request): The FastAPI request object.

    Returns:
        ORJSONResponse: Response containing the shortened URL details.
    """

    _request_id = request.state.request_id
    _successful = True

    logger.info(f"[{_request_id}] query target url {req_body.target_url} in UrlMappings")
    url_mapping = await UrlMappings.find_one(
        {
            "target_url": req_body.target_url,
            "is_active": True
        }
    )


    _message = "a mapping between a key and this target_url already exists"
    _status_code = status.HTTP_200_OK

    logger.info(f"[{_request_id}] check if url_mappings exists")
    if not url_mapping:

        logger.info(f"[{_request_id}] create short key")
        short_key = create_short_key(req_body.short_key_length) if not x_custom_shorten else req_body.custom_key

        logger.info(f"[{_request_id}] create url_mappings")
        url_mapping = UrlMappings(
            target_url = req_body.target_url,
            short_key= short_key,
            hits = 0,
            is_active = True,
            is_custom_key = x_custom_shorten,
            tags = req_body.tags,
            app_version = config.app_version,
        )

        try:
            logger.info(f"[{_request_id}] insert url_mappings to db")
            await url_mapping.insert()

            _message = f"a mapping between a {short_key} and this {req_body.target_url} created"
            _status_code = status.HTTP_201_CREATED
        except DuplicateKeyError as e:
            _message = "duplicate short key error"
            _status_code = status.HTTP_400_BAD_REQUEST if x_custom_shorten else status.HTTP_500_INTERNAL_SERVER_ERROR
            raise HTTPException(status_code=_status_code, detail=_message) from e

    logger.info(f"[{_request_id}] create response")
    _response_body = ShortenUrlResponse.construct_response(
        successful=_successful,
        request_id=_request_id,
        message=_message,
        url_mapping=url_mapping
    )

    return ORJSONResponse(status_code=_status_code, content=_response_body.model_dump())



@api.get(
    "/{short_key}"
)
async def redirect_to_target_url(
    *,

    short_key: str,
    request: Request,

):

    """
    Endpoint to redirect to the target URL associated with a short key.

    Args:
        short_key (str): The short key to look up in the database.
        request (Request): The FastAPI request object.

    Returns:
        RedirectResponse: Redirects to the target URL if the short key is valid.
        HTTPException: Raises a 404 error if the short key is invalid.
    """

    _request_id = request.state.request_id

    logger.info(f"[{_request_id}] query short key {short_key} in UrlMappings")
    url_mapping = await UrlMappings.find_one(
        {
            "short_key": short_key,
            "is_active": True
        }
    )

    logger.info(f"[{_request_id}] check if url_mappings exists")
    if url_mapping:
        logger.info(f"[{_request_id}] update url_mappings hits ({url_mapping.hits})")
        url_mapping.hits = url_mapping.hits + 1
        logger.info(f"[{_request_id}] save update to url_mappings")
        await url_mapping.save()
        logger.info(f"[{_request_id}] redirecting to target_url {url_mapping.target_url}")
        return RedirectResponse(url_mapping.target_url)

    logger.info(f"[{_request_id}] url_mappings not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid short key")
