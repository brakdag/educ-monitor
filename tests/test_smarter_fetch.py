import requests
import time

def test_smarter_fetch():
    session = requests.Session()
    
    # 1. Simulate initial page load to get session cookies
    print("Fetching main page to get cookies...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://educacionales.mendoza.edu.ar/"
    }
    
    # Request the landing page
    session.get("https://educacionales.mendoza.edu.ar/educacionales", headers=headers)
    print(f"Cookies acquired: {session.cookies.get_dict()}")

    # 2. Try fetching the data endpoint now that we have cookies
    timestamp = int(time.time() * 1000)
    url = f"https://educacionales.mendoza.edu.ar/data?_={timestamp}"
    
    print(f"\nFetching data URL: {url}")
    
    # Add htmx-specific headers often used in these apps
    headers["HX-Request"] = "true"
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print("Response Content (first 500 chars):")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_smarter_fetch()
