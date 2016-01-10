# M3DB Django Interface
M3DB provides a lightweight Django app in order to view data an interact with the system.  Through this interface you can generate an abundance profile graph or view raw data that has been committed by the pipeline.  Further a REST API is available if you're a developer and would like to interact with M3DB.

##Installation
M3DB Django requires Django 1.7 or newer and Django Rest Framework 3.1.0.  It is designed to be served using nginx & gunicorn and the necessary gunicorn conf has been provided.

To create the necessary tables a standard:
python manage.py migrate

Then create a superuser:
python manage.py createsuperuser

This will suffice to get you up and running although you will manually need to create the Foreign Data Wrapper Tables if you want the Hive Data to be accessible to Django (usually not necessary).

##Usage
Point your web browser to the address & port you establish in nginx and login using the superuser credentials. You can create and delete other users using the register view.
