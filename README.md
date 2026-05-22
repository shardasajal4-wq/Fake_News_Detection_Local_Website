# 📰 Fake News Detection & News Recommendation System using DistilBERT

## 📌 Overview

This project is an AI-powered **Real-Time Fake News Detection and Recommendation System** that uses a fine-tuned **DistilBERT Transformer model** to classify news articles as **Real**, **Fake**, or **Uncertain** with confidence analysis.

The system automatically fetches live news articles using **NewsAPI**, processes and classifies them using a hybrid decision engine, stores results in **MongoDB**, and recommends similar articles using **TF-IDF cosine similarity**.

The project also includes:

* ⚡ FastAPI backend APIs
* 🖥️ Interactive frontend interface
* 🧠 Intelligent caching and archiving system
* 📊 Confidence-based prediction logic
* 📌 Personalized news recommendation module

---

# 🚀 Key Features

## 🔍 Real-Time News Analysis

* Fetches latest live news using NewsAPI
* Cleans and preprocesses articles automatically
* Performs instant fake news detection

## 🤖 Transformer-Based Detection

* Fine-tuned DistilBERT model for text classification
* Context-aware NLP prediction pipeline
* High accuracy semantic understanding

## 🧠 Hybrid Prediction Logic

The system combines:

* Argmax Classification
* Confidence Thresholding
* Probability Difference Analysis

to generate more reliable predictions.

## 📊 Confidence Scoring

Every prediction includes:

* Prediction label
* Confidence percentage
* Decision analysis

## 🗂️ MongoDB Integration

Stores:

* Live fetched news
* Prediction history
* Archived news articles
* Cached API responses

## ⚡ Smart Caching System

* Reduces repeated API calls
* Uses cached news for faster response
* Automatically refreshes stale data

## 📌 News Recommendation Engine

* Recommends similar articles
* Uses TF-IDF Vectorization
* Uses Cosine Similarity matching

## 🌐 REST API Support

Built using FastAPI with fully functional APIs.

## 🖥️ Frontend Dashboard

Interactive frontend for:

* News checking
* Live news browsing
* Recommendation viewing
* Prediction visualization

---

# 🏗️ Tech Stack

| Category              | Technologies                      |
| --------------------- | --------------------------------- |
| Backend               | FastAPI                           |
| Frontend              | Streamlit / PyQt (Project UI)     |
| Machine Learning      | DistilBERT, Transformers, PyTorch |
| NLP                   | NLTK, BeautifulSoup               |
| Database              | MongoDB                           |
| Recommendation System | TF-IDF, Cosine Similarity         |
| APIs                  | NewsAPI                           |
| Utilities             | Requests, Scikit-learn, Pandas    |

---

# 📂 Updated Project Structure

```bash
fake-news-detection-system/
│
├── backend/
│   ├── main.py
│   └── news_pipeline.py
│
├── models/
│   ├── model_interface.py
│   ├── config.json
│   ├── tokenizer.json
│   └── tokenizer_config.json
│
├── scraper/
│   └── news_fetcher.py
│
├── preprocessing/
│   └── text_cleaner.py
│
├── recommender/
│   └── recommendation_engine.py
│
├── database/
│   └── mongodb_connection.py
│
├── utils/
│   └── time_utils.py
│
├── tests/
│   ├── test_model_interface.py
│   ├── test_news_pipeline.py
│   ├── test_dataset_loader.py
│   ├── test_news_fetcher.py
│   └── test_mongodb.py
│
├── data/
│   ├── Fake.csv
│   └── True.csv
│
├── frontend/
│   └── app.py
│
├── notebook/
│
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ System Workflow

```text
NewsAPI → Fetch News → Clean & Preprocess →
DistilBERT Prediction → Hybrid Decision Engine →
MongoDB Storage → Recommendation Engine →
Frontend/API Response
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
NEWS_API_KEY=your_newsapi_key
MONGO_URI=mongodb://localhost:27017
```

---

# ▶️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/fake-news-detection-system.git
cd fake-news-detection-system
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Start MongoDB

Make sure MongoDB service is running locally.

```bash
mongod
```

---

## 5️⃣ Run Backend Server

```bash
uvicorn backend.main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

---

## 6️⃣ Run Frontend

```bash
cd frontend
streamlit run frontend/app.py
```

---

# 📡 API Endpoints

| Endpoint       | Method | Description                  |
| -------------- | ------ | ---------------------------- |
| `/`            | GET    | API status check             |
| `/predict`     | POST   | Predict fake/real from text  |
| `/check-news`  | POST   | Analyze title + content      |
| `/latest-news` | GET    | Fetch and classify live news |
| `/recommend`   | POST   | Recommend similar articles   |

---

# 📊 Example API Response

```json
{
    "prediction": "Real",
    "confidence": 0.92
}
```

---

# 🧠 Hybrid Decision System

The prediction engine does not rely only on maximum probability.

It combines:

* Highest probability class
* Confidence threshold validation
* Probability difference comparison

This improves robustness and reduces uncertain predictions.

---

# 📌 Recommendation Engine

The recommendation module:

* Stores archived news articles
* Converts text into TF-IDF vectors
* Computes cosine similarity
* Returns top matching articles

---

# 🗃️ MongoDB Collections

| Collection      | Purpose                  |
| --------------- | ------------------------ |
| `news_articles` | Cached latest news       |
| `predictions`   | User prediction history  |
| `news_archive`  | Archived historical news |

---

# 🧪 Testing Modules

The project includes multiple testing files for:

* Dataset loading
* MongoDB connection
* News fetching
* Pipeline execution
* Model prediction

---

# 🔮 Future Improvements

* 🌍 Multi-language fake news detection
* 📱 Mobile application support
* ☁️ Cloud deployment
* 📈 Advanced analytics dashboard
* 🧠 Improved recommendation algorithms
* 🔔 Real-time alert system
* 📰 Source credibility analysis

---

# 👨‍💻 Author

**Sajal Sharda**
B.Tech CSE (Data Science)
The NorthCap University

---

# 📜 License

This project is developed for academic and research purposes.
