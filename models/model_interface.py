import torch
import os
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


class FakeNewsModel:

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None

        print("Fake News Model Initialized")

    # =========================
    # LOAD MODEL
    # =========================
    def load_model(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, ".."))

        model_path = os.path.join(
            project_root,
            "models",
            "trained_models",
            "final_model"
        )

        model_path = os.path.abspath(model_path)

        print("Loading model from:", model_path)

        # Load tokenizer
        self.tokenizer = DistilBertTokenizer.from_pretrained(
            model_path,
            local_files_only=True
        )

        # Load model
        self.model = DistilBertForSequenceClassification.from_pretrained(
            model_path,
            local_files_only=True
        )

        self.model.to(self.device)
        self.model.eval()

        print("DistilBERT model loaded successfully")

    # =========================
    # PREDICT
    # =========================
    def predict(self, text):

        cleaned_text = text.lower()

        inputs = self.tokenizer(
            cleaned_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)

        real_prob = probs[0][0].item()
        fake_prob = probs[0][1].item()

        max_prob = max(real_prob, fake_prob)
        gap = abs(real_prob - fake_prob)

        # =========================
        # METHOD 1: ARGMAX
        # =========================
        argmax_class = torch.argmax(probs).item()

        label_map = {
            0: "Real",
            1: "Fake"
        }

        argmax_prediction = label_map[argmax_class]
        argmax_confidence = probs[0][argmax_class].item()

        # =========================
        # METHOD 2: THRESHOLD
        # =========================
        if max_prob < 0.55:
            threshold_prediction = "Uncertain"
            threshold_confidence = max_prob

        elif gap > 0.25:
            if real_prob > fake_prob:
                threshold_prediction = "Real"
                threshold_confidence = real_prob
            else:
                threshold_prediction = "Fake"
                threshold_confidence = fake_prob
        else:
            threshold_prediction = "Uncertain"
            threshold_confidence = max_prob

        # =========================
        # METHOD 3: DIFFERENCE
        # =========================
        if real_prob - fake_prob > 0.4:
            diff_prediction = "Real"
            diff_confidence = real_prob

        elif fake_prob - real_prob > 0.4:
            diff_prediction = "Fake"
            diff_confidence = fake_prob

        else:
            diff_prediction = "Uncertain"
            diff_confidence = max_prob

        # =========================
        # FINAL DECISION
        # =========================
        if argmax_prediction == "Real" and real_prob > 0.55:
            final_prediction = "Real"
            final_confidence = real_prob

        elif argmax_prediction == "Fake" and fake_prob > 0.55:
            final_prediction = "Fake"
            final_confidence = fake_prob

        elif threshold_prediction != "Uncertain":
            final_prediction = threshold_prediction
            final_confidence = threshold_confidence

        else:
            final_prediction = "Uncertain"
            final_confidence = max_prob

        # =========================
        # RETURN
        # =========================
        return {
            "original_text": text,
            "cleaned_text": cleaned_text,

            "argmax": {
                "prediction": argmax_prediction,
                "confidence": argmax_confidence
            },

            "threshold": {
                "prediction": threshold_prediction,
                "confidence": threshold_confidence
            },

            "difference": {
                "prediction": diff_prediction,
                "confidence": diff_confidence
            },

            "final": {
                "prediction": final_prediction,
                "confidence": final_confidence
            },

            "real_probability": real_prob,
            "fake_probability": fake_prob
        }