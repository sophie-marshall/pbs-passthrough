// Access video element
const video = document.getElementById('videoPlayer');

const canvas = document.getElementById("frameCapture");
const ctx = canvas.getContext("2d"); // Corrected variable name

// Select paragraph element to fill in
const frameNumberParagraph = document.getElementById('frameNumber');

const queryResult = document.getElementById("queryResult");

// Function to toggle display
function toggleDisplay() {
    if (canvas.style.display === "none") {
        console.log("Displaying canvas");
        canvas.style.display = "block";
        queryResult.style.display = "none";
    } else {
        console.log("Displaying queryResult");
        canvas.style.display = "none";
        queryResult.style.display = "block";
    }
}

// Track time to help calculate frame
video.addEventListener('timeupdate', function() {
    // Calculate and display frame number
    const frameNumber = Math.floor(video.currentTime * 30); // Assuming 30 frames per second
    frameNumberParagraph.textContent = 'Frame number: ' + frameNumber;

    // Take a screenshot every 10 frames
    if (frameNumber % 10 === 0) {
        // Capture the frame
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Send the frame to the facial-recognition endpoint for analysis
        canvas.toBlob(function(blob) {
            const formData = new FormData();
            formData.append("image", blob, "frame.png");

            // Send image to server
            fetch("/facial-recognition", { // Update the URL to match your endpoint
                method: "POST", 
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response not ok");
                }
                return response.json();
            })
            .then(data => {
                // Update canvas with boxed image
                const boxedImageBase64 = data.boxed_image;
                const img = new Image();
                img.onload = function() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear previous frame
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height); // Draw new frame
                };
                img.src = 'data:image/jpeg;base64,' + boxedImageBase64;

                const embeddings = data.embeddings;
                
                fetch("/query", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }, 
                    body: JSON.stringify({ embeddings })
                })
                .then(response => response.json())
                .then(data => {
                    const formattedJson = JSON.stringify(data, null, 2);
                    queryResult.textContent = formattedJson
                })
                .catch(error => {
                    console.error("Error querying database:", error)
                })
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});





