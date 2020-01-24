'''
    Django FPGA Interaction demo application  - "sevices.py"
'''
import subprocess

from BoardInteraction.models import ADCSensorReading, ADCchannel 

# For accessing the the Project settings
from django.conf import settings

#
# Start a python application to read the ADC value 
# and write the value to a database
#
def ReadADCchannel():
    # For every activ ADC Channel 
    for sensor in ADCchannel.objects.all():   
        adc_u = 0
        # Start the Python Script "adcReadChannel.py" to read the ADC Channel
        try: 
            adc_u = float(subprocess.check_output(['python3',settings.BASE_DIR+'/BoardInteraction/adcReadChannel.py',str(sensor.ch)],stderr=subprocess.STDOUT, timeout=None))
        except ValueError:
            adc_u = 0
            subprocess.call('echo Value Error ', shell=True)
        
        # Write the value to the database
        ADCSensorReading.reading = adc_u 
        
        newreading = ADCSensorReading(reading= ADCSensorReading.reading)
        newreading.save()
        sensor.readings.add(newreading)
        sensor.save()
        
    return True
