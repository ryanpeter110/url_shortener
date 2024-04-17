#############
## Imports ##
#############

from datetime import datetime
from typing import Any
from app.core.schema.base_schema import BaseMeta, ShortenUrlData, BaseResponse

######################
## Response Schemas ##
######################

class ShortenUrlResponse(BaseResponse):
    """
    Response schema for the API endpoint that shortens URLs.
    """
    meta: BaseMeta  # Metadata for the response
    data: ShortenUrlData  # Data payload for the response (information regarding shortened url)

    @classmethod
    def construct_response(cls, successful:bool, request_id:str, message:str, url_mapping):
        """
        Constructs a ShortenUrlResponse object with the given parameters.

        Args:
            successful (bool): Indicates if the operation was successful.
            request_id (str): The ID of the request.
            message (str): The message associated with the response.
            url_mapping (Union[SystemShortenUrlRequest, CustomShortenUrlRequest]): The URL mapping
                                                    object containing details of the shortened URL.

        Returns:
            ShortenUrlResponse: The constructed ShortenUrlResponse object.
        """

        base_meta = BaseMeta(
            successful= successful,
            request_id= request_id,
            message= message,
            create_date= datetime.now(),
        )

        shorten_url_data = ShortenUrlData(
            mapping_id= str(url_mapping.id),
            target_url= url_mapping.target_url,
            short_key= url_mapping.short_key,
            hits= url_mapping.hits,
            is_active= url_mapping.is_active,
            is_custom_key= url_mapping.is_custom_key,
            tags= url_mapping.tags,
            app_version= url_mapping.app_version,
        )

        return cls(
            meta = base_meta,
            data = shorten_url_data
        )

class ErrorResponse(BaseResponse):
    """
    Response schema for error responses.
    """
    meta : BaseMeta  # Metadata for the response
    data : Any = None # No data payload for error responses

    @classmethod
    def construct_response(cls, request_id: str, message: str, data: Any = None) -> 'ErrorResponse':
        """
        Constructs an ErrorResponse object with the given parameters.

        Args:
        - request_id (str): The ID of the request causing the error.
        - message (str): The error message.
        - data (dict, optional): Additional data to include in the error response.

        Returns:
        - ErrorResponse: The constructed error response object.
        """
        base_meta = BaseMeta(
            successful=False,
            request_id=request_id,
            message=message,
            create_date=datetime.now(),
        )
        return cls(
            meta=base_meta,
            data=data
        )
