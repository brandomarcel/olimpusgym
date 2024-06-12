# Usa una imagen base oficial de Frappe para la versión 13
FROM frappe/bench:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /home/frappe/frappe-bench

# Actualiza el sistema y las dependencias necesarias
RUN apt-get update
RUN apt-get install -y curl git vim
RUN rm -rf /var/lib/apt/lists/*


# Copia los archivos necesarios para Frappe
COPY . .

# Instala las dependencias de Frappe
RUN pip3 install -r requirements.txt

# Inicializa el sitio de Frappe
RUN bench init --frappe-branch version-13 frappe-bench
WORKDIR /home/frappe/frappe-bench/sites
RUN bench new-site olimpus_gym --mariadb-root-password root --admin-password admin

# Instala ERPNext versión 13
# RUN bench get-app erpnext --branch version-13
# RUN bench --site mysite.local install-app erpnext

# Expone el puerto en el que la aplicación escuchará
EXPOSE 8000

# Inicia el servidor Frappe
CMD ["bench", "start"]

