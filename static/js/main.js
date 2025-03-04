document.addEventListener('DOMContentLoaded', () => {
    const modeSelect = document.getElementById('theory-mode');
    const franchiseContainer = document.getElementById('franchise-container');
    const franchiseInput = document.getElementById('franchise-name');
    const inputText = document.getElementById('input-text');
    const generateBtn = document.getElementById('generate-btn');
    const loadingIndicator = document.getElementById('loading');
    const theoryContainer = document.getElementById('theory-container');

    // Show/hide franchise input based on mode selection
    modeSelect.addEventListener('change', () => {
        if (modeSelect.value === 'franchise') {
            franchiseContainer.classList.remove('hidden');
        } else {
            franchiseContainer.classList.add('hidden');
        }
    });

    // Generate theory on button click
    generateBtn.addEventListener('click', async () => {
        // Input validation
        if (modeSelect.value === 'franchise' && !franchiseInput.value.trim()) {
            alert('Please enter a franchise name');
            franchiseInput.focus();
            return;
        }

        if (!inputText.value.trim()) {
            alert('Please enter some text for theory generation');
            inputText.focus();
            return;
        }

        // Prepare request data
        const requestData = {
            mode: modeSelect.value
        };

        if (modeSelect.value === 'unhinged') {
            requestData.text = inputText.value.trim();
        } else {
            requestData.franchise_name = franchiseInput.value.trim();
            requestData.text = inputText.value.trim();
        }

        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        theoryContainer.innerHTML = '';

        try {
            // Call the API
            const response = await fetch('/generate-theory', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            // Handle API response
            if (response.ok) {
                const data = await response.json();
                theoryContainer.innerHTML = formatTheory(data.theory);
            } else {
                const errorData = await response.json();
                theoryContainer.innerHTML = `<div class="text-red-500"><p>Error: ${errorData.detail || 'Failed to generate theory'}</p></div>`;
            }
        } catch (error) {
            theoryContainer.innerHTML = `<div class="text-red-500"><p>Error: ${error.message || 'Something went wrong'}</p></div>`;
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
        }
    });

    // Format theory with basic markdown-like formatting
    function formatTheory(theory) {
        // Replace line breaks with paragraph tags
        let formatted = theory.split('\n\n').map(para => `<p>${para}</p>`).join('');
        
        // Bold text between ** markers
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text between * markers
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        return formatted;
    }
});
