from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import pathlib
import pymysql

from config import MODEL_PATHS
import json 
app = Flask(__name__)

# ─── Load ML model and label encoder ────────────────────────
model = None
label_encoder = None
try:
    # Ensure these paths are correct in your config.py and files exist
    with open(MODEL_PATHS["model"], "rb") as f:
        model = pickle.load(f)

    with open(MODEL_PATHS["label_encoder"], "rb") as f:
        label_encoder = pickle.load(f)
    print("INFO: ML model and label encoder loaded successfully.")
except FileNotFoundError as e:
    print(f"ERROR: Model artifact not found: {e}. Please ensure train_model.py has been run and paths in config.py are correct.")
    print("INFO: Prediction functionality will be limited to 'unknown' emotion if model not loaded.")
except Exception as e:
    print(f"ERROR: An unexpected error occurred while loading model artifacts: {e}")
    print("INFO: Prediction functionality will be limited.")


def predict_emotion(text: str) -> str:
    """Predicts the emotion from the input text using the loaded ML model."""
    if model and label_encoder:
        try:
            # Predict the integer label
            idx = model.predict([text])[0]
            # Convert integer label back to emotion string
            emotion = label_encoder.inverse_transform([idx])[0]
            return emotion
        except Exception as e:
            print(f"ERROR: Prediction failed for text '{text}': {e}")
            return "unknown" # Fallback if prediction fails
    print("WARNING: ML model or label encoder not loaded. Cannot predict emotion.")
    return "unknown" # Fallback if model not loaded


# ─── Load songs.csv and normalize emotion column ─────────────
SONGS_PATH = pathlib.Path("data/songs.csv")
songs_df = pd.DataFrame()
if SONGS_PATH.exists():
    try:
        songs_df = pd.read_csv(SONGS_PATH, encoding="utf-8")
        # Normalize emotion column: strip whitespace and convert to lowercase
        songs_df["emotion"] = songs_df["emotion"].str.strip().str.lower()
        print(f"INFO: {SONGS_PATH} loaded successfully.")
        # Debugging: Print a sample of the loaded dataframe to console
        print("DEBUG: songs_df head after loading (check 'link' column):\n", songs_df.head())
        print("DEBUG: columns in songs_df:", songs_df.columns.tolist())
    except Exception as e:
        print(f"ERROR: Could not load {SONGS_PATH}: {e}")
        print("INFO: Song recommendations will not be available.")
else:
    print(f"WARNING: {SONGS_PATH} not found. Song recommendations will not be available.")


# Define emotion aliases for better mapping
EMOTION_ALIASES = {
    "angry": "anger",
    "mad": "anger",
    "joy": "happy",
    "super": "happy", # Example alias
    "fearful": "fear",
    "scared": "fear",
    "sadness": "sad",
    "disgust": "disgust",
    "surprise": "surprise",
    "neutral": "neutral"
}

def normalize_emotion(emotion: str) -> str:
    """Normalizes an emotion string to a standardized form."""
    e = emotion.strip().lower()
    return EMOTION_ALIASES.get(e, e) # Return alias if exists, else original


def get_songs_by_emotion(emotion: str, limit: int = 5):
    """Retrieves a limited number of random songs matching a given emotion."""
    if songs_df.empty:
        print("WARNING: songs_df is empty, no songs can be retrieved.")
        return []

    emo = normalize_emotion(emotion)
    matches = songs_df[songs_df["emotion"] == emo]

    if matches.empty:
        print(f"INFO: No songs found for normalized emotion '{emo}'.")
        return []

    # Sample randomly, ensuring not to ask for more songs than available
    num_samples = min(limit, len(matches))
    selected_songs = matches.sample(n=num_samples).to_dict(orient="records")

    # Debugging: Print songs being sent to the frontend
    print(f"DEBUG: Sending {len(selected_songs)} songs for emotion '{emo}':")
    for song in selected_songs:
        print(f"  - Title: {song.get('title')}, Artist: {song.get('artist')}, Link: {song.get('link', 'N/A')}")

    return selected_songs


# ─── Optional: log emotion predictions to MySQL database ─────
def log_to_db(text: str, emotion: str):
    """Logs the user input and predicted emotion to a MySQL database."""
    conn = None # Initialize conn to None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="4566", # Replace with your actual MySQL password
            database="emotion_music",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO emotion_logs (text_input, predicted_emotion) VALUES (%s, %s)",
                (text, emotion)
            )
        conn.commit()
        print(f"INFO: Logged '{text}' -> '{emotion}' to database.")
    except pymysql.Error as e:
        print(f"DB ERROR: Could not log to database: {e}")
        # Specific error handling for common DB issues:
        if e.args[0] == 1049: # Unknown database
            print("DB ERROR: Database 'emotion_music' does not exist. Please create it.")
        elif e.args[0] == 1146: # Table doesn't exist
            print("DB ERROR: Table 'emotion_logs' does not exist. Please create it (CREATE TABLE emotion_logs (id INT AUTO_INCREMENT PRIMARY KEY, text_input TEXT, predicted_emotion VARCHAR(255), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);)")
        elif e.args[0] == 1045: # Access denied
            print("DB ERROR: Access denied for user. Check MySQL username/password or host.")
    except Exception as e:
        print(f"DB ERROR: An unexpected error occurred during logging: {e}")
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                print(f"DB ERROR: Error closing database connection: {e}")


# ─── Flask routes ───────────────────────────────────────────
@app.route("/")
def index():
    """Renders the main index page."""
    return render_template("index.html")

@app.route("/feeling")
def feeling_page():
    """Renders the page where users can input their feeling and get music recommendations."""
    return render_template("feeling.html")

@app.route("/predict", methods=["POST"])
def predict():
    """API endpoint to receive user text, predict emotion, and return songs."""
    data = request.get_json()
    user_input = data.get("text", "")
    if user_input:
        emotion = predict_emotion(user_input)
        songs = get_songs_by_emotion(emotion)
        log_to_db(user_input, emotion) # Log the prediction
        return jsonify({"emotion": emotion, "songs": songs})
    return jsonify({"error": "No text provided"}), 400

@app.route("/chart")
def chart_page():
    """Renders the page to display emotion statistics chart."""
    return render_template("chart.html")

@app.route("/get_emotion_data")
def get_emotion_data():
    """API endpoint to fetch emotion counts from the database for charting."""
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="4566", # Replace with your actual MySQL password
            database="emotion_music",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cur:
            cur.execute("SELECT predicted_emotion, COUNT(*) as count FROM emotion_logs GROUP BY predicted_emotion")
            rows = cur.fetchall()
        
        emotion_counts = {row['predicted_emotion']: row['count'] for row in rows}
        labels = list(emotion_counts.keys())
        counts = list(emotion_counts.values())

        print("DEBUG: Emotion data for chart:", {"labels": labels, "counts": counts})
        return jsonify({"labels": labels, "counts": counts})
    except pymysql.Error as e:
        print(f"DB ERROR: Error fetching stats data: {e}")
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        print(f"ERROR: Unexpected error fetching stats data: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                print(f"DB ERROR: Error closing connection after fetching stats: {e}")


# ─── Run app ────────────────────────────────────────────────
if __name__ == "__main__":
    # Ensure debug is True only during development
    app.run(debug=True)