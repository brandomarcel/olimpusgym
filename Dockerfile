

# Usa una imagen base oficial de Frappe para la versión 13
FROM frappe/bench:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /home/frappe/frappe-bench


# Actualiza el sistema y las dependencias necesarias
USER root  
# Cambia al usuario root para ejecutar los comandos como root

# Actualiza el sistema y las dependencias necesarias
RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y redis-server
# Restaura el usuario predeterminado
USER frappe  
# Cambia a tu usuario predeterminado



# Copia los archivos necesarios para Frappe
COPY . .

# Instala las dependencias de Frappe
RUN pip3 install -r requirements.txt
# Instala la herramienta Bench
RUN pip3 install frappe-bench
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

