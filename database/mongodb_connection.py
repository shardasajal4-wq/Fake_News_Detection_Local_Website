from pymongo import MongoClient
import os

# =========================
# MONGODB CONNECTION
# =========================

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

# =========================
# DATABASE
# =========================
db = client["fake_news_detector"]

# =========================
# COLLECTIONS
# =========================
news_collection = db["news_articles"]
predictions_collection = db["predictions"]
archive_collection = db["news_archive"]