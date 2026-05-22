from scraper.news_fetcher import fetch_news

api_key = "b352094e37ea425d9410133f87ab055c"

articles = fetch_news(api_key)

print("\nFetched Articles:\n")

for i, article in enumerate(articles[:5]):
    print(f"Article {i+1}")
    print("Title:", article["title"])
    print("Source:", article["source"])
    print()