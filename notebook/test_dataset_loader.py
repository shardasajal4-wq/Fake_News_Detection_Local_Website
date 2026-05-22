from data.dataset_loader import load_dataset, preprocess_dataset

# path to dataset
file_path = "../data/sample_fake_news.csv"

# load dataset
df = load_dataset(file_path)

# clean dataset
df = preprocess_dataset(df, "text")

print("\nCleaned Dataset:\n")
print(df.head())