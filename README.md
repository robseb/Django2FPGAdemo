# Django2FPGAdemo

Complex web interfaces for controlling and monitoring of embedded systems are seen as standard today. For low quantity systems the development of this web application is often really time-consuming.
To accelerate this process, it is important to use powerful web development frameworks with simple to use IDEs. One of these is the framework Django. That is used by a huge community on desktop site and if the same version of Django also runs on the embedded Linux it is possible to benefit from their knowledge. Django has a comprehensive documentation with a lot of demos. These examples are often designed for typical cloud applications, like book shelf management.

The interesting part of embedded control and monitor web applications are the interaction between the web interface and Sensor- or FPGA-data. 
The following step by step guide shows how Django is able to log and present real sensor data in a web application. 

The solution used here is very easy to implement, but cannot be seen as a professional one.

The target of this demo is to show the accelerometer data of a Terasic DE10 Board inside a web browser.

The latest version of Django with all necessary tools is pre-installed on [*rsYocto*](https://github.com/robseb/rsyocto), an embedded Linux System of Intel SoC-FPGAs and used as reference here.  


# Creating a new Django Project

* Boot up [*rsYocto*](https://github.com/robseb/rsyocto) by following the [getting started Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.03/doc/guides/1_Booting.md)
* Setup Visual Studio Code Insider with [this instructions](https://github.com/robseb/rsyocto/blob/rsYocto-1.03/doc/guides/4_Python.md)
* Use inside Visual Studio Code Insider the integrated Linux Terminal with the following command to create a new Django project with the name "DjangoSensor":
  ````bash
  django-admin startproject DjangoSensor
  ````
  (Pic01)
 
 * **Note:** Use in the drop-down menu (blue arrow) the point "sh" to access the Linux Terminal. In case the point is not there press the “**+**”-icon to add it. 
 * Navigate with the Linux Terminal inside Visual Studio code to this project
  ````bash
  cd DjangoSensor
  ````
 
# Testing the empty Django Project by accessing it with a web browser

* By default the Django web server is only reachable internally by the embedded Linux
* To access Django applications within your network do following steps:
  1. Open the Django project settings file (*settings.py*) with Visual Studio Code (as shown above) and allow everybody to connect with the following lines:
    ````python
    ALLOWED_HOSTS = [
     '*'
   ]
   ````
  2. After any change of the settings file a migration of the project is necessary:
    ````bash
    python3 manage.py migrate 
    ````
    * The output of this command should look like this:
      ````bash
      root@cyclone5:~/DjangoSensor# python3 manage.py migrate
      Operations to perform:
      Apply all migrations: admin, auth, contenttypes, sessions
      Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying auth.0009_alter_user_last_name_max_length... OK
      Applying auth.0010_alter_group_name_max_length... OK
      Applying auth.0011_update_proxy_permissions... OK
      Applying sessions.0001_initial... OK
      ````
  3. Use the next command to start the web server (here on Port 8181)
    ````bash
     python3 manage.py runserver 0:8181
    ````
    * The output of this command should look like this:
      ````bash
      root@cyclone5:~/DjangoSensor# python3 manage.py runserver 0:8181
      Watching for file changes with StatReloader
      Performing system checks...

      System check identified no issues (0 silenced).
      January 18, 2020 - 15:35:44
      Django version 3.0.2, using settings 'DjangoSensor.settings'
      Starting development server at http://0:8181/
      Quit the server with CONTROL-C.
      ````
    * **Note:** The default port 8080 is used by the *Apache web server*
  
* Go with a web browser on a device inside this network (computer, tablet, smart-phone) to the URL:
    ````txt
     http://<iPv4-Address of the Board>:8181 
    ````
* If you see a *rocket lunch* your Django project works properly

  (Pic02)
 
* All **HTTP**-attaches are listed on the terminal as well


# Creating a new Django application to read and show accelerometer data
Every Django project requiers at least one application. We will build an App to readout the accelerometer (*Analog Devices ADXL345*) of a Terasic DE10-Standard- or Terasic DE10-Nano-Board and present the data in the web browser.

*  The following command adds a new app called "AccSensor" to the project.
  ````bash
  python3 manage.py startapp AccSensor
  ````
  * **Note:** Be sure that this command is executed inside the project-folder (*DjangoSensor/*)
* The project folder now contains the following structure:
  * All important files are marked
  
  (Pic03)
* Add this application to the Django project by adding the following line *settings.py* to the variable **INSTALLED_APPS**:
  ````python
  # Application definition
  INSTALLED_APPS = [
      'AccSensor.apps.AccsensorConfig', # Add this line 
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
  ]
  ````
  * **Note:** This is a connection to the function *AccsensorConfig()* that is located in the *"app.py"* file
  * Migrate the project again
   ````bash
   python3 manage.py migrate 
   ````

### Creating a model to store the accelerometer data into a mySQLite database
* Add the following python code to the model file (*DjangoSensor/AccSensor/models.py*)
  ````python
  '''
  Django accelerometer demo application - "models.py"
  '''
  from django.db import models

  #
  # Class for reading the accelerometer data
  #
  class AccSensorReading(models.Model):
      reading = models.CharField(max_length=20)           # Sensor value as Char Text Field type
      time    = models.DateTimeField(auto_now_add=True)   # Time stamp value

      def __unicode__(self):
          return self.reading

  # 
  # Class for connecting an Analog Devices ADXL345
  #
  class AccSensor(models.Model):
      name     = models.CharField(max_length=200)          # a name for the Sensor
      slug     = models.SlugField(unique=True)             # an unique working handler name
      readings = models.ManyToManyField(AccSensorReading)  # the sensor data object

      def __unicode__(self):
          return self.name
   
  ````
 
 ### Creating an Administrator page to allow an access to the database
 * Create an user who can do the login to the admin site. Run the following command:
    ````bash
    django-admin startproject createsuperuser
    ````
 * Enter an Username, an Email-Address and a Passwort
    ````bash
    Password: **********
    Password (again): *********
    Superuser created successfully.
    ```
 * Allow the Admin to access the accelerometer database models by adding the following code lines to the Admin-file (*DjangoSensor/AccSensor/Admin.py*)
   ````python
   '''
   Django accelerometer demo application - "admin.py"
   '''

   from django.contrib import admin
   from AccSensor.models import AccSensorReading, AccSensor

   # Allow access to all accelerometer data models 
   admin.site.register(AccSensor)
   admin.site.register(AccSensorReading)

   # Personalisation of the admin page
   admin.site.site_header = 'rsYocto'                               # Headline title           
   admin.site.index_title = 'Django Sensor Demo Administration'     # Sub-Headline title       
   admin.site.site_title = 'rsYocto'                                # HTML Headline
   ````
  
 ### Test 
   
   
