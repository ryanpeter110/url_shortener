#############
## Imports ##
#############

from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field

from app import config

############
## Models ##
############


class UrlMappings(Document):
    """
    Represents URL mappings for clients with various attributes.
    
    Attributes:
    - target_url (str): Unique indexed field representing the target URL for redirection.
    - short_key (str): Unique indexed field for the short key for the URL, used for redirection.
    - hits (int): Integer representing the number of hits or accesses to the URL.
    - is_active (bool): Boolean indicating whether the URL mapping is active, default is True.
    - is_custom_key (bool): Boolean indicating whether the 
                            short key is custom or auto-generated, default is False.
    - tags (list): List representing tags associated with the URL mapping.
    - app_version (str): Field representing the application version associated with the URL mapping.
    - create_date (datetime): DateTime representing the creation date for the URL mapping, 
                              default is the current datetime.
    
    Settings:
    - name (str): Collection name for storing URL mappings data.
    """

    target_url: str = Field(...)
    short_key: Indexed(str, unique=True) = Field(...)
    hits: int = Field(default=0)
    is_active: bool = Field(default=True)
    is_custom_key: bool = Field(default=False)
    tags: list = Field(default=None)
    app_version: str = Field(...)
    create_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = config.db_url_mappings_collection_name
        indexes = [
            [("target_url", 1), ("is_active", 1)],  # Compound unique index
        ]
