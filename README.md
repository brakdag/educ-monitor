# educ-monitor

Sistema automatizado de monitoreo de llamados docentes (DGE Mendoza).

## Características
- **Scraping Optimizado:** Captura directa de datos JSON mediante `requests`.
- **Persistencia Total:** Almacena historial completo en SQLite (`llamados.db`).
- **Filtrado Inteligente:** Notifica únicamente llamados nuevos vigentes.
- **Integración:** Notificaciones publicadas vía MQTT.
- **Interfaz CLI:** Gestión de configuración y ejecución sencilla.

## Roles de Automatización (Agentes)
- **Agente Scraper (Eficiente, c/1 hora):** Obtiene datos dinámicos mediante
  `requests` (optimizado, sin necesidad de navegador).
- **Agente Analista:** Comparación de estados contra el último registro en
  SQLite.
- **Agente Notificador:** Integración con Broker MQTT local. Publica JSON para
  Home Assistant.

## Instalación
1. Clonar el repositorio.
2. Ejecutar `./install.sh` para configurar el entorno.
3. Completar la configuración inicial en `.env`.

## Configuración y Uso (CLI)
`python3 -m educ_monitor.cli` permite configurar la aplicación:
- `--run`: Ejecuta el ciclo de monitoreo.
- `--set-mqtt-ip <ip>`: Configura el broker MQTT.
- `--set-filters <lista_escuelas>`: Configura filtros de escuela.
- `--show-config`: Muestra la configuración actual.

## Gestión de TODO.md
Si existe un archivo `TODO.md` en el repositorio, se debe procesar de la
siguiente manera:
1. Subir cada elemento del archivo como un issue a GitHub.
2. Si un issue existe pero está cerrado, se debe reabrir.
3. Si no existe, se crea uno nuevo.
4. Al finalizar, el archivo `TODO.md` debe ser eliminado.

**Nota para IAs:** Si detectas la presencia de un archivo `TODO.md`,
pregunta SIEMPRE al usuario antes de ejecutar este proceso automático.
