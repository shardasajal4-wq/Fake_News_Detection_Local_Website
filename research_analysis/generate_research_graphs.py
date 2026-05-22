import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LOAD CSV
# =========================
CSV_PATH = "research_analysis/results/live_news_results.csv"

df = pd.read_csv(CSV_PATH)

# =========================
# CREATE OUTPUT FOLDER
# =========================
GRAPH_DIR = "research_analysis/graphs"

os.makedirs(GRAPH_DIR, exist_ok=True)

# =========================
# GLOBAL STYLE
# =========================
sns.set_style("whitegrid")

plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300

plt.rcParams["font.size"] = 12
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 13

# =========================
# GRAPH 1
# PREDICTION DISTRIBUTION
# =========================
plt.figure(figsize=(8, 6))

prediction_counts = df["argmax_prediction"].value_counts()

sns.barplot(
    x=prediction_counts.index,
    y=prediction_counts.values
)

plt.title("Prediction Distribution on Live News")
plt.xlabel("Prediction")
plt.ylabel("Number of Articles")

for i, v in enumerate(prediction_counts.values):
    plt.text(i, v + 1, str(v), ha='center')

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "prediction_distribution.png"
    )
)

plt.close()

# =========================
# GRAPH 2
# CATEGORY-WISE HEATMAP
# =========================
heatmap_data = pd.crosstab(
    df["category"],
    df["argmax_prediction"]
)

plt.figure(figsize=(10, 6))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Category-wise Prediction Heatmap")

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "category_prediction_heatmap.png"
    )
)

plt.close()

# =========================
# GRAPH 3
# CONFIDENCE DISTRIBUTION
# =========================
plt.figure(figsize=(10, 6))

sns.histplot(
    df["argmax_confidence"],
    bins=20,
    kde=True
)

plt.title("Confidence Distribution")
plt.xlabel("Confidence Score")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "confidence_distribution.png"
    )
)

plt.close()

# =========================
# GRAPH 4
# AVG CONFIDENCE BY CATEGORY
# =========================
avg_confidence = (
    df.groupby("category")["argmax_confidence"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=avg_confidence.index,
    y=avg_confidence.values
)

plt.title("Average Confidence by Category")
plt.xlabel("Category")
plt.ylabel("Average Confidence")

plt.xticks(rotation=20)

for i, v in enumerate(avg_confidence.values):
    plt.text(i, v + 0.005, f"{v:.2f}", ha='center')

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "avg_confidence_by_category.png"
    )
)

plt.close()

# =========================
# GRAPH 5
# INFERENCE TIME DISTRIBUTION
# =========================
plt.figure(figsize=(10, 6))

sns.histplot(
    df["inference_time"],
    bins=20,
    kde=True
)

plt.title("Inference Time Distribution")
plt.xlabel("Inference Time (seconds)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "inference_time_distribution.png"
    )
)

plt.close()

# =========================
# GRAPH 6
# ARTICLE LENGTH VS CONFIDENCE
# =========================
plt.figure(figsize=(10, 6))

sns.scatterplot(
    x=df["article_length"],
    y=df["argmax_confidence"]
)

plt.title("Article Length vs Confidence")
plt.xlabel("Article Length")
plt.ylabel("Confidence")

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "length_vs_confidence.png"
    )
)

plt.close()

# =========================
# GRAPH 7
# CATEGORY-WISE CONFIDENCE BOXPLOT
# =========================
plt.figure(figsize=(12, 6))

sns.boxplot(
    x=df["category"],
    y=df["argmax_confidence"]
)

plt.title("Category-wise Confidence Distribution")
plt.xlabel("Category")
plt.ylabel("Confidence")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "category_confidence_boxplot.png"
    )
)

plt.close()

# =========================
# GRAPH 8
# SOURCE DISTRIBUTION
# =========================
top_sources = df["source"].value_counts().head(10)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=top_sources.index,
    y=top_sources.values
)

plt.title("Top News Sources")
plt.xlabel("Source")
plt.ylabel("Article Count")

plt.xticks(rotation=45)

for i, v in enumerate(top_sources.values):
    plt.text(i, v + 0.2, str(v), ha='center')

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_DIR,
        "top_sources.png"
    )
)

plt.close()

# =========================
# DONE
# =========================
print("\n===================================")
print("ALL RESEARCH GRAPHS GENERATED")
print("===================================")

print(f"\nGraphs saved to:\n{GRAPH_DIR}")