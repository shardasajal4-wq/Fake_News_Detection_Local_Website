from database.mongodb_connection import news_collection

test_data = {
    "title": "Test News",
    "content": "This is a test document",
    "source": "System"
}

news_collection.insert_one(test_data)

print("Test document inserted into MongoDB")