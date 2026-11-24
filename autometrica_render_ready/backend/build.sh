#!/usr/bin/env bash
set -euo pipefail

echo "==> Instalando dependencias"
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "==> Verificando conexión a PostgreSQL"
python -c "from app.database import engine; connection = engine.connect(); connection.close(); print('Conexión de base de datos correcta')"

echo "==> Creando tablas declaradas en SQLAlchemy"
python -c "from app.main import app; print('Aplicación FastAPI importada y esquema inicializado')"

echo "==> Creando administrador inicial si las variables están configuradas"
python bootstrap_admin.py

echo "==> Build completado"
