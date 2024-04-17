#############
## Imports ##
#############

from typing import Union
from pydantic import BaseModel

#####################
## Request Schemas ##
#####################

class ShortenUrlRequest(BaseModel):
    """
    Schema for the request to shorten a URL. 
    """
    target_url: str  # The original URL to be shortened
    tags: Union[list, None]  # Optional list of tags associated with the URL

    def __getattr__(self, name):
        """
        Overrides the default behavior for attribute access.
        """
        return None

class SystemShortenUrlRequest(ShortenUrlRequest):
    """
    Schema for system-generated shortened URLs.
    """
    short_key_length: int  # Length of the shortened key

class CustomShortenUrlRequest(ShortenUrlRequest):
    """
    Schema for custom shortened URLs.
    """
    custom_key: str  # The custom key provided for the shortened URL
