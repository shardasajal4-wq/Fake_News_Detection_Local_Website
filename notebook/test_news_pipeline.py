from backend.news_pipeline import run_pipeline

api_key = "b352094e37ea425d9410133f87ab055c"

results = run_pipeline(api_key)

print("\nNews Prediction Results:\n")

for i, article in enumerate(results[:5]):

    print(f"Article {i+1}")
    print("Title:", article["title"])
    print("Source:", article["source"])
    print("Prediction:", article["prediction"])
    print("Confidence:", article["confidence"])
    print()