from preprocessing.text_cleaner import clean_text

sample_text = "Breaking News!!! Visit https://abc.com for more details about the shocking event."

cleaned = clean_text(sample_text)

print("Original Text:")
print(sample_text)

print("\nCleaned Text:")
print(cleaned)