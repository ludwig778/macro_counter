from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError


class MongoAdapter:
    def __init__(self, config):
        self.config = config

        self.client = MongoClient(
            host=self.uri, serverSelectionTimeoutMS=self.config.timeout_ms
        )
        self.database: Database = self.client[self.config.database]

    @property
    def connected(self) -> bool:
        try:
            self.client.server_info()
            return True
        except ServerSelectionTimeoutError:
            return False

    def get_collection(self, name: str) -> Collection:
        return self.database[name]

    @property
    def uri(self) -> str:
        if self.config.srv_mode:
            raw_uri = "mongodb+srv://{username}:{password}@{host}/{database}?retryWrites=true&w=majority"
        else:
            raw_uri = "mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"

        return raw_uri.format(**self.config.dict())
