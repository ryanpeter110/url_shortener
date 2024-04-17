#############
## imports ##
#############

import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

#########################
## define config class ##
#########################

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """

    # Location of .env file
    model_config = SettingsConfigDict(env_file=os.getenv("CONFIG_PATH"))

    # Environment config
    env_type: str  # The environment type (e.g., prod, dev, testing)

    # Application docs config

    # The name of the application
    app_name: str
    # The version of the application
    app_version: str
    # The name of the contact person for the application
    app_contact_name: str
    # The email address of the contact person for the application
    app_contact_email: str
    # The link to the terms of service for the application
    app_terms_of_service_link: str
    # The basic username for accessing application APIs
    app_docs_basic_username: str
    # The basic password for accessing application APIs
    app_docs_basic_password: SecretStr

    # CORS config

    # List of allowed origins for CORS
    cors_allow_origins: list
    # Whether credentials are allowed for CORS
    cors_allow_credentials: bool
    # List of allowed HTTP methods for CORS
    cors_allow_methods: list
    # List of allowed headers for CORS
    cors_allow_headers: list

    # Whether to include Sentry middleware for error tracking (true/false)
    enforce_sentry_middleware: bool

    # Database config

    # The username for accessing the database
    db_username: SecretStr
    # The password for accessing the database
    db_password: SecretStr
    # The host address of the database
    db_host: str
    # The name of the database
    db_name: str
    # The port number of the database
    db_port: Optional[int] = None
    # Name of the collection that has URL mapping information
    db_url_mappings_collection_name: str

    # Logging config

    # The format of log messages
    log_format: str
    # The path to the log file
    log_file: str
    # The logging level
    log_level: int
    # The mode of logging
    log_mode: str
    # The maximum size of log files in bytes
    log_max_bytes: int
    # The number of backup log files to keep
    log_backup_count: int
    # The name of the logger
    log_logger_name: str
