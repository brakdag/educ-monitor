import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def get_llamados():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            async with page.expect_response("**/data?*", timeout=30000) as response_info:
                await page.goto("https://educacionales.mendoza.edu.ar/educacionales")
            
            response = await response_info.value
            data = await response.json()
            
            llamados = []
            if "datos" in data:
                for item in data["datos"]:
                    # Mapping fields
                    unique_id = str(item.get("id"))
                    
                    escuela_info = item.get("lugar_trabajo", "")
                    escuela_id = escuela_info.split(' - ')[0] if ' - ' in escuela_info else escuela_info
                    
                    # Parse Date
                    fecha_raw = item.get("fecha_llamado_1")
                    fecha_llamado = None
                    if fecha_raw:
                        try:
                            # Format: "26/03/26 20:00" -> "2026-03-26"
                            fecha_llamado = datetime.strptime(fecha_raw.split(' ')[0], "%d/%m/%y").strftime("%Y-%m-%d")
                        except:
                            pass
                    
                    # Content summary
                    content = f"{item.get('nivel')} - {item.get('departamento')} - {item.get('lugar_trabajo')} - {item.get('articulo')}"
                    
                    llamados.append({
                        "unique_id": unique_id,
                        "escuela_id": escuela_id,
                        "content": content,
                        "tipo_llamado": item.get("tipo_llamado", ""),
                        "fecha_llamado": fecha_llamado,
                        "fecha_publicacion": datetime.now().strftime("%Y-%m-%d")
                    })
            
            await browser.close()
            return llamados
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            await browser.close()
            return []
