import re
import nltk
from nltk.corpus import stopwords

# download stopwords (only runs first time)
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def clean_text(text):

    # convert to lowercase
    text = text.lower()

    # remove URLs
    text = re.sub(r"http\S+", "", text)

    # remove special characters
    text = re.sub(r"[^a-zA-Z ]", "", text)

    # split into words
    words = text.split()

    # remove stopwords
    words = [word for word in words if word not in stop_words]

    # join back to sentence
    cleaned_text = " ".join(words)

    return cleaned_text