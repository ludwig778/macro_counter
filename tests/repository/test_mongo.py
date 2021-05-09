from macro_counter.repository.mongo import mongo_client, mongo_database


def test_mongo_methods():
    assert mongo_client.connected

    test_collection = mongo_database.test_collection
    test_collection.drop()

    assert test_collection.insert_one({"lmao": "test"})
    assert test_collection.insert_one({"lmao": "test2"})
    assert test_collection.estimated_document_count() == 2

    assert test_collection.insert_one({"lmao": "test2"})
    assert len(list(test_collection.find({"lmao": {"$regex": "test2"}}))) == 2
    assert len(list(test_collection.find({"lmao": {"$regex": "test.*"}}))) == 3
    assert len(list(test_collection.find())) == 3

    assert test_collection.delete_one({"lmao": "test"})
    assert test_collection.delete_many({"lmao": "test2"})

    assert len(list(test_collection.find())) == 0

    test_collection.drop()
