'''
Django FPGA Interaction demo application  - "admin.py"
'''

from django.http import Http404
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import ADCSensorReading
from subprocess import call

# use "pip install plotly" to add this package
from plotly.graph_objs import Scatter
from plotly.offline import plot 
import plotly.graph_objects as go


# For accessing the FPGA configuration
from subprocess import call

# For working with a file upload box 
from .forms import DocumentForm
from .models import FPGAconfFiles

# For accessing the the Project settings
from django.conf import settings

# import trigger function for reading the ADC
from BoardInteraction.services import ReadADCchannel
 

# 
# View the current ADC Channel Sensor data 
# FPGA LED and FPGA Fabric interface
#
def detail(request):

     # Handle file upload for the FPGA configuration file
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid(): 
            # Upload the File to the Database
            newdoc = FPGAconfFiles(docfile = request.FILES['docfile'])
            newdoc.save()
            # Write FPGA Configuration
            call('FPGA-writeConfig -f '+settings.BASE_DIR+"/"+newdoc.docfile.url, shell=True)
    else:
        form = DocumentForm() 

    # Load all stored FPGA configuration files
    try:
        FPGAconfigFiles = FPGAconfFiles.objects.all()
    except ADCSensorReading.DoesNotExist:   
        raise Http404("FPGA Configuration data does not exist")

    # Load the ADC Value database
    try:
        adcChvalue = ADCSensorReading.objects.all() 
    except ADCSensorReading.DoesNotExist:        
        raise Http404("ADC data does not exist")  # In case of an Error display an Error 404 Screeen

    ### Plot the ADC Values #####

    # We want to show the last 100 messages, ordered most-recent-last
    adcData = adcChvalue.order_by('-timestamp')[:100]

    y_data= []
    x_data= []

    for b in adcData:
        y_data.append(b.reading)
        x_data.append(b.timestamp)

    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name='Sensor Voltage',
                            line = dict(color='royalblue', width=4, dash='dashdot')))
    # Edit the layout
    fig.update_layout(title='Plot of recorded ADC data from a Soft IP-interface',
                    xaxis_title='Time (UTC)  [HH:MM:SS]',
                    yaxis_title='ADC Voltage (V)')

    # store the plot object 
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    # render the HTML template with all values
    return render(request, "BoardInteraction/DisplayTemplate.html", context=
    { 
        'plot_div': plot_div,           # Plot object 
        'obj':adcData,                  # ADC raw data 
        'documents': FPGAconfigFiles,   # FPGA Configuration files 
        'form': form                    # Upload File form
    })

#
# Called in case the user selected a FPGA Configuration 
# file from the Database list
#
def change_FPGAconfiguration(request):
    # <URL>/?subjectID=<Configuration file path>
    subjectID = request.GET.get("subjectID")

    call('FPGA-writeConfig -f '+settings.BASE_DIR+"/"+subjectID, shell=True)

    # Relaod the main app page again 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#
# Called in case the user selected the Bootloader FPGA Configuration 
# file from the Database list
#
def change_FPGAconfigurationBack(request):
    # <URL>/?subjectID=<Configuration file path>
    subjectID = request.GET.get("subjectID")

    call('FPGA-writeConfig -r', shell=True)

    # Relaod the main app page again 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#
# Function to turn FPGA LED 0 on 
#
def LED0_ON(request):
    # Turn FPGA LED0 on 
    call('FPGA-writeBridge -lw 20 -b 0 1 -b', shell=True)
    # Relaod the main app page again 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#
# Function to turn FPGA LED 0 off 
#
def LED0_OFF(request):
    # Turn FPGA LED0 off
    call('FPGA-writeBridge -lw 20 -b 0 0 -b', shell=True)
    # Relaod the main app page again 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#
# ADC Store data trigger function 
#
def ADCtrigger(request):
    ReadADCchannel()
    return HttpResponse('')




