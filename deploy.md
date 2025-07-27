# Guía de Despliegue a Producción: The Green Economics

Esta guía detalla los pasos necesarios para desplegar la aplicación Django en un servidor de producción utilizando Nginx, Gunicorn y Systemd.

## Arquitectura de Despliegue

La arquitectura que seguiremos es un estándar robusto para aplicaciones Django:

*   **Nginx:** Como servidor web y reverse proxy. Se encargará de recibir las peticiones HTTP/HTTPS, servir los archivos estáticos y multimedia directamente y pasar las peticiones dinámicas a Gunicorn.
*   **Gunicorn:** Como servidor de aplicaciones WSGI. Ejecutará el código Python de Django.
*   **Systemd:** Como gestor de servicios. Se asegurará de que Gunicorn se inicie automáticamente con el servidor y se reinicie si falla.
*   **MySQL:** La base de datos de producción.
*   **Virtual Environment:** Para aislar las dependencias de Python del proyecto.

---

## Guía de Despliegue Paso a Paso

### Paso 1: Preparación del Servidor

1.  **Provisiona un servidor:** Necesitarás un servidor con acceso root/sudo (ej. Ubuntu 22.04).

2.  **Instala dependencias del sistema:** Conéctate a tu servidor por SSH e instala todo lo necesario.

    ```bash
    sudo apt update
    sudo apt install -y python3-pip python3-dev python3-venv libmysqlclient-dev nginx curl nodejs npm
    ```

3.  **Crea un usuario para la aplicación:** Es una buena práctica de seguridad no ejecutar la aplicación como `root`.

    ```bash
    sudo adduser greeneconomics_user
    ```

### Paso 2: Despliegue del Código

1.  **Clona tu repositorio:** Cambia al nuevo usuario y clona tu proyecto desde Git.

    ```bash
    sudo -u greeneconomics_user -i
    git clone <tu-repositorio-git> /home/greeneconomics_user/TheGreenEconomics
    cd /home/greeneconomics_user/TheGreenEconomics
    ```

### Paso 3: Configuración del Entorno de Python

1.  **Crea y activa un entorno virtual:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Instala las dependencias de producción:**

    ```bash
    pip install -r requirements/production.txt
    ```

### Paso 4: Variables de Entorno

El proyecto usa `django-environ` para leer un archivo `.env`. Crearemos este archivo en la raíz del proyecto.

1.  **Crea el archivo `.env`:**

    ```bash
    nano .env
    ```

