"""
config.py

Contains all application configuration variables.
This follows the Single Responsibility Principle by separating
configuration from application logic.
"""

# List of allowed domains for the final link extraction
ALLOWED_DOMAINS = [
    'usersdrive.com',
    'yoteshinportal.cc',
    'gdtot',
    'megaup.net',
    'terabox.app',
    't.me'  # Telegram links
]

# Base headers for the scraper
# This makes it easy to update the User-Agent in one place.
BASE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.google.com/'
}
