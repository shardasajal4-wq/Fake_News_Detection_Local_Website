import os
import time
import requests
import pandas as pd
from datetime import datetime

# =========================
# IMPORT YOUR MODEL
# =========================
from models.model_interface import FakeNewsModel

# =========================
# NEWS API CONFIG
# =========================
API_KEY = "b352094e37ea425d9410133f87ab055c"

CATEGORIES = [
    "politics",
    "technology",
    "business",
    "sports",
    "health",
    "science",
    "entertainment"
]

ARTICLES_PER_CATEGORY = 30

# =========================
# OUTPUT PATH
# =========================
RESULTS_DIR = "research_analysis/results"

os.makedirs(RESULTS_DIR, exist_ok=True)

OUTPUT_CSV = os.path.join(
    RESULTS_DIR,
    "live_news_results.csv"
)

# =========================
# LOAD MODEL
# =========================
print("\nLoading DistilBERT model...\n")

model = FakeNewsModel()
model.load_model()

print("Model loaded successfully.\n")

# =========================
# FETCH NEWS FUNCTION
# =========================
def fetch_news_by_category(category):

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={category}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize={ARTICLES_PER_CATEGORY}&"
        f"apiKey={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching {category} news")
        return []

    data = response.json()

    return data.get("articles", [])

# =========================
# MAIN EVALUATION LOOP
# =========================
results = []

article_counter = 1

for category in CATEGORIES:

    print(f"\nFetching {category} news...\n")

    articles = fetch_news_by_category(category)

    print(f"Fetched {len(articles)} articles.\n")

    for article in articles:

        try:

            title = article.get("title", "")
            description = article.get("description", "")
            content = article.get("content", "")

            source = ""

            if article.get("source"):
                source = article["source"].get("name", "")

            # Combine article text
            full_text = f"{title}. {description}. {content}"

            # Skip short articles
            if len(full_text.split()) < 20:
                continue

            # =========================
            # MEASURE INFERENCE TIME
            # =========================
            start_time = time.time()

            prediction_result = model.predict(full_text)

            end_time = time.time()

            inference_time = end_time - start_time

            # =========================
            # EXTRACT RESULTS
            # =========================
            argmax_prediction = prediction_result["argmax"]["prediction"]
            argmax_confidence = prediction_result["argmax"]["confidence"]

            threshold_prediction = prediction_result["threshold"]["prediction"]
            threshold_confidence = prediction_result["threshold"]["confidence"]

            difference_prediction = prediction_result["difference"]["prediction"]
            difference_confidence = prediction_result["difference"]["confidence"]

            # Article length
            article_length = len(full_text.split())

            # Timestamp
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # =========================
            # STORE RESULT
            # =========================
            results.append({
                "article_id": article_counter,
                "category": category,
                "source": source,
                "title": title,

                "argmax_prediction": argmax_prediction,
                "argmax_confidence": argmax_confidence,

                "threshold_prediction": threshold_prediction,
                "threshold_confidence": threshold_confidence,

                "difference_prediction": difference_prediction,
                "difference_confidence": difference_confidence,

                "inference_time": inference_time,
                "article_length": article_length,
                "timestamp": timestamp
            })

            print(
                f"[{article_counter}] "
                f"{category.upper()} | "
                f"{argmax_prediction} | "
                f"Confidence: {argmax_confidence:.4f}"
            )

            article_counter += 1

        except Exception as e:

            print(f"Error processing article: {e}")

# =========================
# SAVE CSV
# =========================
df = pd.DataFrame(results)

df.to_csv(OUTPUT_CSV, index=False)

print("\n===================================")
print("LIVE NEWS EVALUATION COMPLETE")
print("===================================")

print(f"\nResults saved to:\n{OUTPUT_CSV}")

print(f"\nTotal articles processed: {len(df)}")