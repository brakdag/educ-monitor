import requests

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://educacionales.mendoza.edu.ar/"
}

# 1. Load initial page to get cookies
r = session.get("https://educacionales.mendoza.edu.ar/", headers=headers)
print(f"Cookies after main page: {session.cookies}")

# 2. Try fetching /educacionales (the endpoint triggered by htmx)
headers["HX-Request"] = "true"
response = session.get("https://educacionales.mendoza.edu.ar/educacionales/", headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Content length: {len(response.text)}")
print(response.text[:500])
