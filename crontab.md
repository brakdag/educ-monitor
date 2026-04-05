# Instrucciones para configurar cron job de educ-monitor

## Objetivo
Ejecutar el script de monitoreo (`run.sh`) cada hora entre las 07:00 y las 18:00 horas.

## Pasos a seguir

### 1. Verificar la ubicación del proyecto
Ejecuta el siguiente comando para confirmar el path absoluto del proyecto:
```bash
pwd
```
La salida debe ser el directorio donde están los archivos `run.sh`, `educ_monitor.py`, etc. **Guarda esta ruta para usarla en los pasos siguientes.**

### 2. Revisar el contenido de `run.sh`
Confirma qué ejecuta exactamente este script para asegurar que llama al monitor correctamente:
```bash
cat run.sh
```
Debe contener algo similar a:
```
python3 educ_monitor.py --run
```
*(Asumiendo que estás ejecutando este comando desde el directorio del proyecto)*

### 3. Abrir el editor de crontab de forma segura
Ejecuta:
```bash
crontab -e
```
- Selecciona tu editor preferido (por ejemplo, `nano`) si es la primera vez que lo usas.
- Se abrirá el archivo de crontab de tu usuario para edición.

### 4. Añadir la línea de cron
Pega exactamente la siguiente línea, **reemplazando [RUTA_DEL_PROYECTO]** con la ruta que obtuviste en el paso 1:
```
0 7-18 * * * [RUTA_DEL_PROYECTO]/run.sh >> [RUTA_DEL_PROYECTO]/cron.log 2>&1
```

#### Desglose de la expresión cron:
- `0` → Minuto 0 (en punto de cada hora).
- `7-18` → Horas desde las 07:00 hasta las 18:00 (inclusive).
- `* * *` → Todos los días del mes, todos los meses y todos los días de la semana.
- El comando ejecutará `run.sh` desde tu proyecto y redirigirá tanto la salida estándar como los errores al archivo `cron.log` para su posterior revisión.

### 5. Guardar y salir del editor
- Si usas `nano`: presiona `Ctrl+O` → `Enter` para guardar → `Ctrl+X` para salir.
- Si usas `vi`/`vim`: escribe `:wq` y presiona `Enter`.

### 6. Verificar que la línea se guardó correctamente
Ejecuta:
```bash
crontab -l
```
Deberías ver la línea que acabas de añadir en la lista de trabajos cron.

### 7. (Opcional) Probar inmediatamente
Para verificar que el script funciona sin esperar a la próxima hora programada:
```bash
./run.sh
```
*(Ejecuta esto desde el directorio del proyecto)*

Luego revisa el log para confirmar una ejecución exitosa:
```bash
tail -n 20 cron.log
```
Busca indicaciones de que el monitor se ejecutó correctamente (por ejemplo, mensajes de "Nuevo llamado vigente..." o similares).

## Notas importantes

1. **Rutas en cron**: Las líneas de cron requieren rutas absolutas o rutas relativas desde el directorio home del usuario. Por eso es necesario usar la ruta absoluta del proyecto verificada en el paso 1.
2. **Permisos de ejecución**: Asegúrate de que `run.sh` tenga permiso de ejecución:
   ```bash
   chmod +x run.sh
   ```
3. **Rotación de logs**: Ten en cuenta que `cron.log` crecerá con el tiempo. Considera implementar una estrategia de rotación de logs en el futuro si el archivo llega a ser muy grande.
4. **Zona horaria**: Cron utiliza la zona horaria del sistema donde se ejecuta. Verifica que la zona horaria de tu servidor coincida con tu horario local esperado.

Con estos pasos, tu monitor educ-monitor se ejecutará automáticamente cada hora entre las 07:00 y las 18:00, dejando un registro detallado de su actividad en `cron.log` para facilitar la depuración y el seguimiento.