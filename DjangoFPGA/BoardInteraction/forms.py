'''
Django FPGA Interaction demo application - "form.py"
'''
from django import forms

# 
# Build the Upload File Box for selecting 
# a FPGA configuration file 
#
class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a ".rbf"- FPGA configuration file',
        help_text='Click Upload to save the file and configure the FPGA fabric'
    )