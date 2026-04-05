import requests
import time
import sys

def test_data_fetch():
    # Generate timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    url = f"https://educacionales.mendoza.edu.ar/data?_={timestamp}"
    
    print(f"Testing URL: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://educacionales.mendoza.edu.ar/educacionales"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response Content (first 500 chars):")
            print(response.text[:500])
        else:
            print("Response Content:")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_data_fetch()
