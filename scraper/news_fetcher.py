import requests
import re
from bs4 import BeautifulSoup


# =========================
# TEXT CLEANING FUNCTIONS
# =========================

def remove_html_tags(text):
    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text()

    return cleaned.replace("\n", " ").strip()


def remove_newsapi_truncation(text):
    if not text:
        return ""

    return re.sub(r"\[\+\d+\schars]", "", text).strip()


def remove_ellipsis_truncation(text):
    if not text:
        return ""

    return re.sub(r"\.\.\.$", "", text).strip()


def normalize_text(text):
    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


# =========================
# FILTER IRRELEVANT NEWS
# =========================

def is_valid_news(text):

    text = text.lower()

    reject_patterns = [
        "top 10",
        "top 50",
        "ranked",
        "follow us",
        "subscribe",
        "globe newswire"
    ]

    return not any(pattern in text for pattern in reject_patterns)


# =========================
# FETCH NEWS FUNCTION
# =========================

def fetch_news(api_key):

    url = (
        "https://newsapi.org/v2/everything"
        "?q=india&language=en&pageSize=50&sortBy=publishedAt"
        f"&apiKey={api_key}"
    )

    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

    except requests.exceptions.RequestException:
        return []

    articles = []

    for article in data.get("articles", []):

        title = article.get("title") or ""
        description = article.get("description") or ""
        content = article.get("content") or ""

        # =========================
        # FALLBACK IF CONTENT MISSING
        # =========================

        if not content:
            content = description

        # =========================
        # CLEANING
        # =========================

        title = normalize_text(
            remove_ellipsis_truncation(
                remove_newsapi_truncation(
                    remove_html_tags(title)
                )
            )
        )

        description = normalize_text(
            remove_ellipsis_truncation(
                remove_newsapi_truncation(
                    remove_html_tags(description)
                )
            )
        )

        content = normalize_text(
            remove_ellipsis_truncation(
                remove_newsapi_truncation(
                    remove_html_tags(content)
                )
            )
        )

        # =========================
        # SMART TEXT SELECTION
        # =========================

        if content and len(content) > 100:
            final_text = content

        elif description:
            final_text = description

        else:
            final_text = title

        # =========================
        # FILTER IRRELEVANT NEWS
        # =========================

        if not final_text or not is_valid_news(final_text):
            continue

        # =========================
        # SOURCE
        # =========================

        source = ""

        if article.get("source"):
            source = article["source"].get("name", "")

        # =========================
        # ARTICLE URL
        # =========================

        article_url = article.get("url", "")

        # =========================
        # FINAL OBJECT
        # =========================

        news = {
            "title": title,
            "content": final_text,
            "source": source,
            "url": article_url
        }

        articles.append(news)

    return articles