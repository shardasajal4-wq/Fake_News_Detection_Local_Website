import pandas as pd
from preprocessing.text_cleaner import clean_text
from sklearn.model_selection import train_test_split


def load_training_dataset(fake_path, true_path):

    # Load datasets
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    # Add labels
    fake_df["label"] = 0
    true_df["label"] = 1

    # Combine datasets
    df = pd.concat([fake_df, true_df], ignore_index=True)

    # Handle missing values
    df["title"] = df["title"].fillna("")
    df["text"] = df["text"].fillna("")

    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Combine title + text
    df["content"] = df["title"] + " " + df["text"]

    # Clean text
    df["content"] = df["content"].apply(clean_text)

    # Keep only needed columns
    df = df[["content", "label"]]

    print("Dataset prepared successfully")
    print("Total samples:", len(df))
    print("Label distribution:\n", df["label"].value_counts())

    return df


def split_dataset(df):

    # Train + temp split
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=42,
        stratify=df["label"]
    )

    # Validation + Test split
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=42,
        stratify=temp_df["label"]
    )

    # Reset index
    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    print("\nDataset Split:")
    print("Train:", len(train_df))
    print("Validation:", len(val_df))
    print("Test:", len(test_df))

    return train_df, val_df, test_df