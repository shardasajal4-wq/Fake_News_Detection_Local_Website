# 📰 Fake News Detection & News Recommendation System using DistilBERT

## 📌 Overview

This project is an AI-powered **Real-Time Fake News Detection and News Recommendation System** that uses a fine-tuned **DistilBERT Transformer model** to classify news articles as **Real**, **Fake**, or **Uncertain** with confidence analysis.

The system automatically fetches live news articles using **NewsAPI**, preprocesses and analyzes them using a hybrid decision engine, stores prediction results in **MongoDB**, and recommends related news articles using **TF-IDF cosine similarity**.

The project also includes:

* ⚡ FastAPI backend APIs
* 🖥️ Interactive Streamlit frontend
* 🧠 Intelligent caching and archiving system
* 📊 Confidence-based prediction analysis
* 📌 Smart recommendation engine
* 🔗 Read Full Article support

---

# 🚀 Key Features

## 🔍 Real-Time News Analysis

* Fetches latest live news using NewsAPI
* Cleans and preprocesses articles automatically
* Performs instant fake news detection
* Displays confidence scores for predictions

---

## 🤖 Transformer-Based Detection

* Fine-tuned DistilBERT model for text classification
* Context-aware NLP prediction pipeline
* Semantic understanding of news articles
* Hybrid decision logic for better reliability

---

## 🧠 Hybrid Prediction Logic

The prediction system combines:

* Argmax Classification
* Confidence Thresholding
* Probability Difference Analysis

to generate more robust and reliable predictions.

---

## 📊 Confidence Scoring

Every prediction includes:

* Prediction label
* Confidence percentage
* Prediction visualization

---

## 🗂️ MongoDB Integration

Stores:

* Latest fetched news
* User prediction history
* Archived news articles
* Cached API responses

---

## ⚡ Smart Caching System

* Reduces repeated NewsAPI requests
* Improves response speed
* Automatically refreshes stale cache data

---

## 📌 News Recommendation Engine

* Suggests similar articles
* Uses TF-IDF Vectorization
* Uses Cosine Similarity matching
* Supports article link redirection

---

## 🔗 Full Article Access

Users can directly open and read the complete news article from:

* Latest News section
* Recommendations section

---

## 🌐 REST API Support

Built using FastAPI with fully functional REST APIs.

---

## 🖥️ Interactive Frontend Dashboard

Frontend supports:

* Manual news verification
* Live news browsing
* Prediction visualization
* Recommendation system
* Full article access

---

# 🏗️ Tech Stack

| Category              | Technologies                      |
| --------------------- | --------------------------------- |
| Backend               | FastAPI                           |
| Frontend              | Streamlit                         |
| Machine Learning      | DistilBERT, Transformers, PyTorch |
| NLP                   | NLTK, BeautifulSoup               |
| Database              | MongoDB                           |
| Recommendation System | TF-IDF, Cosine Similarity         |
| APIs                  | NewsAPI                           |
| Utilities             | Requests, Scikit-learn, Pandas    |

---

# 📂 Project Structure

```bash
Fake_News_Detection_Local_Website/
│
├── backend/
│   ├── main.py
│   └── news_pipeline.py
│
├── database/
│   └── mongodb_connection.py
│
├── data/
│   └── dataset_loader.py
│
├── frontend/
│   ├── app.py
│   └── assets/
│
├── models/
│   └── model_interface.py
│
├── preprocessing/
│   └── text_cleaner.py
│
├── recommender/
│   └── recommendation_engine.py
│
├── scraper/
│   └── news_fetcher.py
│
├── utils/
│   ├── model_comparison.py
│   └── time_utils.py
│
├── notebook/
│
├── research_analysis/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ System Workflow

```text
NewsAPI
   ↓
Fetch News
   ↓
Text Cleaning & Preprocessing
   ↓
DistilBERT Prediction
   ↓
Hybrid Decision Logic
   ↓
MongoDB Storage & Cache
   ↓
Recommendation Engine
   ↓
Frontend/API Response
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root directory:

```env
NEWS_API_KEY=your_newsapi_key
MONGO_URI=mongodb://localhost:27017
```

---

# ▶️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/shardasajal4-wq/Fake_News_Detection_Local_Website.git

cd Fake_News_Detection_Local_Website
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Start MongoDB

Make sure MongoDB is running locally.

```bash
mongod
```

---

## 5️⃣ Run Backend Server

```bash
uvicorn backend.main:app --reload
```

Backend API runs at:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 6️⃣ Run Frontend

```bash
streamlit run frontend/app.py
```

Frontend runs at:

```text
http://localhost:8501
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
* Returns top matching related articles

---

# 🗃️ MongoDB Collections

| Collection      | Purpose                  |
| --------------- | ------------------------ |
| `news_articles` | Cached latest news       |
| `predictions`   | User prediction history  |
| `news_archive`  | Archived historical news |

---

# 🧪 Testing Modules

The project includes testing scripts for:

* Dataset loading
* MongoDB connection
* News fetching
* News pipeline
* Model prediction

---

# 🔮 Future Improvements

* 🌍 Multi-language fake news detection
* 📱 Mobile application support
* ☁️ Cloud deployment
* 📈 Advanced analytics dashboard
* 🧠 Improved recommendation algorithms
* 🔔 Real-time fake news alerts
* 📰 Source credibility analysis

---

# 📌 Important Note

Large datasets and trained model files are excluded from the GitHub repository due to GitHub file size limitations.

---

# 👨‍💻 Author

**Sajal Sharda**
B.Tech CSE (Data Science)
The NorthCap University

---

# 📜 License

This project is developed for academic and research purposes only.
