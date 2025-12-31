import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "priority_model.pkl")
vectorizer = joblib.load(BASE_DIR / "vectorizer.pkl")

reverse_label_map = {
    0: "LOW",
    1: "MEDIUM",
    2: "HIGH"
}

def predict_priority(text):
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0]
    return reverse_label_map[prediction]