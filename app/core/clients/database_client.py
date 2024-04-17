#############
## Imports ##
#############

from typing import List
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


####################
## DatabaseClient ##
####################


class DatabaseClient:
    """
    A client for connecting to MongoDB and initializing Beanie for document models.
    """

    def __init__(
        self,
        db_username: str,
        db_password: str,
        db_host: str,
        db_port: int,
        db_name: str
    ) -> None:
        """
        Initializes the DatabaseClient with MongoDB connection details.

        Args:
            db_username (str): The MongoDB username.
            db_password (str): The MongoDB password.
            db_host (str): The MongoDB host address.
            db_port (int): The MongoDB port.
            db_name (str): The name of the MongoDB database.
        """
        self.db_username = db_username
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name

        # Connect to MongoDB using Motor async client

        if not self.db_port:
            self.client = AsyncIOMotorClient(
                f"mongodb://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}"
            )
        else:
            self.client = AsyncIOMotorClient(
                f"mongodb+srv://{self.db_username}:{self.db_password}@{self.db_host}"
            )


    async def connect(self, document_models: List) -> None:
        """
        Connects to the MongoDB database and initializes Beanie for document models.

        args:
            document_models (List): A list of document models to initialize with Beanie.
        """

        await init_beanie(database=self.client[self.db_name], document_models=document_models)

    async def disconnect(self) -> None:
        """
        Disconnects from the MongoDB database.
        """
        self.client.close()
