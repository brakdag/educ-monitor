import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
from datetime import datetime

async def get_llamados():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "stylesheet", "font", "media"] else route.continue_())
        await page.goto("https://educacionales.mendoza.edu.ar/educacionales")
        await page.wait_for_selector("#target")
        
        content = await page.content()
        await browser.close()
        
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.select_one("table")
        if not table:
            return []
        
        llamados = []
        rows = table.select("tbody tr")
        for row in rows:
            cells = row.select("td")
            if len(cells) > 5:
                # Col 0: "1er: 12/03/2026"
                col0 = cells[0].text.strip()
                try:
                    tipo_llamado, fecha_raw = col0.split(':', 1)
                    tipo_llamado = tipo_llamado.strip()
                    fecha_str = fecha_raw.strip()
                    # Convert dd/mm/yyyy to yyyy-mm-dd
                    fecha_llamado = datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                except Exception:
                    tipo_llamado = col0
                    fecha_llamado = None

                escuela_info = cells[4].text.strip()
                escuela_id = escuela_info.split(' - ')[0] if ' - ' in escuela_info else escuela_info
                
                # Assume Llamado ID is unique to the call + escuela
                llamado_id = col0
                unique_id = f"{llamado_id}_{escuela_id}"
                
                llamados.append({
                    "unique_id": unique_id,
                    "escuela_id": escuela_id,
                    "content": row.text.strip(),
                    "tipo_llamado": tipo_llamado,
                    "fecha_llamado": fecha_llamado,
                    "fecha_publicacion": datetime.now().strftime("%Y-%m-%d") # simplified
                })
        return llamados
