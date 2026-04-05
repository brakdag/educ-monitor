# Roles de Automatización (Agentes)

Todos los archivos deben tener un máximo de 80 caracteres por línea para una mejor legibilidad.

## 1. Agente Scraper (Eficiente, c/1 hora)
- **Objetivo:** Obtener datos dinámicos con consumo optimizado.
- **Acción:**
  1. Ejecuta Playwright en modo headless.
  2. Intercepta petición de red a `/data`.

## 2. Agente Analista
- **Objetivo:** Comparación de estados.
- **Acción:** Compara datos con último registro en SQLite.

## 3. Agente Notificador (Integración MQTT)
- **Objetivo:** Integración y envío de datos.
- **Acción:**
  1. Se conecta al Broker MQTT local.
  2. Publica mensaje JSON con detalles.
  3. Home Assistant recibe mensaje y dispara acciones.
