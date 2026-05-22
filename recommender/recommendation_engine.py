from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.mongodb_connection import archive_collection


def get_recommendations(article_text, top_n=5):

    # ---------------------------
    # STEP 1: LOAD & FILTER DATA
    # ---------------------------
    articles = list(archive_collection.find({}, {"_id": 0}))

    if not articles:
        return []

    # 🔥 FILTER OUT FAKE NEWS
    filtered_articles = [
        article for article in articles
        if article.get("prediction") != "Fake"
    ]

    if not filtered_articles:
        return []

    texts = [article["cleaned_text"] for article in filtered_articles]

    # ---------------------------
    # STEP 2: ADD INPUT TEXT
    # ---------------------------
    article_text = article_text.lower()  # match preprocessing
    texts.append(article_text)

    # ---------------------------
    # STEP 3: TF-IDF
    # ---------------------------
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    # ---------------------------
    # STEP 4: SIMILARITY
    # ---------------------------
    similarity_scores = cosine_similarity(
        tfidf_matrix[-1], tfidf_matrix[:-1]
    )

    scores = similarity_scores.flatten()

    # ---------------------------
    # STEP 5: GET TOP MATCHES
    # ---------------------------
    top_indices = scores.argsort()[::-1][:top_n]

    recommendations = []

    for idx in top_indices:
        score = scores[idx]

        # OPTIONAL: MIN SIMILARITY THRESHOLD
        if score < 0.1:
            continue

        article = filtered_articles[int(idx)]

        recommendations.append({
            "title": article["title"],
            "source": article["source"],
            "url": article.get("url", ""),
            "prediction": article["prediction"],
            "confidence": article["confidence"],
            "similarity_score": round(float(score), 0)
        })

    return recommendations