from scraper.news_fetcher import fetch_news
from models.model_interface import FakeNewsModel
from database.mongodb_connection import news_collection, archive_collection
from datetime import datetime, timedelta, timezone
from preprocessing.text_cleaner import clean_text


def run_pipeline(api_key):

    # =========================
    # STEP 0: CHECK CACHE
    # =========================
    latest_article = news_collection.find_one(
        sort=[("timestamp", -1)]
    )

    if latest_article:

        cache_time = latest_article["timestamp"].replace(
            tzinfo=timezone.utc
        )

        current_time = datetime.now(timezone.utc)

        # Cache valid for 2 hours
        if current_time - cache_time < timedelta(minutes=1):#hours=2):

            cached_news = list(
                news_collection.find({}, {"_id": 0}).limit(50)
            )

            return cached_news

    # =========================
    # STEP 1: FETCH NEWS
    # =========================
    articles = fetch_news(api_key)

    # =========================
    # STEP 2: ARCHIVE OLD NEWS
    # =========================
    old_news = list(news_collection.find({}))

    for article in old_news:

        existing_archive = archive_collection.find_one({
            "title": article.get("title"),
            "source": article.get("source")
        })

        if not existing_archive:
            archive_collection.insert_one(article)

    # =========================
    # STEP 3: CLEAN OLD ARCHIVE
    # =========================
    seven_days_ago = (
        datetime.now(timezone.utc) - timedelta(days=7)
    )

    archive_collection.delete_many({
        "timestamp": {"$lt": seven_days_ago}
    })

    # =========================
    # STEP 4: CLEAR CACHE
    # =========================
    news_collection.delete_many({})

    # =========================
    # STEP 5: LOAD MODEL
    # =========================
    model = FakeNewsModel()
    model.load_model()

    results = []

    # =========================
    # STEP 6: PROCESS ARTICLES
    # =========================
    for article in articles:

        title = article.get("title", "")
        content = article.get("content", "")
        source = article.get("source", "")
        article_url = article.get("url", "")

        # =========================
        # SAFE TEXT COMBINATION
        # =========================
        text = " ".join(
            filter(None, [title, content])
        )

        # =========================
        # RUN PREDICTION
        # =========================
        prediction = model.predict(text)

        # =========================
        # CLEAN TEXT FOR RECOMMENDER
        # =========================
        cleaned_text = clean_text(text)

        # =========================
        # FINAL RESULT OBJECT
        # =========================
        result = {
            "title": title,
            "content": content,
            "cleaned_text": cleaned_text,
            "source": source,
            "url": article_url,
            "prediction": prediction.get(
                "final", {}
            ).get("prediction"),

            "confidence": prediction.get(
                "final", {}
            ).get("confidence"),

            "timestamp": datetime.now(timezone.utc)
        }

        # =========================
        # PREVENT DUPLICATES
        # =========================
        existing_news = news_collection.find_one({
            "title": title,
            "source": source
        })

        if not existing_news:

            news_collection.insert_one(result)
            results.append(result)

    return results