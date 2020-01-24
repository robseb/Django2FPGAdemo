"""DjangoFPGA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Include the "BoardInteraction" App  
from BoardInteraction import views

# URL linkages of this project 
urlpatterns = [
    
    # UI 
    path('', views.detail,name="main"),                 # Front page -> linked to the "BoardInteraction" App 
    path('admin/', admin.site.urls),                    # /admin     -> Admin interface

    # HPS LED 0 
    path('LED0_ON',views.LED0_ON,name="scriptLED0N"),   # /LED0_ON   -> triggered by pushing the LED0 ON Button 
    path('LED0_OFF',views.LED0_OFF,name="scriptLED0F"), # /LED0_OFF  -> triggered by pushing the LED0 OFF Button 

    # e.g. views.LED0_ON is the name of the viewer function  
    # With e.g. the name="scriptLED0N" the linkage is taken to the HTML event handler: '{% url 'scriptLED0N' %}'

    # FPGA Configuration 
    path('FPGA',views.change_FPGAconfiguration,name="scriptFPGAconf"),
    path('BOOTFPGA',views.change_FPGAconfigurationBack,name="BootloaderFPGAconf"),

    # ADC Sensor Trigger
    path('ADCtrigger',views.ADCtrigger,name="scriptADCtrigger")
]
