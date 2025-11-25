document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const textInput = document.getElementById('textInput');
    const resultsDiv = document.getElementById('results');
    const emotionResult = document.getElementById('emotionResult');
    const suggestionsDiv = document.getElementById('suggestions');
    const historyDiv = document.getElementById('history');
    const analyzeText = document.getElementById('analyzeText');
    const analyzeSpinner = document.getElementById('analyzeSpinner');

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeTextHandler);
    }

    // Load history when page loads
    loadHistory();

    async function analyzeTextHandler() {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        if (text.length < 10) {
            alert('Please enter at least 10 characters for better analysis.');
            return;
        }

        // Show loading state
        analyzeBtn.disabled = true;
        analyzeText.textContent = 'Analyzing...';
        analyzeSpinner.classList.remove('d-none');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
                loadHistory(); // Refresh history
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing the text. Please try again.');
        } finally {
            // Reset button state
            analyzeBtn.disabled = false;
            analyzeText.textContent = 'Analyze Emotion';
            analyzeSpinner.classList.add('d-none');
        }
    }

    function displayResults(data) {
        resultsDiv.style.display = 'block';
        
        // Smooth scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        const confidenceColor = data.confidence > 80 ? 'success' : 
                              data.confidence > 60 ? 'warning' : 'danger';
        
        emotionResult.innerHTML = `
            <div class="alert alert-${confidenceColor}">
                <h6 class="alert-heading">Detected Emotion</h6>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="h4 mb-0">${data.emotion}</span>
                    <span class="badge bg-${confidenceColor} fs-6">${data.confidence}% Confidence</span>
                </div>
            </div>
        `;

        const suggestionsHtml = `
            <h6>💡 Suggestions for managing ${data.emotion}:</h6>
            <div class="list-group">
                ${data.suggestions.map((suggestion, index) => `
                    <div class="list-group-item">
                        <div class="d-flex align-items-center">
                            <span class="badge bg-primary me-3">${index + 1}</span>
                            <span>${suggestion}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        suggestionsDiv.innerHTML = suggestionsHtml;
    }

    async function loadHistory() {
        if (!historyDiv) return;

        try {
            const response = await fetch('/history');
            const data = await response.json();

            if (response.ok) {
                if (data.length === 0) {
                    historyDiv.innerHTML = `
                        <div class="text-center text-muted">
                            <p>No analysis history yet.</p>
                            <p>Start by analyzing some text above!</p>
                        </div>
                    `;
                } else {
                    historyDiv.innerHTML = data.map(item => `
                        <div class="card mb-3">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <h6 class="card-title mb-1">${item.emotion}</h6>
                                    <span class="badge ${item.confidence > 80 ? 'bg-success' : 'bg-warning'}">
                                        ${item.confidence}%
                                    </span>
                                </div>
                                <p class="card-text small">${item.text}</p>
                                <small class="text-muted">${new Date(item.timestamp).toLocaleString()}</small>
                            </div>
                        </div>
                    `).join('');
                }
            }
        } catch (error) {
            console.error('Error loading history:', error);
            historyDiv.innerHTML = '<p class="text-danger">Error loading history</p>';
        }
    }

    // Add Enter key support for textarea
    if (textInput) {
        textInput.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                analyzeTextHandler();
            }
        });
    }
});