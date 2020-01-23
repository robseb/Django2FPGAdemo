# Django2FPGAdemo

 ![Alt text](pic/pic00.jpg?raw=true "Concept")

### Demonstration how build with the Django Framework a Management Web interface to interact with the FPGA or other Sensors and actuators

**This step by step guide shows how to log Sensor Data from a Soft-IP ADC interface within a SQLite-Database and how to plot this data on a web interface. In addition, it is demonstrated how to manage and change the FPGA Configuration with just a web browser.**

Complex web interfaces for controlling and monitoring of embedded systems are standard today. For low quantity FPGA applications, the development of this web application is often time-consuming. To accelerate this process, it is important to use powerful web development frameworks with simple to use IDEs such as Django. A huge community on desktop site uses that and if the same version of Django runs on the embedded Linux, it is possible to benefit from their knowledge. Django has a comprehensive documentation with many demos. However, these demos are for typical Desktop- and Cloud- applications and not for embedded applications. The imported part of embedded management web applications are the interaction between the web interface and Sensor- or FPGA-data.

To demonstrated that, is the ADC converter (*Analog Devices LTC2308*) of a *Terasic DE10-Nano*- or *DE10-Standard* Board (Intel Cyclon V SoC-FPGA) with an Soft-IP interface connected with the *Lightweight HPS to FPGA Bridge* to the Hard Processor System (HPS). 
On the ARM Cortex-A9 of the HPS run my embedded Linux, called [*rsYocto*](https://github.com/robseb/rsyocto), customized for Intel SoC-FPGAs. 

On *rsYocto* is the **Django Framework  (Version 3.01)** with all necessary components, like the **Apache-Webserver** and the **SQLite database**, are pre-installed. 

**This approach is the monitoring and management of embedded FPGA systems with a web interface**. This cannot be consider for low latency real-time applications. 
The advantage of the usage SQLite and HTTP with Linux is that these are standard in the desktop world. For these are for example API for connecting with cloud services available. 
<br>

![Alt text](pic/SequenceDiagram.jpg?raw=true "Sequence Diagramm of the Sensor Reading")
<br>

### Screenshot of the Web interface

![Alt text](pic/FinalWebinterface.PNG?raw=true "Screenshot of the final Web interface")


# Creating a new Django Project

* Boot up [*rsYocto*](https://github.com/robseb/rsyocto) by following the [getting started Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.03/doc/guides/1_Booting.md)
* Setup Visual Studio Code Insider with [this instructions](https://github.com/robseb/rsyocto/blob/rsYocto-1.03/doc/guides/4_Python.md)
* Use inside Visual Studio Code Insider the integrated Linux Terminal with the following command to create a new Django project with the name "DjangoFPGA":
  ````bash
  django-admin startproject DjangoFPGA
  ````
  ![Alt text](pic/pic01.jpg?raw=true "Django Development with Visual Studio Code")
 
 * **Note:** Use in the drop-down menu (blue arrow) the point "sh" to access the Linux Terminal. In case the point is not there press the “**+**”-icon to add it. 
 * Navigate with the Linux Terminal inside Visual Studio code to this project
  ````bash
  cd DjangoFPGA
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
      root@cyclone5:~/DjangoFPGA# python3 manage.py migrate
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
      root@cyclone5:~/DjangoFPGA# python3 manage.py runserver 0:8181
      Watching for file changes with StatReloader
      Performing system checks...

      System check identified no issues (0 silenced).
      January 18, 2020 - 15:35:44
      Django version 3.0.2, using settings 'DjangoFPGA.settings'
      Starting development server at http://0:8181/
      Quit the server with CONTROL-C.
      ````
    * **Note:** The default port 8080 is used by the *Apache web server*
  
* Go with a web browser on a device inside this network (computer, tablet, smart-phone) to the URL:
    ````txt
     http://<iPv4-Address of the Board>:8181/ 
    ````
* If you see a *rocket lunch* your Django project works properly 

  ![Alt text](pic/pic02.jpg?raw=true "Django Start screen")


* All **HTTP**-attaches are listed on the terminal as well


# Creating a new Django read and show data from the FPGA fabric and to manage FPGA configurations
Every Django project requiers at least one application. We will build an App to readout the Soft-IP ADC Interface  (*Analog Devices LTC2308*) of a Terasic DE10-Standard- or Terasic DE10-Nano-Board and present the data in the web browser.
As a secound feature it is also shown how to build with the Django Franework a Web application to configure the FPGA fabric and to mange all uploaded configuration files

*  The following command adds a new app called "BoardInteraction" to the project.
   ````bash
   python3 manage.py startapp BoardInteraction
   ````
  * **Note:** Be sure that this command is executed inside the project-folder (*DjangoFPGA/*)
* The project folder now contains the following structure:
  * All important files are marked
  
  ![Alt text](pic/pic03.jpg?raw=true "Django Folder structure")
  
* Add this application to the Django project by adding the following line *settings.py* to the variable **INSTALLED_APPS**:
  ````python
  # Application definition
  INSTALLED_APPS = [
      'BoardInteraction.apps.BoardinteractionConfig', # Add this line 
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
  ]
  ````
  * **Note:** This is a connection to the function *BoardinteractionConfig()* that is located in the *"app.py"* file
  * Migrate the project again
   ````bash
   python3 manage.py migrate 
   ````

### Creating a model to store the accelerometer data into a mySQLite database
* Add the following python code to the model file (*DjangoFPGA/BoardInteraction/models.py*)
  ````python
  '''
  Django FPGA Interaction demo application - "models.py"
  '''
  from django.db import models
  from datetime import datetime

  #
  # Class for reading a analog Sensor 
  #
  class ADCSensorReading(models.Model):
      reading = models.CharField(max_length=20)           # Sensor value as Char Text Field type 
                                                          # max 20 characters 
      timestamp = models.DateTimeField(default=datetime.now, db_index=True)    # Time stamp

      def __unicode__(self):
          return self.reading

  # 
  # Class for connecting a Analog Devices LTC LTC2308 ADC Channel
  #
  class ADCchannel(models.Model):
      name     = models.CharField(max_length=200)          # a name for the Sensor on the ADC Channel
      slug     = models.SlugField(unique=True)             # an unique working handler name
      readings = models.ManyToManyField(ADCSensorReading)  # the sensor data object
      ch       = models.IntegerField()                     # the used ADC Channel Number

      def __unicode__(self):
          return self.name

  ````
 
 ### Creating an Administrator page to allow an access to the database
 * Create an user who can do the login to the admin site. Run the following command:
    ````bash
    python3 manage.py createsuperuser
    ````
 * Enter an Username, an Email-Address and a Passwort
    ````bash
    Password: **********
    Password (again): *********
    Superuser created successfully.
    ````
 * Allow the Admin to access the accelerometer database models by adding the following code lines to the Admin-file (*DjangoFPGA/BoardInteraction/admin.py*)
   ````python
   '''
   Django FPGA Interaction demo application  - "admin.py"
   '''

   from django.contrib import admin
   from BoardInteraction.models import ADCSensorReading, ADCchannel

   # Allow access to all ADC data models inside the MySQLite Database
   admin.site.register(ADCchannel)
   admin.site.register(ADCSensorReading)

   # Personalisation of the admin page
   admin.site.site_header = 'rsYocto'                               # Headline title           
   admin.site.index_title = 'Django Sensor Demo Administration'     # Sub-Headline title       
   admin.site.site_title = 'rsYocto'                                # HTML Headline
   ````
   
 ### Testing the Administrator page
 * Save all open files
 * To generate a mySQLite database with these settings execude the following Linux Shell commands (*DjangoFPGA/*):
   ````bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py migrate --run-syncdb
   ````
 * Start the Django Server
   ````bash 
   python3 manage.py runserver 0:8181
   ```` 
 * Open the following URL with a web browser:
   ````txt
   http://<iPv4-Address of the Board>:8181/admin 
   ```` 
 * The Yocto Login Screen should appear:
   
  ![Alt text](pic/pic04.jpg?raw=true "Django Adim Login Screen")
 
 * Use your login credentials to login
 
  ![Alt text](pic/pic05.jpg?raw=true "Django Adim interface")
  
 * Here is the content of the database with the table "*Accsensor*" accessible
 * At this point it is possible to add the sensor data manuelly 
 (Hier ggf. manuel ein wert einfuegen)
 
  ### Presenting the Sensor Data and control the FPGA LED on a web page
  * To view this data in a graphic the Libary [plotly](https://plot.ly/python/) is used
    * That is by far the easiest way to implement such kind of UI-elemets to a web page, but really unefficient as well
  * To display live date of the accelerometer it is necessary to add some lines of code to the "*views.py*"-file on the App (*DjangoFPGA/AccSensor/views.py*):
  ````python
  '''
  Django accelerometer demo application - "views.py"
  '''

  from django.http import Http404
  from django.shortcuts import render, HttpResponse, HttpResponseRedirect
  from .models import AccSensorReading
  from subprocess import call

  # use "pip install plotly" to add this package
  from plotly.graph_objs import Scatter
  from plotly.offline import plot 

  from subprocess import call

  # 
  # View the current Sensor data 
  #
  def detail(request):
      try:
          accSensor = AccSensorReading.objects.all()     # Read the latest sensor object
      except AccSensorReading.DoesNotExist:        
          raise Http404("Accelerometer data does not exist")  # In case of an Error display an Error 404 Screeen

      # Show the template file "AccDisplayTemplate.html" with the current object
      #time.sleep(.500)

      # We want to show the last 50 messages, ordered most-recent-last
      accData = accSensor.order_by('-timestamp')[:50]

      i=0
      y_data= []
      x_data= []

      for b in accData:
          y_data.append(b.reading)
          x_data.append(i)
          i=i+1

      plot_div = plot([Scatter(x=x_data, y=y_data,
                          mode='lines', name='test',
                          opacity=0.8, marker_color='green')],
                 output_type='div',include_plotlyjs=False)

      return render(request, "AccSensor/AccDisplayTemplate.html", context=
      { 
          'plot_div': plot_div,
          'obj':accData    
      })

  ````
  * With this functions two events are declared, this allows to control the HPS with a push of the button LED 0:
    * Add them to "*views.py*"-file as well
    ````python
      def LED0_ON(request):
          # Turn FPGA LED0 on 
          call('FPGA-writeBridge -lw 20 -b 0 1 -b', shell=True)
          # Relaod the main app page again 
          return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

      def LED0_OFF(request):
          # Turn FPGA LED0 off
          call('FPGA-writeBridge -lw 20 -b 0 0 -b', shell=True)
          # Relaod the main app page again 
          return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

     ````

  * The *render*-function uses the "*DisplayTemplate.html*" HTML file to build the canvas of the web interface
  * Django only looks for this kind of template file in this folder structure: *<App>/templates/<App>/
  * That meens here, that this file must be located at here:
    ````txt
    DjangoFPGA/BoardInteraction/templates/BoardInteraction/DisplayTemplate.html
    ````
    * Creat the file with all folders with *Visual Studio Code Insider*
  * For building a simple UI add the following to the HTML file:
    ````html
    <!-- Django accelerometer demo application - AccSensor/AccDisplayTemplate.html -->
    <!DOCTYPE HTML>
    <html>
      <head>
        <!--Load the ploty Library script -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <meta charset="utf-8">
        </script>
        <title>rsYocto Django Demo</title>
      </head>
      <body>
        <!--Load the ploty UI-->
        {% autoescape off %}
        {{ plot_div }}
        {% endautoescape %}

        <!--Show the raw sensor data in a table-->
        <table>
          <tr>
            <th>Data</th>
            <th>author</th>
          </tr>
          {% for b in obj %}
          <tr>
            <td>{{ b.reading }}</td>
          </tr>
          {% endfor %}
        </table>

        <!--Create two push buttons to control the FPGA LED 0-->
        <button onclick="location.href='{% url 'scriptLED0N' %}'">LED 0 ON</button>
        <button onclick="location.href='{% url 'scriptLED0F' %}'">LED 0 OFF</button>
        <!-- {% url 'scriptLED0N' %} -> triggers jump to URL "<IPv4-Address>/scriptLED0N" by push event -->

      </body>
    </html>  
    ````

### Routing the URLs of the Application
* By default nothing will be routed to the front page of this application (http://<iPv4-Address of the Board>:8181/)
* On this URL Django will show an error screen:
    (Pic06)
* To link the front page to the "AccSensor"-App with the previosly created UI at the following lines of code in the global url configurations (*DjangoFPGA/DjangoSensor/urls.py*):
  ````python
  from django.contrib import admin
  from django.urls import path

  # Include the "AccSensor" App  
  from AccSensor import views

  # URL linkages of this project 
  urlpatterns = [
      path('', views.detail),                              # Front page -> linked to the "AccSensor" App 
      path('admin/', admin.site.urls),                     # /admin     -> Admin interface

      path('/LED0_ON',views.LED0_ON,name="scriptLED0N"),   # /LED0_ON   -> triggered by pushing the LED0 ON Button 
      path('/LED0_OFF',views.LED0_OFF,name="scriptLED0F"), # /LED0_OFF  -> triggered by pushing the LED0 OFF Button 
      # e.g. views.LED0_ON is the name of the viewer function  
      # With e.g. the name="scriptLED0N" the linkage is taken to the HTML event handler: '{% url 'scriptLED0N' %}'
  ]
  ````

 ### Testing the UI of the Appilcation 
 * Now all configurations of the user elements of these applications are done and it is time to test this state
 * Save all open files
 * Import the Python pip-package "plotly" that is used for the plotting of the data:
  ````bash
  pip install plotly
  ````
 * Execude the following Linux Shell commands again (*DjangoFPGA/*):
   ````bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py migrate --run-syncdb
   ````
 * Start the Django Server
   ````bash 
   python3 manage.py runserver 0:8181
   ```` 
 * Open the following URL with a web browser:
   ````txt
   http://<iPv4-Address of the Board>:8181/admin 
   ```` 
 * The front page should now look like this: 
   (Pic07)

 * With the admin interface it is possible to add some values to the plot

