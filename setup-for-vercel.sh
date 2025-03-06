#!/bin/bash

# Script para preparar la aplicación para despliegue en Vercel
# Ejecuta este script localmente antes de hacer push a GitHub

# Verificar si la carpeta frontend existe
if [ ! -d "frontend" ]; then
  echo "Error: La carpeta 'frontend' no existe"
  exit 1
fi

# Copiar archivos de React
echo "Copiando archivos de React a la raíz..."
cp -r frontend/src ./
cp -r frontend/public ./

# Verificar si ya existen los archivos en la raíz
if [ -f "package.json" ] && [ -f "vercel.json" ]; then
  echo "Los archivos package.json y vercel.json ya existen en la raíz"
else
  # Copiar package.json si no existe
  [ ! -f "package.json" ] && cp frontend/package.json ./
  
  # Crear vercel.json si no existe
  if [ ! -f "vercel.json" ]; then
    echo '{
  "version": 2,
  "buildCommand": "npm install && npm run build",
  "outputDirectory": "build",
  "framework": "create-react-app",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}' > vercel.json
  fi
fi

echo "Preparación completada. Ahora puedes hacer commit y push para desplegar en Vercel." 