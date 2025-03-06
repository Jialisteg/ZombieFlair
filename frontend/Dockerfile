FROM node:18-alpine as build

WORKDIR /app

# Copiar package.json y package-lock.json (si existe)
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto de archivos
COPY . .

# Construir la aplicación
RUN npm run build

# Etapa de producción usando Nginx
FROM nginx:alpine

# Copiar los archivos de construcción de la etapa anterior
COPY --from=build /app/build /usr/share/nginx/html

# Copiar la configuración personalizada de Nginx (la crearemos después)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer el puerto 80
EXPOSE 80

# Iniciar Nginx
CMD ["nginx", "-g", "daemon off;"] 