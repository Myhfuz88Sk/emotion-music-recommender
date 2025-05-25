import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from config import MODEL_PATHS, CSV_PATHS

# ──────────────────────────────────────────────────────────────
# 1. Load Dataset
# ──────────────────────────────────────────────────────────────
# Ensure 'emotions.csv' exists in the 'data' directory
EMOTIONS_CSV_PATH = CSV_PATHS["emotions"]
if not os.path.exists(EMOTIONS_CSV_PATH):
    raise FileNotFoundError(f"'{EMOTIONS_CSV_PATH}' not found. Please place your emotion dataset there.")

df = pd.read_csv(EMOTIONS_CSV_PATH)
texts = df["text"].astype(str).values
labels = df["label"].astype(str).values

# ──────────────────────────────────────────────────────────────
# 2. Encode Labels
# ──────────────────────────────────────────────────────────────
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# ──────────────────────────────────────────────────────────────
# 3. Train/Test Split
# ──────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels_encoded, test_size=0.2, random_state=42, stratify=labels_encoded
)

# ──────────────────────────────────────────────────────────────
# 4. Build Pipeline (TF-IDF + Logistic Regression)
# ──────────────────────────────────────────────────────────────
pipeline = make_pipeline(
    TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000)
)

# ──────────────────────────────────────────────────────────────
# 5. Train Model
# ──────────────────────────────────────────────────────────────
print("🚀 Training model...")
pipeline.fit(X_train, y_train)

# ──────────────────────────────────────────────────────────────
# 6. Evaluate
# ──────────────────────────────────────────────────────────────
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Validation Accuracy: {accuracy:.4f}")

# ──────────────────────────────────────────────────────────────
# 7. Save Artifacts
# ──────────────────────────────────────────────────────────────
# Create the directory for models if it doesn't exist
os.makedirs(os.path.dirname(MODEL_PATHS["model"]), exist_ok=True)

# Save model (pipeline includes vectorizer)
with open(MODEL_PATHS["model"], "wb") as f:
    pickle.dump(pipeline, f)

# Save label encoder
with open(MODEL_PATHS["label_encoder"], "wb") as f:
    pickle.dump(label_encoder, f)

# Save vectorizer separately (optional, as it's part of the pipeline)
with open(MODEL_PATHS["vectorizer"], "wb") as f:
    pickle.dump(pipeline.named_steps["tfidfvectorizer"], f)

print("✅ Model, LabelEncoder, and Vectorizer saved to /model/")