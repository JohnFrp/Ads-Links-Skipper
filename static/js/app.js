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
