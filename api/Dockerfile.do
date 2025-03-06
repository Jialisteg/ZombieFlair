FROM python:3.12-slim

WORKDIR /app

# Copiar requirements.txt primero para aprovechar la caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos
COPY . .

# Agregar el directorio src al path de Python
ENV PYTHONPATH=/app

# Configurar variables de entorno
ENV PORT=8080

# Exponer el puerto que usará FastAPI
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 index:app 