import os

# Define the base directory of your project
# This assumes config.py is in the root of your project (e.g., C:\Users\myhfuz\Desktop\exp1\)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths to your model and associated files
# These paths are relative to the BASE_DIR
MODEL_PATHS = {
    "model": os.path.join(BASE_DIR, "model", "emotion_pipeline.pkl"),
    "label_encoder": os.path.join(BASE_DIR, "model", "label_encoder.pkl"),
    "vectorizer": os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")
}

# Define paths to your CSV data files
# These paths are relative to the BASE_DIR
CSV_PATHS = {
    "emotions": os.path.join(BASE_DIR, "data", "emotions.csv")
}

# You can add other configuration settings here as needed
# For example, API keys, database connection strings, etc.