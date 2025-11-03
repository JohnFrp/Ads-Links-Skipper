from flask import Flask, render_template, request
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def extract_filtered_download_links(url):
    try:
        scraper = cloudscraper.create_scraper()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        
        response = scraper.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = f"{url.split('/')[0]}//{url.split('/')[2]}"
        
        allowed_domains = [
            'usersdrive.com',
            'yoteshinportal.cc',
            'gdtot',
            'megaup.net',
            'terabox.app',
            't.me/sender_RMC_bot'
            
        ]
        
        download_links = set()
        all_links = soup.find_all('a', href=True)
        
        for a in all_links:
            href = a['href']
            if not href.startswith('http'):
                href = urljoin(base_url, href)
            
            if any(domain in href.lower() for domain in allowed_domains):
                download_links.add(href)
        
        return sorted(download_links) if download_links else "No matching download links found"
    
    except Exception as e:
        return f"Error extracting links: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    links = None
    url = ""
    error = None
    
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            links = extract_filtered_download_links(url)
            if links and isinstance(links, str) and links.startswith("Error"):
                error = links
                links = None
    
    return render_template('index.html', 
                         links=links, 
                         url=url, 
                         error=error,
                         allowed_domains=[
                             "usersdrive.com", 
                             "yoteshinportal.cc", 
                             "gdtot", 
                             "megaup.net",
                             "terabox.app"
                             
                             
                         ])

if __name__ == '__main__':

    app.run(debug=True)

