// Function to draw the emotion chart
async function drawEmotionChart() {
  const emotionChartElement = document.getElementById("emotionChart"); // Get the chart canvas element

  if (emotionChartElement) { // Only attempt to draw the chart if the element exists
    try {
      const response = await fetch('/get_emotion_data'); // Fetch emotion data from the server

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json(); // Parse the JSON data

      const ctx = emotionChartElement.getContext('2d'); // Get the 2D rendering context
      new Chart(ctx, {
        type: 'pie', // Pie chart type
        data: {
          labels: data.labels, // Emotion labels
          datasets: [{
            data: data.counts, // Emotion counts
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)', /* Red */
              'rgba(54, 162, 235, 0.8)', /* Blue */
              'rgba(255, 206, 86, 0.8)', /* Yellow */
              'rgba(75, 192, 192, 0.8)', /* Green */
              'rgba(153, 102, 255, 0.8)', /* Purple */
              'rgba(255, 159, 64, 0.8)', /* Orange */
              'rgba(199, 199, 199, 0.8)', /* Grey */
              'rgba(83, 102, 255, 0.8)' /* Indigo */
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(199, 199, 199, 1)',
              'rgba(83, 102, 255, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true, // Chart responsiveness
          maintainAspectRatio: false, // Allows chart to resize freely within its container
          plugins: {
            title: {
              display: true, // Display title
              text: 'Distribution of Predicted Emotions', // Chart title text
              color: '#333', // Dark color for chart title
              font: {
                size: 18,
                weight: 'bold'
              }
            },
            legend: {
              labels: {
                color: '#555', // Dark color for legend labels
                font: {
                  size: 14
                }
              }
            },
            tooltip: { // Enhanced tooltips for better user experience
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed !== null) {
                            label += context.parsed + ' entries';
                        }
                        return label;
                    }
                }
            }
          }
        }
      });

    } catch (error) {
      console.error("Error fetching emotion data for chart:", error); // Log chart data error
      const chartContainer = document.querySelector('.chart-container'); // Get chart container
      if (chartContainer) {
          const errorMessage = document.createElement('p'); // Create error message element
          errorMessage.style.color = 'red';
          errorMessage.textContent = 'Failed to load chart data. Please try again later or check server logs.';
          chartContainer.appendChild(errorMessage); // Append error message to container
      }
    }
  }
}

// Call the chart drawing function when the DOM is loaded
window.addEventListener("DOMContentLoaded", drawEmotionChart);