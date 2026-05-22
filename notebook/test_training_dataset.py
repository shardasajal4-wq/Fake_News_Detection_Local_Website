from data.dataset_loader import load_training_dataset, split_dataset

fake_path = "../data/Fake.csv"
true_path = "../data/True.csv"

df = load_training_dataset(fake_path, true_path)

print("\nDataset Preview:\n")
print(df.head())

print("\nLabel distribution:")
print(df["label"].value_counts())

train_df, val_df, test_df = split_dataset(df)

print("\nTrain preview:\n")
print(train_df.head())