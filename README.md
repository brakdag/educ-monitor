# educ-monitor

Sistema automatizado de monitoreo de llamados docentes (DGE Mendoza).

## Características
- **Scraping Optimizado:** Captura directa de datos JSON desde los servicios de la DGE.
- **Persistencia Total:** Almacena el historial completo en SQLite (`llamados.db`).
- **Filtrado Inteligente:** Notifica únicamente llamados nuevos que coinciden con los filtros de escuela y que están vigentes.
- **Integración:** Notificaciones publicadas vía **MQTT**.
- **Interfaz CLI:** Gestión de configuración y ejecución sencilla mediante línea de comandos.

## Instalación
1. Clonar el repositorio.
2. Ejecutar `./install.sh` para configurar el entorno, dependencias y base de datos.
3. Completar la configuración inicial en `.env` (o usar la CLI).

## Configuración y Uso (CLI)
`educ_monitor.py` permite configurar la aplicación:

- `--run`: Ejecuta el ciclo de monitoreo.
- `--set-mqtt-ip <ip>`: Configura el broker MQTT.
- `--set-filters <lista_escuelas>`: Configura filtros de escuela (ej: `4117,4124`).
- `--show-config`: Muestra la configuración actual.

Nota: El funcionamiento asegura que SIEMPRE se registra todo en la base de datos, y solo se notifica si el llamado es nuevo, pertenece a una escuela permitida y está vigente (fecha >= hoy).

## Integración
El sistema publica mensajes JSON en un tópico MQTT configurado, ideal para Home Assistant o Node-RED.
