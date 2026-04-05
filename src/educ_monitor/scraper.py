import requests
import time
from datetime import datetime

def get_llamados():
    session = requests.Session()
    
    # Header configuration based on successful reproduction
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1"
    headers = {
        "Host": "educacionales.mendoza.edu.ar",
        "User-Agent": user_agent,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
        "Referer": "https://educacionales.mendoza.edu.ar/",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1, i"
    }

    try:
        # 1. Establish session
        session.get("https://educacionales.mendoza.edu.ar/", headers={"User-Agent": user_agent})
        
        # 2. Fetch data
        timestamp = int(time.time() * 1000)
        url = f"https://educacionales.mendoza.edu.ar/data?_={timestamp}"
        
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        llamados = []
        if "datos" in data:
            for item in data["datos"]:
                unique_id = str(item.get("id"))
                
                escuela_info = item.get("lugar_trabajo", "")
                escuela_id = escuela_info.split(' - ')[0] if ' - ' in escuela_info else escuela_info
                
                fecha_raw = item.get("fecha_llamado_1")
                fecha_llamado = None
                if fecha_raw:
                    try:
                        fecha_llamado = datetime.strptime(fecha_raw.split(' ')[0], "%d/%m/%y").strftime("%Y-%m-%d")
                    except:
                        pass
                
                llamado_data = {
                    "unique_id": unique_id,
                    "escuela_id": escuela_id,
                    "tipo_llamado": item.get("tipo_llamado", ""),
                    "fecha_llamado": fecha_llamado,
                    "fecha_publicacion": datetime.now().strftime("%Y-%m-%d"),
                    "raw_data": item
                }
                
                llamados.append(llamado_data)
        
        return llamados
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
