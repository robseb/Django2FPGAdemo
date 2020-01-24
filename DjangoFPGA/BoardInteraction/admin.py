'''
Django FPGA Interaction demo application  - "admin.py"
'''

from django.contrib import admin
from BoardInteraction.models import ADCSensorReading, ADCchannel, FPGAconfFiles

# Allow access to all ADC data models and FPGA configuration files inside the SQLite Database


admin.site.register(ADCchannel)
admin.site.register(ADCSensorReading)
admin.site.register(FPGAconfFiles) 

# Personalisation of the admin page
admin.site.site_header = 'rsYocto'                               # Headline title           
admin.site.index_title = 'Django Sensor Demo Administration'     # Sub-Headline title       
admin.site.site_title = 'rsYocto'                                # HTML Headline