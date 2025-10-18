document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('resumeFile');
    const submitBtn = document.getElementById('submitBtn');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Screening...';

    fetch('/api/upload/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            // Update score with animation
            const score = data.score;
            document.getElementById('progressFill').style.width = score + '%';
            document.getElementById('scoreText').textContent = score + '%';
            document.getElementById('text').textContent = data.extracted_text.substring(0, 500) + '...';  // Truncate for readability
            document.getElementById('results').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    })
    .finally(() => {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-play"></i> Screen Resume';
    });
});