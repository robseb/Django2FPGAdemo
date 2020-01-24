import subprocess

from BoardInteraction.models import ADCSensorReading, ADCchannel 

# For accessing the the Project settings
from django.conf import settings


# Singe shoot ADC Channel and write the value to the mySQLite Database 
def ReadADCchannel():
    for sensor in ADCchannel.objects.all():   
        adc_u = 0
        try: 
            adc_u = float(subprocess.check_output(['python3',settings.BASE_DIR+'/BoardInteraction/adcReadChannel.py',str(sensor.ch)],stderr=subprocess.STDOUT, timeout=None))
        except ValueError:
            adc_u = 0
            subprocess.call('echo Value Error ', shell=True)
        
        ADCSensorReading.reading = adc_u 
        subprocess.call('echo '+str(adc_u), shell=True)
        
        newreading = ADCSensorReading(reading= ADCSensorReading.reading)
        newreading.save()
        sensor.readings.add(newreading)
        sensor.save()
        
    return True