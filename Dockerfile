# Usa una imagen base oficial de Frappe
FROM frappe/bench:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /home/frappe/frappe-bench

# Copia los archivos necesarios para Frappe
COPY . .

# Instala las dependencias de Frappe
RUN bench setup requirements
RUN bench setup redis
RUN bench setup socketio

# Inicializa el sitio de Frappe
RUN bench new-site sym_web --mariadb-root-password root --admin-password admin

# Instala ERPNext (opcional)
# RUN bench get-app erpnext --branch version-13
# RUN bench --site mysite.local install-app erpnext

# Inicia el servidor Frappe
CMD ["bench", "start"]
