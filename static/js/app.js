document.addEventListener('DOMContentLoaded', function() {
    const resetBtn = document.getElementById('resetBtn');
    const urlInput = document.getElementById('url');
    
    if (resetBtn && urlInput) {
        resetBtn.addEventListener('click', function(e) {
            // Prevent default form reset behavior to handle it ourselves
            e.preventDefault();
            
            // Clear the URL input field
            urlInput.value = '';
            
            // Clear any displayed links
            const linksContainer = document.querySelector('.links-container');
            if (linksContainer) {
                linksContainer.innerHTML = '';
                
                // Re-add the heading if it was removed
                if (!linksContainer.querySelector('h3')) {
                    const heading = document.createElement('h3');
                    heading.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#00d4ff">
                            <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
                        </svg>
                        
                    `;
                    linksContainer.appendChild(heading);
                }
            }
            
            // Clear any error messages
            const errorDiv = document.querySelector('.error');
            if (errorDiv) errorDiv.remove();
            
            // Return focus to the input field
            urlInput.focus();
        });
        
        // Also clear results when typing in the input field
        urlInput.addEventListener('input', function() {
            const linksContainer = document.querySelector('.links-container');
            if (linksContainer && linksContainer.querySelectorAll('.link-item').length > 0) {
                linksContainer.querySelectorAll('.link-item').forEach(item => item.remove());
            }
            
            const errorDiv = document.querySelector('.error');
            if (errorDiv) errorDiv.remove();
        });
    }
});