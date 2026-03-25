# Scraping de Llamados Docentes - DGE Mendoza

Sistema automatizado de monitoreo de llamados docentes, diseñado para correr en servidores de bajo recurso (ej. Atom N2600 + Home Assistant).

## Características
- **Optimización de recursos:** Se utiliza Playwright en modo headless, optimizado para no cargar imágenes ni CSS, ejecutándose cada 1 hora para minimizar el impacto en memoria.
- **Integración:** Notificaciones publicadas a través de protocolo **MQTT**.
- **Persistencia:** Almacenamiento local mediante SQLite para historial y detección de nuevos llamados.

## Requisitos
- Python 3.11+
- `playwright`, `requests`, `beautifulsoup4`, `paho-mqtt`
- SQLite3

## Integración
El sistema publica mensajes en un servidor MQTT. Esto permite integrar fácilmente los datos en Home Assistant (vía sensor MQTT), Node-RED o cualquier otro sistema de automatización.

## Session Resumption Guide
1. **Ambiente:** Activa el entorno virtual antes de ejecutar cualquier comando: `source venv/bin/activate`.
2. **Configuración:** Asegúrate de tener el archivo `.env` configurado según `.env.example` con las escuelas y los datos del broker MQTT.
3. **Ejecución:** Usa `./run.sh` para una ejecución manual y pruebas.
4. **Logs:** Consulta `cron.log` para revisar errores de ejecución.
5. **Base de Datos:** El estado de los llamados se mantiene en `llamados.db`.
