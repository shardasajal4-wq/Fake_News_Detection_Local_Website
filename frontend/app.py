import streamlit as st
import requests
import os
import base64
from PIL import Image

# =========================
# CONFIG
# =========================
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Fake News Detector", layout="wide")

# =========================
# PATHS
# =========================
base_dir = os.path.dirname(__file__)
assets = os.path.join(base_dir, "assets")

# =========================
# IMAGE LOADER (BASE64)
# =========================
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Load images
logo = Image.open(os.path.join(assets, "logo.jpeg"))
hero_path = os.path.join(assets, "hero.jpeg")

ai_img = get_base64_image(os.path.join(assets, "ai.jpeg"))
news_img = get_base64_image(os.path.join(assets, "news.jpeg"))
rec_img = get_base64_image(os.path.join(assets, "recommend.jpeg"))

# =========================
# CSS (FULLY FIXED)
# =========================
st.markdown("""
<style>

/* REMOVE STREAMLIT BLOCK BACKGROUNDS */
[data-testid="stVerticalBlock"] > div {
    background: transparent !important;
    box-shadow: none !important;
}

/* HEADER */
.title {
    text-align: center;
    font-size: 46px;
    font-weight: 700;
    margin-top: 20px;
}

/* HERO IMAGE */
.hero img {
    width: 100%;
    height: 320px;
    object-fit: cover;
    border-radius: 15px;
}

/* CARD */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 8px 18px rgba(0,0,0,0.08);
    transition: 0.3s;
}

/* HOVER EFFECT */
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 12px 24px rgba(0,0,0,0.12);
}

/* CARD IMAGE */
.card img {
    width: 130px;
    border-radius: 10px;
}

/* TITLE */
.card-title {
    font-size: 20px;
    font-weight: bold;
    margin-top: 12px;
}

/* TEXT */
.card-text {
    font-size: 14px;
    margin-top: 8px;
    color: #555;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1, col2, col3 = st.columns([1,5,1])

with col1:
    st.image(logo, width=130)

with col2:
    st.markdown("<div class='title'>Fake News Detection System</div>", unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown("<div class='hero'>", unsafe_allow_html=True)
st.image(hero_path, width='stretch')
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs(
    ["Home", "Check News", "Latest News", "Recommendations"]
)

# =========================
# HOME
# =========================
with tab1:

    st.markdown(
        "<h2 style='text-align:center;'>Check whether news is real or fake using intelligent AI analysis.</h2>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="card">
            <img src="data:image/jpeg;base64,{ai_img}">
            <div class="card-title">AI Detection</div>
            <div class="card-text">Uses advanced NLP model</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <img src="data:image/jpeg;base64,{news_img}">
            <div class="card-title">Live News</div>
            <div class="card-text">Analyzes latest articles</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <img src="data:image/jpeg;base64,{rec_img}">
            <div class="card-title">Smart Recommendation</div>
            <div class="card-text">Suggests similar news</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# CHECK NEWS
# =========================
with tab2:

    st.header("Check News")

    # ✅ Clear function (callback)
    def clear_inputs():
        st.session_state.title_input = ""
        st.session_state.content_input = ""
        st.session_state.result = None

    # Initialize session state
    if "title_input" not in st.session_state:
        st.session_state.title_input = ""

    if "content_input" not in st.session_state:
        st.session_state.content_input = ""

    if "result" not in st.session_state:
        st.session_state.result = None

    # Inputs
    title = st.text_input("Title", key="title_input")
    content = st.text_area("Content", key="content_input")

    # Buttons row
    col1, col2 = st.columns(2)

    with col1:
        # ✅ Disable button if inputs are empty
        analyze_clicked = st.button(
            "Analyze",
            disabled=not title or not content
        )

    with col2:
        st.button("Clear", on_click=clear_inputs)

    # Analyze logic
    if analyze_clicked:

        # Save for recommendation
        st.session_state["last_title"] = title
        st.session_state["last_content"] = content

        try:
            with st.spinner("Analyzing news..."):
                res = requests.post(
                    f"{API_URL}/check-news",
                    params={"title": title, "content": content}
                ).json()

            st.session_state.result = res

        except Exception as e:
            st.error(f"Error: {e}")

    # Show result
    if st.session_state.result:

        pred = st.session_state.result.get("prediction")
        conf = st.session_state.result.get("confidence")

        if pred == "Real":
            st.success(f"Real ({conf:.2f})")
        elif pred == "Fake":
            st.error(f"Fake ({conf:.2f})")
        else:
            st.warning("Uncertain")

# =========================
# LATEST NEWS
# =========================
with tab3:

    st.header("Latest News Feed")

    # Initialize session state
    if "news_data" not in st.session_state:
        st.session_state.news_data = []

    if "news_limit" not in st.session_state:
        st.session_state.news_limit = 10

    # Fetch button
    if st.button("Fetch News"):
        try:
            data = requests.get(
                f"{API_URL}/latest-news?limit=50"
            ).json()

            st.session_state.news_data = data
            st.session_state.news_limit = 10

        except Exception as e:
            st.error(f"Error fetching news: {e}")

    # Show news
    news = st.session_state.news_data[:st.session_state.news_limit]

    if news:

        # 2-column layout
        col1, col2 = st.columns(2)

        for i, a in enumerate(news):

            col = col1 if i % 2 == 0 else col2

            with col:
                with st.container():

                    # =========================
                    # TITLE
                    # =========================
                    st.subheader(a.get("title", "No Title"))

                    # =========================
                    # SOURCE + TIME
                    # =========================
                    st.caption(
                        f"{a.get('source', 'Unknown')} • {a.get('timestamp', '')}"
                    )

                    # =========================
                    # READ FULL ARTICLE BUTTON
                    # =========================
                    article_url = a.get("url", "")

                    if article_url:
                        st.link_button(
                            "🔗 Read Full Article",
                            article_url,
                            use_container_width=True
                        )

                    prediction = a.get("prediction")
                    confidence = float(a.get("confidence", 0))

                    # =========================
                    # PREDICTION STYLING
                    # =========================
                    if prediction == "Real":
                        st.success(f"Prediction: {prediction}")

                    elif prediction == "Fake":
                        st.error(f"Prediction: {prediction}")

                    else:
                        st.warning(f"Prediction: {prediction}")

                    # =========================
                    # CONFIDENCE STYLING
                    # =========================
                    if confidence > 0.8:
                        st.success(
                            f"Confidence: {confidence * 100:.1f}%"
                        )

                    elif confidence > 0.6:
                        st.warning(
                            f"Confidence: {confidence * 100:.1f}%"
                        )

                    else:
                        st.error(
                            f"Confidence: {confidence * 100:.1f}%"
                        )

                    # =========================
                    # PROGRESS BAR
                    # =========================
                    st.progress(confidence)

                    st.markdown("---")

        # =========================
        # LOAD MORE BUTTON
        # =========================
        if st.session_state.news_limit < len(st.session_state.news_data):

            if st.button("Load More"):

                st.session_state.news_limit += 10
                st.rerun()

# =========================
# RECOMMENDATIONS
# =========================
with tab4:

    st.header("Recommended News")

    if st.button("Get Recommendations"):

        # Check if user has analyzed news first
        if "last_title" not in st.session_state or "last_content" not in st.session_state:
            st.warning("⚠️ Please analyze a news article first.")

        else:
            try:
                res = requests.post(
                    f"{API_URL}/recommend",
                    params={
                        "title": st.session_state["last_title"],
                        "content": st.session_state["last_content"]
                    }
                ).json()

                recommendations = res.get("recommendations", [])

                if not recommendations:
                    st.warning("No recommendations found.")

                else:
                    for r in recommendations:

                        # 📰 Title
                        st.subheader(r["title"])

                        # 🏷 Source
                        st.caption(f"Source: {r['source']}")

                        # URL
                        # 🔗 Read Full Article
                        article_url = r.get("url", "")

                        if article_url:
                            st.link_button(
                                "🔗 Read Full Article",
                                article_url,
                                use_container_width=True
                            )

                        # 🎯 Prediction (color coded)
                        if r["prediction"] == "Real":
                            st.success(f"Prediction: {r['prediction']}")
                        else:
                            st.error(f"Prediction: {r['prediction']}")

                        # 📊 Confidence Display
                        confidence = float(r.get("confidence", 0))

                        if confidence > 0.8:
                            st.success(f"High Confidence: {confidence * 100:.2f}%")
                        elif confidence > 0.6:
                            st.warning(f"Moderate Confidence: {confidence * 100:.2f}%")
                        else:
                            st.error(f"Low Confidence: {confidence * 100:.2f}%")

                        # 📈 Progress Bar
                        st.progress(confidence)

                        st.markdown("---")

            except Exception as e:
                st.error(f"Error: {e}")