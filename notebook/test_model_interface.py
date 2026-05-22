from models.model_interface import FakeNewsModel

# Create model object
model = FakeNewsModel()

# Load model
model.load_model()

# Example news article
sample_news = "Breaking news! Government announces a shocking new policy today."

# Run prediction
result = model.predict(sample_news)

print("\nPrediction Result:")
print(result)