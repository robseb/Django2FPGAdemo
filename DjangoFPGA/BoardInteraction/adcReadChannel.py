#!/usr/bin/env python
# coding: utf-8

'''
@disc:  ADC readout Sensor Test (Analog Devices LTC2308)
        Fast way over the virtual memory
           
@date:   21.01.2020
@device: Intel Cyclone V 
@author: Robin Sebastian
         (https://github.com/robseb)
'''
import os
import time
import math
import sys
# 
# This demo uses the python class "devmen" (https://github.com/kylemanna/pydevmem)
# be sure that this file is on the same directory 
#
import devmem

# the Lightweight HPS-to-FPGA Bus base address offset
HPS_LW_ADRS_OFFSET = 0xFF200000 

# LTC2308 Address offset
ADC_ADDRES_OFFSET = 0x40

# Register set of the LTC2308
ADC_CMD_REG_OFFSET  = 0x0
ADC_DATA_REG_OFFSET = 0x4


### FIFO Convention Data Size for average calculation
FIFO_SIZE = 255 # MAX=1024 

if __name__ == '__main__':
   
    # Read selcted ADC Channel as input argument [1]
    # python3 adcReadChannl <CH> 
    
    ch = 0
    
    ch_selet = str(sys.argv[1])
    try: 
        ch = int(ch_selet)
    except ValueError:
        ch = 0

    if(not(ch >=0 and ch < 6)):
        ch = 0
    
    # open the memory Access to the Lightweight HPS-to-FPGA bridge
    #                  (Base address, byte length to acceses, interface)
    de = devmem.DevMem(HPS_LW_ADRS_OFFSET, ADC_ADDRES_OFFSET+0x8, "/dev/mem")
    

    # Set meassure number for ADC convert
    de.write(ADC_ADDRES_OFFSET+ADC_DATA_REG_OFFSET,[FIFO_SIZE])
    # Enable the convention with CH0 
    de.write(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET, [(ch <<1) | 0x00])
    de.write(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET, [(ch <<1) | 0x01])
    de.write(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET, [(ch <<1) | 0x00])
    
    timeout = 300 #ms
    # Wait untis convention is done or timeout
    while (not(timeout == 0)):
        
        if(de.read(ADC_ADDRES_OFFSET+ADC_CMD_REG_OFFSET,1)[0] & (1<<0)): 
            break

        timeout = timeout -1
        time.sleep(.001) # delay 1ms 

    # Avarage FIFO values
    rawValue = 0
    for i in range(FIFO_SIZE): 
        rawValue = rawValue+ (de.read(ADC_ADDRES_OFFSET+ADC_DATA_REG_OFFSET,1))[0]
    
    value = rawValue / FIFO_SIZE

    # Convert ADC Value to Volage
    volage = round(value/1000,2)
    print(str(volage))
    
