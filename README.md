# PRUEBA SCRAPING RECETAS

Este es un proyecto de prueba de web scraping sobre el sitio web [https://www.recetasgratis.net/](https://www.recetasgratis.net/).

## Requisitos

- Python 3.12
- virtualenv (``pip install virtualenv``)
- Crear virtualenv (``virtualenv env``)
- Activar virtualenv (``source env/bin/activate``)
- Instalar requirements (``pip install -r requirements.txt``)
- Crear variable de entorno para Django (``export DJANGO_SETTINGS_MODULE=scraping_recetas.local_settings``)

Para este proyecto se han realizado los siguientes pasos:

### 1. Extracción de datos
Extraer los datos de las recetas de la página mediante un script en Python. Este script se encuentra en el archivo 
``scraping_recetas/extraccion_datos.py``. Para ejecutarlo abrimos la consola y escribimos el comando:

````
python extraccion_datos.py
````

Después de unos instantes, nos mostrará los datos obtenidos de las recetas.
La primera vez tardará unos minutos, ya que se ejecutan miles de peticiones a la página. Es por eso que se ha configurado
una caché en base de datos que, por motivos de tamaño, Git no deja subir al repositorio.

### 2. Almacenamiento de datos
Para almacenar estos datos en nuestra base de datos, se ha creado un script en Python que obtiene los datos de las recetas
del anterior script y crea instancias de los modelos de Django diseñados para almacenar la información. Esto solo se ha
tenido que ejecutar la primera vez, ya que si lo ejecutamos más veces duplicaremos datos en la base de datos.
Este script se encuentra en ``scraping_recetas/almacenamiento_datos.py`` y se ha ejecutado con el comando:

````
python almacenamiento_datos.py
````

### 3. API REST con los datos obtenidos

Después de obtener y almacenar estos datos, se ha creado una API REST con Django REST Framework para mostrarlos.
Para no tener que configurar el entorno local y ejecutarla, se ha hecho un deploy en Heroku: 
[https://prueba-scraping-recetas.herokuapp.com/](https://prueba-scraping-recetas.herokuapp.com/).
Esta API es explorable y documentada.


## Ejecución en local
Primero debemos tener activado el `virtualenv` tal y como se ha indicado en el paso 1. Una vez activado, primero ejecutaremos las migraciones de la base de datos:
```python
python manage.py migrate
```

Luego arrancamos el servidor:
````python
python manage.py runserver
````
Y listo, ya podemos acceder a `localhost:8000` y visualizar la API.

