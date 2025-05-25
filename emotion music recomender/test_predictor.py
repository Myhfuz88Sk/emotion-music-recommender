from utils.predictor import predict_emotion

samples = [
    "I am so happy today!",
    "This is terrifying!",
    "Why do I feel so mad right now?",
    "I'm anxious and nervous.",
    "Such a joyful day!"
]

for text in samples:
    print(f"Input: {text} => Predicted Emotion: {predict_emotion(text)}")
