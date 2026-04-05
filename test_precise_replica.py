import requests
import time

def test_precise_replica():
    # Exact URL based on headers
    timestamp = int(time.time() * 1000)
    url = f"https://educacionales.mendoza.edu.ar/data?_={timestamp}"
    
    # Replicating EXACT headers from user-provided request
    headers = {
        "Host": "educacionales.mendoza.edu.ar",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
        "Referer": "https://educacionales.mendoza.edu.ar/",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1, i"
    }

    print(f"Fetching: {url}")
    
    try:
        # Need to ensure cookies are present from the main page visit first
        session = requests.Session()
        session.get("https://educacionales.mendoza.edu.ar/", headers={"User-Agent": headers["User-Agent"]})
        
        response = session.get(url, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            print("Response Content (first 500 chars):")
            print(response.text[:500])
        else:
            print("Response Content:")
            print(response.text[:500])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_precise_replica()
