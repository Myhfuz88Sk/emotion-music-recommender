// Function to handle navigation from the index page and store user name
function goToNextPage() {
    const userName = document.getElementById('feeling').value;
    localStorage.setItem('userName', userName); // Store name in browser's local storage
    window.location.href = '/feeling'; // Navigate to the feeling page
}

// Function to run when the feeling page loads (to display user's name and hide results initially)
document.addEventListener('DOMContentLoaded', () => {
    const userName = localStorage.getItem('userName'); // Retrieve name
    if (userName) {
        // Update all elements with id "oldFeeling" (if multiple exist)
        document.querySelectorAll('#oldFeeling').forEach(span => {
            span.textContent = userName;
        });
    }

    // Hide the prediction results section initially
    document.getElementById('predictionResults').style.display = 'none';
});

// Function to handle emotion prediction and song recommendation when "Get Music Recs" is clicked
async function showFinalFeeling() {
    const newFeelingText = document.getElementById('newFeeling').value;
    const resultFeeling = document.getElementById('resultFeeling');
    const predictedEmotionSpan = document.getElementById('predictedEmotionSpan');
    const songList = document.getElementById('songList');
    const predictionResultsDiv = document.getElementById('predictionResults');

    // Basic input validation: check if the text input is empty or just whitespace
    if (!newFeelingText.trim()) {
        resultFeeling.textContent = "Please tell me how you feel!";
        predictionResultsDiv.style.display = 'none'; // Ensure results are hidden if input is empty
        return;
    }

    resultFeeling.textContent = "Analyzing your feelings..."; // Show a processing message
    predictionResultsDiv.style.display = 'none'; // Hide previous results while processing

    try {
        // Send a POST request to the Flask /predict endpoint
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: newFeelingText }) // Send the user's text as JSON
        });

        // Check if the HTTP response was successful (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json(); // Parse the JSON response from Flask

        // Handle errors returned specifically from the Flask API (e.g., "No text provided")
        if (data.error) {
            resultFeeling.textContent = `Error: ${data.error}`;
            predictionResultsDiv.style.display = 'none';
        } else {
            resultFeeling.textContent = ''; // Clear any processing message

            // Display the predicted emotion
            predictedEmotionSpan.textContent = data.emotion;

            // Clear any existing song list items from previous predictions
            songList.innerHTML = '';

            // Check if the 'songs' array exists in the response data and has elements
            if (data.songs && data.songs.length > 0) {
                data.songs.forEach(song => {
                    const listItem = document.createElement('li'); // Create an <li> element for each song
                    const songLink = document.createElement('a'); // Create an <a> (anchor) element for the link

                    // Set the text that will be displayed for the link (e.g., "Song Title by Artist")
                    songLink.textContent = `${song.title} by ${song.artist}`;

                    // *** CRITICAL CHANGE: Use song.url instead of song.link ***
                    if (song.url) { // Check for 'url' property from your CSV [cite: 1]
                        songLink.href = song.url; // Use 'song.url' for the href [cite: 1]
                        songLink.target = "_blank"; // Open the link in a new browser tab
                        songLink.rel = "noopener noreferrer"; // Security best practice for target="_blank"
                    } else {
                        // If 'song.url' is missing or empty, indicate that no link is available
                        songLink.textContent += " (No link available)";
                        songLink.style.color = "grey"; // Make it visually distinct and non-clickable looking
                    }

                    listItem.appendChild(songLink); // Add the <a> tag to the <li> tag
                    songList.appendChild(listItem); // Add the <li> tag to the <ul> (songList element)
                });
            } else {
                // Message if no songs are found for the predicted emotion
                songList.innerHTML = '<li>No specific songs found for this emotion.</li>';
            }
            predictionResultsDiv.style.display = 'block'; // Show the section containing results (emotion and songs)
        }
    } catch (error) {
        // Catch and log any errors that occur during the fetch operation or response parsing
        console.error('Fetch error:', error);
        resultFeeling.textContent = `Could not get recommendations. Please try again. Error: ${error.message}`;
        predictionResultsDiv.style.display = 'none'; // Hide results on error
    }
}