FROM python:3.9-slim

WORKDIR /app

# Copiar archivos de configuración primero (para aprovechar el caché de Docker)
COPY requirements.txt setup.py config.yaml ./
COPY README.md ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copiar el código fuente
COPY src/ ./src/
COPY run.py ./

# Crear directorio de logs
RUN mkdir -p logs

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

# Exponer puerto (para futuras expansiones como interfaz web)
EXPOSE 8000

# Ejecutar la aplicación al iniciar el contenedor
CMD ["python", "run.py"] 