FROM node:18-alpine as build

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar archivos de código fuente
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa de producción
FROM nginx:alpine

# Copiar la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos de compilación de la etapa anterior
COPY --from=build /app/build /usr/share/nginx/html

# Configurar variable de entorno para el puerto
ENV PORT=80
EXPOSE 80

# Script para reemplazar API_URL al inicio
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"] 