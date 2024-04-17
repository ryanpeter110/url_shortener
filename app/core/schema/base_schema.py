#############
## Imports ##
#############

from datetime import datetime
from pydantic import BaseModel

##################
## Base Schemas ##
##################


class BaseResponse(BaseModel):
    """
    Base schema for API responses.
    """
    meta: BaseModel  # Metadata for the response
    data: BaseModel  # Data payload for the response (information regarding shortened url)

class BaseMeta(BaseModel):
    """
    Base schema for metadata in API responses.
    """
    successful: bool  # Indicates if the request was successful
    request_id: str  # Unique identifier for the request
    message: str  # Message related to the request
    create_date: datetime  # Date and time of the response creation

class ShortenUrlData(BaseModel):
    """
    Schema for data related to shortened URLs in API responses.
    """
    mapping_id: str  # Unique identifier for the URL mapping
    target_url: str  # Original URL being shortened
    short_key: str  # Shortened key or URL
    hits: int  # Number of hits or accesses to the shortened URL
    is_active: bool  # Indicates if the URL mapping is active
    is_custom_key: bool  # Indicates if the key is user-generated
    tags: list  # List of tags associated with the URL mapping
    app_version: str  # Version of the application handling the mapping