2.  **Añade las siguientes variables.** Reemplaza los valores de ejemplo con los tuyos.

    ```ini
    # .env (en /home/greeneconomics_user/TheGreenEconomics/.env)

    # General: Indica a Django que use la configuración de producción
    DJANGO_SETTINGS_MODULE=config.settings.production
    
    # Seguridad: ¡Genera una nueva clave secreta!
    # Puedes usar `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
    DJANGO_SECRET_KEY='<tu-nueva-clave-secreta-aqui>'
    
    # Hosts: El dominio de tu sitio web
    DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
    
    # Base de datos: La URL de conexión a tu base de datos MySQL de producción
    DATABASE_URL='mysql://user:password@localhost:3306/the_green_economics_prod'
    
    # Admin: Una URL no predecible para el panel de administración
    DJANGO_ADMIN_URL='secret-admin/'
    
    # Email: Configuración para el envío de correos
    DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    DJANGO_EMAIL_HOST=smtp.gmail.com
    DJANGO_EMAIL_PORT=587
    DJANGO_EMAIL_USE_TLS=True
    DJANGO_EMAIL_HOST_USER='tu-correo@gmail.com'
    DJANGO_EMAIL_HOST_PASSWORD='tu-contraseña-de-aplicacion-de-gmail'
    DJANGO_DEFAULT_FROM_EMAIL='The Green Economics <noreply@yourdomain.com>'
    DJANGO_SERVER_EMAIL='The Green Economics <noreply@yourdomain.com>'
    
    # Tailwind/NPM: Verifica la ruta en tu servidor con `which npm`
    NPM_BIN_PATH=/usr/bin/npm
    ```

### Paso 5: Configuración de la Base de Datos

1.  **Crea la base de datos y el usuario en MySQL:**

    ```sql
    -- Conéctate a MySQL como root
    CREATE DATABASE the_green_economics_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    CREATE USER 'greeneconomics_prod_user'@'localhost' IDENTIFIED BY 'una_contraseña_muy_segura';
    GRANT ALL PRIVILEGES ON the_green_economics_prod.* TO 'greeneconomics_prod_user'@'localhost';
    FLUSH PRIVILEGES;
    ```
2.  **Actualiza la variable `DATABASE_URL`** en tu archivo `.env` con los datos que acabas de crear.

### Paso 6: Comandos de Django para Producción

Con el entorno virtual activado, ejecuta los siguientes comandos para preparar tu aplicación.

1.  **Construye los assets de Tailwind CSS:**
    ```bash
    python manage.py tailwind install
    python manage.py tailwind build
    ```
2.  **Recolecta todos los archivos estáticos:**
    ```bash
    python manage.py collectstatic --noinput
    ```
3.  **Comprime los archivos estáticos:**
    ```bash
    python manage.py compress --force
    ```
4.  **Aplica las migraciones a la base de datos:**
    ```bash
    python manage.py migrate
    ```
5.  **Crea un superusuario:**
    ```bash
    python manage.py createsuperuser
    ```

### Paso 7: Configurar Gunicorn con Systemd

1.  **Crea el archivo de servicio de systemd:**

    ```bash
    sudo nano /etc/systemd/system/gunicorn.service
    ```

2.  **Pega la siguiente configuración:**

    ```ini
    [Unit]
    Description=gunicorn daemon for The Green Economics
    After=network.target

    [Service]
    User=greeneconomics_user
    Group=www-data
    WorkingDirectory=/home/greeneconomics_user/TheGreenEconomics
    
    # Carga las variables de entorno desde el archivo .env
    EnvironmentFile=/home/greeneconomics_user/TheGreenEconomics/.env
    
    ExecStart=/home/greeneconomics_user/TheGreenEconomics/venv/bin/gunicorn \
              --access-logfile - \
              --workers 3 \
              --bind unix:/run/gunicorn.sock \
              config.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Inicia y habilita el servicio Gunicorn:**

    ```bash
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    sudo systemctl status gunicorn
    ```

### Paso 8: Configurar Nginx como Reverse Proxy

1.  **Crea un archivo de configuración de Nginx para tu sitio:**

    ```bash
    sudo nano /etc/nginx/sites-available/the_green_economics
    ```

2.  **Pega la siguiente configuración.** Reemplaza `yourdomain.com` con tu dominio real.

    ```nginx
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/ {
            alias /home/greeneconomics_user/TheGreenEconomics/staticfiles/;
        }

        location /media/ {
            alias /home/greeneconomics_user/TheGreenEconomics/the_green_economics/media/;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }
    ```

3.  **Habilita el sitio, reinicia Nginx y ajusta el firewall:**

    ```bash
    sudo ln -s /etc/nginx/sites-available/the_green_economics /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    sudo ufw allow 'Nginx Full'
    ```

### Paso 9: Configurar HTTPS con Let's Encrypt

1.  **Instala Certbot:**

    ```bash
    sudo apt install certbot python3-certbot-nginx
    ```
2.  **Obtén e instala el certificado:**

    ```bash
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

¡Tu sitio ya debería estar en línea en `https://yourdomain.com`!

## Mantenimiento y Actualizaciones

Para actualizar tu aplicación en el futuro, sigue estos pasos:

```bash
# En el servidor, como greeneconomics_user
cd /home/greeneconomics_user/TheGreenEconomics
git pull
source venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compress --force

# Como root, para reiniciar el servicio
sudo systemctl restart gunicorn
```