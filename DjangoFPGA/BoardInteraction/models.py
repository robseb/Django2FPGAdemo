'''
Django FPGA Interaction demo application - "models.py"
'''
from django.db import models
from datetime import datetime

#
# Class for reading a analog Sensor 
#
class ADCSensorReading(models.Model):
    # Sensor value as Char Text Field type   
    reading = models.FloatField()         
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
    ch       = models.IntegerField() # the used ADC Channel Number

    def __unicode__(self):
        return self.name

# 
# FPGA .rbf Configuration File Database
# 
class FPGAconfFiles(models.Model):
    docfile = models.FileField(upload_to='FPGAconfigDatabase/%Y/%m/%d')      # local storge folder  
    timestamp = models.DateTimeField(default=datetime.now, db_index=True)    # Time stamp