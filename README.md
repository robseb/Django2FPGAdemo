# Django2FPGAdemo

Complex web interfaces for controlling and monitoring embedded systems are seen as standard today. For low quantity systems is the development of this web application often really time-consuming.
To accelerate this process, it is important to use powerful web development frameworks with simple to use IDEs. One of this is the framework Django. That is used by a huge community on the desktop and if the same version of Django runs also on the embedded Linux it possible to benefit from them. Django has a comprehensive documentation with a lot of demos. These examples are often designed for typical cloud applications, like book shelf management.

The interesting part of embedded control and monitor web applications are the interaction between the web interface and Sensor- or FPGA-data. 
The following step by step guide shows how Django is able to log and present real sensor data in a web application. 

The solution used here is very easy to implement, but cannot be seen as a professional one.

The target of this demo is to show the accelerometer data of a Terasic DE10 Board inside a web browser.

The latest Version of Django with all necessary tools is pre-installed on [*rsYocto*](https://github.com/robseb/rsyocto), an embedded Linux System of Intel SoC-FPGAs and used as reference here.  


# Creating a new Django Project

* Boot up [*rsYocto*](https://github.com/robseb/rsyocto) by follwoing the [getting started Guide](https://github.com/robseb/rsyocto/blob/rsYocto-1.03/doc/guides/1_Booting.md)
* Setup Visual Studio Code Insider with [this instructions](https://github.com/robseb/rsyocto/blob/rsYocto-1.03/doc/guides/4_Python.md)
* Use inside Visual Studio Code Insider the integrated Linux Terminal with following command to create a new Django project with the name "DjangoSensor":
  ````python
  django-admin startproject DjangoSensor
  ````
  (Pic01)
 
 * **Note:** Use in the drop-down menu (blue arrow) the point "sh" to access the Linux Terminal. In case the point is not there press the “**+**”-icon to add it. 
 
# Testing the empty Django Project by accessing it with a web browser

* By default is the Django web server only reachable internally by the embedded linux
* To access Django applications within your network do following steps:
  1. Open the Django project settings file  (*settings.py*) with Visual Studio Code (as shown above) and allow everybody to connect with following lines:
    ````python
    ALLOWED_HOSTS = [
     '*'
   ]
   ````
  2. Use the next command to start the web server (here on Port 8181)
  ````bash
   python3 manage.py runserver 0:8181
  ````
  * **Note:** The default port 8080 is used by the *apache web server*
  
* Open  
 
