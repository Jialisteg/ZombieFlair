FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Asegúrate de que Python pueda encontrar los módulos del proyecto
ENV PYTHONPATH=/app

# Exponer el puerto que usará FastAPI
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "5000"] 