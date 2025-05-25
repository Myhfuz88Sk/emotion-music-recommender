import matplotlib.pyplot as plt

def plot_emotion_distribution(emotion_counts, save_path="static/emotion_chart.png"):
    labels = list(emotion_counts.keys()) # Convert dict_keys to list
    sizes = list(emotion_counts.values()) # Convert dict_values to list

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors) # Added startangle and colors for better visual
    plt.title('Emotion Distribution')
    plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(save_path)
    plt.close()