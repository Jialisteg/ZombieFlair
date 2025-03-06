#!/bin/sh

# Reemplazar la URL de la API en los archivos JavaScript
find /usr/share/nginx/html -name "*.js" -exec sed -i "s|REACT_APP_API_URL|${REACT_APP_API_URL}|g" {} \;

# Iniciar Nginx
nginx -g 'daemon off;' 