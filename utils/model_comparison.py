import matplotlib.pyplot as plt

# =========================
# FINAL MODEL RESULTS
# =========================

models = ["CNN", "LSTM", "HAN", "BERT"]

accuracy = [
    0.9978,   # CNN
    0.9973,   # LSTM
    0.9987,   # HAN
    0.9990    # BERT v2
]

# =========================
# PLOT GRAPH
# =========================

plt.figure(figsize=(10, 6))

bars = plt.bar(models, accuracy)

# Add value labels
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval,
             f"{yval:.4f}", ha='center', va='bottom', fontsize=10)

plt.title("Model Accuracy Comparison for Fake News Detection", fontsize=14)
plt.xlabel("Models", fontsize=12)
plt.ylabel("Accuracy", fontsize=12)

# Zoomed axis for better visualization
plt.ylim(0.997, 1.0)

plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()

plt.show()
