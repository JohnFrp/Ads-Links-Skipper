"""
app.py

This is the main web application file (the "Controller").
Its only responsibilities are:
1. Handling web routes (e.g., '/').
2. Getting user input from the form.
3. Calling the `ScraperService` to do the "real work".
4. Passing the results (or errors) to the `index.html` template.

This file is now very "thin" and easy to read.
It adheres to SRP and DIP (it depends on the ScraperService,
not on the low-level scraping libraries).
"""
from flask import Flask, request, render_template

# Import our separated modules
from config import ALLOWED_DOMAINS, BASE_HEADERS
from scraper_service import ScraperService

# Initialize the Flask app
app = Flask(__name__)

# --- Dependency Injection ---
# We create ONE instance of our service and inject its dependencies.
# The web app doesn't know HOW the scraper works, only that it
# has an .extract_links() method.
scraper = ScraperService(
    allowed_domains=ALLOWED_DOMAINS,
    headers=BASE_HEADERS
)
# -----------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route for the application.
    Handles both displaying the form (GET) and processing it (POST).
    """
    links = None
    error = None
    url = ""
    
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not url:
            error = "Please enter a URL."
        else:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # --- Call the Service ---
            # All the complex logic is hidden inside the service.
            # We just call one method and get a clean result.
            links, error = scraper.extract_links(url)
            # ------------------------

    # Pass all data to the Jinja2 template for rendering
    return render_template(
        'index.html', 
        links=links, 
        error=error, 
        url=url, 
        allowed_domains=ALLOWED_DOMAINS
    )

if __name__ == '__main__':
    # Setting debug=False is safer for production
    # host='0.0.0.0' makes it accessible on your network
    app.run(debug=True, host='0.0.0.0', port=5000)

