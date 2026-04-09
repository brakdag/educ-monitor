#!/bin/bash
# install.sh - Configuración inicial robusta de educ_monitor

# Detener el script si cualquier comando falla
set -e

echo "⚙️ Iniciando instalación completa y robusta..."

# 0. Verificar si es root
if [ "$EUID" -ne 0 ]; then 
  echo "⚠️ Error: Este script debe ejecutarse como root o con sudo."
  exit 1
fi

# 1. Instalar dependencias del sistema
echo "✅ Verificando dependencias del sistema..."
if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "Instalando python3-venv..."
    apt update && apt install -y python3-venv
else
    echo "python3-venv ya está instalado."
fi

# 2. Gestionar entorno virtual (Limpieza de venv corruptos)
echo "✅ Configurando entorno virtual..."
if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
    echo "⚠️ Se detectó un entorno virtual corrupto. Recreando..."
    rm -rf venv
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Entorno virtual creado."
else
    echo "El entorno virtual ya existe y es válido."
fi

# 3. Instalar el proyecto y dependencias usando rutas directas
echo "✅ Instalando el proyecto en modo editable..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -e ".[dev]"

# 4. Preparar configuración (.env)
if [ ! -f ".env" ]; then
    echo "✅ Creando configuración inicial en .env..."
    cat <<EOF > .env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=educacionales/llamados
SCHOOL_FILTER=4117,4124,4114,4239,4063
EOF
else
    echo "El archivo .env ya existe, se mantiene la configuración actual."
fi

# 5. Asegurar permisos
chmod +x run.sh

# 6. Inicializar BD
echo "✅ Inicializando base de datos..."
./venv/bin/python3 -c "from educ_monitor.database import init_db; init_db(); print('Base de datos creada exitosamente.')"

echo "
✅✅✅ Instalación completada con éxito. El sistema está listo para funcionar."
