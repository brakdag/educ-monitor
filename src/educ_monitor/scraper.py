import requests
import time
import json
from datetime import datetime
from requests.exceptions import RequestException, HTTPError, Timeout
from .config import config
from .logger import get_logger
from .utils import parse_date

logger = get_logger("scraper")

def get_llamados() -> list[dict]:
    """
    Fetches teacher call data from the DGE Mendoza website.
    
    Returns:
        list[dict]: A list of processed call dictionaries.
    """
    session = requests.Session()
    headers = config.default_headers.copy()
    headers["User-Agent"] = config.user_agent

    try:
        # 1. Establish session
        session.get("https://educacionales.mendoza.edu.ar/", headers={"User-Agent": config.user_agent}, timeout=10)
        
        # 2. Fetch data
        timestamp = int(time.time() * 1000)
        url = f"https://educacionales.mendoza.edu.ar/data?_={timestamp}"
        
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            return []
        
        llamados = []
        if "datos" not in data:
            logger.warning("API response received but 'datos' key is missing.")
            return llamados

        for item in data["datos"]:
            unique_id = str(item.get("id", "unknown"))
            escuela_info = item.get("lugar_trabajo", "")
            escuela_id = escuela_info.split(' - ')[0] if ' - ' in escuela_info else escuela_info
            
            # Use the robust date parser utility
            fecha_raw = item.get("fecha_llamado_1")
            fecha_llamado = parse_date(fecha_raw)
            
            llamados.append({
                "unique_id": unique_id,
                "escuela_id": escuela_id,
                "tipo_llamado": item.get("tipo_llamado", ""),
                "fecha_llamado": fecha_llamado,
                "fecha_publicacion": datetime.now().strftime("%Y-%m-%d"),
                "raw_data": item
            })
        
        logger.info(f"Successfully fetched {len(llamados)} calls.")
        return llamados
            
    except HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except Timeout:
        logger.error("The request timed out while fetching data.")
    except RequestException as e:
        logger.error(f"Network error occurred: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in scraper: {e}", exc_info=True)
        
    return []