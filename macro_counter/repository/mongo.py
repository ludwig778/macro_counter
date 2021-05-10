from pymongo import MongoClient

from macro_counter.settings import MONGO_CONFIG, MONGO_DATABASE, TEST

mongo_client = MongoClient(**MONGO_CONFIG)
mongo_database = getattr(mongo_client, MONGO_DATABASE)

ingredient_collection = getattr(
    mongo_database,
    ("TEST_" if TEST else "") + "ingredient"
)
