from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import json

def extract_domain(url):
    """Extract the base domain from a URL."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def format_date(timestamp):
    """Convert Unix timestamp to YYYY-MM-DD format."""
    try:
        # Convert string to integer if it's not empty
        if timestamp:
            timestamp = int(timestamp)
            # Convert seconds to milliseconds if needed
            if timestamp > 253402300799:  # Max year 9999 in seconds
                timestamp = timestamp // 1000
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        pass
    return ""

def extract_urls(html_file):
    """Extract URLs from HTML bookmarks file and organize by domain."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')
    domain_dict = {}

    # Find all <a> tags
    for link in soup.find_all('a'):
        url = link.get('href', '')
        if not url:
            continue

        domain = extract_domain(url)
        title = link.string.strip() if link.string else ''
        add_date = format_date(link.get('add_date', ''))

        if domain not in domain_dict:
            domain_dict[domain] = []

        domain_dict[domain].append({
            'title': title,
            'url': url,
            'date': add_date
        })

    # Sort each domain's links by date
    for domain in domain_dict:
        domain_dict[domain].sort(key=lambda x: x['date'] if x['date'] else '9999-12-31', reverse=True)

    return domain_dict

def main():
    input_file = 'data/bookmarks_2024_12_19_1.html'
    output_file = 'data/urls_by_domain.json'
    
    # Extract URLs and organize by domain
    domain_dict = extract_urls(input_file)
    
    # Save to JSON file with pretty printing
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(domain_dict, f, ensure_ascii=False, indent=2)
    
    print(f"URLs have been successfully extracted and saved to {output_file}")

if __name__ == "__main__":
    main()
