import requests
from bs4 import BeautifulSoup

url = "https://www.archives.gov/research/jfk/release-2025"

try:
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    
    total_size = 0
    count = 0
    
    for pdf_link in pdf_links:
        pdf_url = pdf_link if pdf_link.startswith('http') else f"https://www.archives.gov{pdf_link}"
        try:
            # HEAD request to get file size without downloading
            head = requests.head(pdf_url)
            size = int(head.headers.get('Content-Length', 0))  # Size in bytes
            total_size += size
            count += 1
            print(f"{pdf_url}: {size / 1024 / 1024:.2f} MB")
        except Exception as e:
            print(f"Couldn’t get size for {pdf_url}: {e}")
    
    print(f"\nTotal PDFs: {count}")
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB ({total_size / 1024 / 1024 / 1024:.2f} GB)")

except Exception as e:
    print(f"Error accessing webpage: {e}")