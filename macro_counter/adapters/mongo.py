from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class MongoAdapter:
    def __init__(self, config):
        self.connect(config)

    def connect(self, config):
        self._client = MongoClient(
            self.format_uri(config), serverSelectionTimeoutMS=config.timeout_ms
        )
        self.database = getattr(self._client, config.database)

    @property
    def connected(self):
        try:
            self._client.server_info()
            return True
        except ServerSelectionTimeoutError:
            return False

    def get_collection(self, collection_name: str):
        return getattr(self.database, collection_name)

    def format_uri(self, config):
        if config.srv_mode:
            uri = "mongodb+srv://{username}:{password}@{host}/{database}?retryWrites=true&w=majority"
        else:
            uri = "mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"

        return uri.format(**config.dict())
