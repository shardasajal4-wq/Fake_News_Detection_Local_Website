from fastapi import FastAPI, HTTPException
from backend.news_pipeline import run_pipeline
from models.model_interface import FakeNewsModel
from database.mongodb_connection import predictions_collection
from datetime import datetime, timezone
from recommender.recommendation_engine import get_recommendations
from utils.time_utils import convert_utc_to_ist
from preprocessing.text_cleaner import clean_text
from dotenv import load_dotenv
import os

app = FastAPI(title="Fake News Detection API")

# =========================
# LOAD MODEL
# =========================
model = FakeNewsModel()
model.load_model()

# =========================
# ENV VARIABLES
# =========================
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in environment variables")

# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return {"message": "Fake News Detection API Running"}


# =========================
# SIMPLE PREDICTION
# =========================
@app.post("/predict")
def predict_news(text: str):
    try:
        result = model.predict(text)

        return {
            #"prediction": result.get("prediction"),
            #"confidence": result.get("confidence"),
            "final": result.get("final")  # keeping your custom output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# CHECK NEWS (TITLE + CONTENT)
# =========================
@app.post("/check-news")
def check_news(title: str, content: str):
    try:
        # safer text joining
        text = " ".join(filter(None, [title, content]))

        result = model.predict(text)

        # ✅ extract from "final"
        final_result = result.get("final", {})

        prediction = final_result.get("prediction")
        confidence = final_result.get("confidence")

        # ✅ store in DB
        log_data = {
            "title": title,
            "content": content,
            "cleaned_text": result.get("cleaned_text"),
            "prediction": prediction,
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc)
        }

        predictions_collection.insert_one(log_data)

        # ✅ return correct response
        return convert_utc_to_ist({
            "prediction": prediction,
            "confidence": confidence
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# LATEST NEWS PIPELINE
# =========================
@app.get("/latest-news")
def latest_news(limit: int = 10):
    try:
        results = run_pipeline(NEWS_API_KEY)

        response = []

        for article in results[:limit]:
            response.append({
                "title": article.get("title"),
                "source": article.get("source"),
                "prediction": article.get("prediction"),
                "confidence": article.get("confidence"),
                "url": article.get("url", ""),
                "timestamp": datetime.now(timezone.utc)
            })

        return convert_utc_to_ist(response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# RECOMMENDATION SYSTEM
# =========================
@app.post("/recommend")
def recommend_news(title: str, content: str):
    try:
        text = " ".join(filter(None, [title, content]))

        # clean before recommendation
        cleaned_text = clean_text(text)

        recommendations = get_recommendations(cleaned_text)

        return convert_utc_to_ist({
            "recommendations": recommendations
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))