import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LOAD CSV
# =========================
CSV_PATH = "research_analysis/results/live_news_results.csv"

df = pd.read_csv(CSV_PATH)

# =========================
# OUTPUT FOLDER
# =========================
GRAPH_DIR = "research_analysis/graphs"

os.makedirs(GRAPH_DIR, exist_ok=True)

# =========================
# GLOBAL STYLE
# =========================
sns.set_theme(style="whitegrid")

plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300

plt.rcParams["font.size"] = 13
plt.rcParams["axes.titlesize"] = 18
plt.rcParams["axes.labelsize"] = 14

# =========================================================
# GRAPH 1
# CONFIDENCE TREND ACROSS ARTICLES
# =========================================================
plt.figure(figsize=(14, 6))

plt.plot(
    df["article_id"],
    df["argmax_confidence"],
    linewidth=2
)

plt.axhline(
    y=0.5,
    linestyle="--",
    linewidth=1.5,
    label="Minimum Confidence Threshold"
)

plt.axhline(
    y=0.7,
    linestyle=":",
    linewidth=1.5,
    label="High Confidence Region"
)

plt.title(
    "Confidence Stability Across Live News Articles"
)

plt.xlabel("Article ID")
plt.ylabel("Confidence Score")

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "confidence_trend.png"
    )
)

plt.close()

# =========================================================
# GRAPH 2
# REAL VS FAKE CONFIDENCE COMPARISON
# =========================================================
plt.figure(figsize=(10, 6))

sns.boxplot(
    x=df["argmax_prediction"],
    y=df["argmax_confidence"]
)

plt.title(
    "Confidence Comparison Between Real and Fake Predictions"
)

plt.xlabel("Prediction")
plt.ylabel("Confidence")

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "real_vs_fake_confidence.png"
    )
)

plt.close()

# =========================================================
# GRAPH 3
# SOURCE-WISE FAKE PREDICTION RATE
# =========================================================
top_sources = (
    df["source"]
    .value_counts()
    .head(10)
    .index
)

source_df = df[df["source"].isin(top_sources)]

fake_rates = []

for source in top_sources:

    source_articles = source_df[
        source_df["source"] == source
    ]

    fake_count = (
        source_articles["argmax_prediction"]
        == "Fake"
    ).sum()

    total = len(source_articles)

    fake_rate = (fake_count / total) * 100

    fake_rates.append(fake_rate)

plt.figure(figsize=(14, 6))

sns.barplot(
    x=top_sources,
    y=fake_rates
)

plt.title(
    "Fake Prediction Rate Across Major News Sources"
)

plt.xlabel("News Source")
plt.ylabel("Fake Prediction Rate (%)")

plt.xticks(rotation=45)

for i, v in enumerate(fake_rates):
    plt.text(i, v + 1, f"{v:.1f}%", ha='center')

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "source_fake_rate.png"
    )
)

plt.close()

# =========================================================
# GRAPH 4
# CATEGORY-WISE INFERENCE TIME
# =========================================================
plt.figure(figsize=(12, 6))

sns.boxplot(
    x=df["category"],
    y=df["inference_time"]
)

plt.title(
    "Inference Time Distribution Across Categories"
)

plt.xlabel("Category")
plt.ylabel("Inference Time (seconds)")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "category_inference_time.png"
    )
)

plt.close()

# =========================================================
# GRAPH 5
# RADAR CHART
# =========================================================
categories = [
    "Avg Confidence",
    "Prediction Balance",
    "Inference Speed",
    "Category Stability",
    "Confidence Stability"
]

# =========================
# NORMALIZED METRICS
# =========================
avg_conf = df["argmax_confidence"].mean()

real_count = (
    df["argmax_prediction"] == "Real"
).sum()

fake_count = (
    df["argmax_prediction"] == "Fake"
).sum()

prediction_balance = (
    min(real_count, fake_count)
    / max(real_count, fake_count)
)

avg_time = df["inference_time"].mean()

speed_score = 1 - min(avg_time / 0.1, 1)

category_std = (
    df.groupby("category")["argmax_confidence"]
    .mean()
    .std()
)

category_stability = 1 - category_std

confidence_std = (
    df["argmax_confidence"]
    .std()
)

confidence_stability = 1 - confidence_std

values = [
    avg_conf,
    prediction_balance,
    speed_score,
    category_stability,
    confidence_stability
]

values += values[:1]

angles = np.linspace(
    0,
    2 * np.pi,
    len(categories),
    endpoint=False
).tolist()

angles += angles[:1]

fig, ax = plt.subplots(
    figsize=(8, 8),
    subplot_kw=dict(polar=True)
)

ax.plot(
    angles,
    values,
    linewidth=2
)

ax.fill(
    angles,
    values,
    alpha=0.25
)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)

plt.title(
    "Overall DistilBERT Real-World Performance Profile",
    pad=20
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "performance_radar_chart.png"
    )
)

plt.close()

# =========================================================
# GRAPH 6
# CONFIDENCE THRESHOLD ANALYSIS
# =========================================================
thresholds = [0.5, 0.6, 0.7, 0.8]

counts = []

for threshold in thresholds:

    count = (
        df["argmax_confidence"] >= threshold
    ).sum()

    counts.append(count)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=[str(t) for t in thresholds],
    y=counts
)

plt.title(
    "High-Confidence Prediction Analysis"
)

plt.xlabel("Confidence Threshold")
plt.ylabel("Number of Predictions")

for i, v in enumerate(counts):
    plt.text(i, v + 1, str(v), ha='center')

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "confidence_threshold_analysis.png"
    )
)

plt.close()

# =========================================================
# DONE
# =========================================================
print("\n===================================")
print("ADVANCED RESEARCH GRAPHS GENERATED")
print("===================================")

print(f"\nGraphs saved to:\n{GRAPH_DIR}")