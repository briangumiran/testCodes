import serial
import usbtmc
import usb.core
import usb.util
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path

#Parameters
VMAX = 20;
VMIN = 4; #minimum voltage to produce data, otherwise will put the test in inf loop
NTERVAL = 0.2;

PORT = "COM4";
BAUDRATE = 9600;
TIMEOUT = 10;
PID = 25;

"""
To connect to the powersuppply, 
the USB Test and Measurement Class (usbtmc)
https://github.com/python-ivi/python-usbtmc

usbtmc in windows will require additional requirements such as 
pyUSB (can be installed using pyPI) and libusb*. 

*the libusb module in the usbtmc github page presents challenge in installation. 
driver installation of the device will be facilitated by this module:

1.  use the libusb as a device filter: 
Download (https://sourceforge.net/projects/libusb-win32/files/) the latest 
filter driver installer (libusb-win32-devel-filter-x.x.x.x.zip and 
then unzip, or libusb-win32-devel-filter-x.x.x.x.exe ).

2. If the installation is successful, the test program testlibusb-win.exe can see
the details of the connected device. take note of the idVendor and idProduct numbers

3. The Actual device driver is installed automatically (plug and play), if not, consult
the instructions for driver installation in https://sourceforge.net/p/libusb-win32/wiki/Home/

* to determine if the device driver is installed manually:
"Run the test program (testlibusb-win.exe) from the system's start menu. This program will verify the correct installation 
and print the descriptors of the USB devices accessible by the library."
"""

"""
establishing communication of PC and Power supply
"""

#device set configuration
dev = usb.core.find(idVendor = 0x0699, idProduct =0x0392)

# was it found?
if dev is None:
    raise ValueError('Device not found')

dev.set_configuration()
#usb.util.claim_interface(dev, interface)

#Connect Tektronix PW4305 DC power supply
instr = usbtmc.Instrument("USB::0x0699::0x0392::C011164::INSTR")

"""
For control of the Tektronix PWS4305, the command syntax is explained in:
http://research.physics.illinois.edu/bezryadin/labprotocol/PWS4205Manual.pdf
"""


#enable remote control
instr.write("SYSTEM:REMOTE")
print "enable remote control"

# config serial port 9600 baud
ser = serial.Serial()
ser.baudrate = BAUDRATE
ser.port = PORT
ser.timeout = TIMEOUT

#open serial
if (ser.is_open is not True):
		ser.open()
		print "SERIAL OPEN"

#order of parameters
para = ['PIEZOID', 'VOLTAGE', 'FREQUENCY', 'TEMP', 'CURRENT']

#create empty DataFrame
if(os.path.exists('piezotest.csv')):
	maindf = pd.read_csv('piezotest.csv',index_col = False)
else:
	maindf = pd.DataFrame(columns = para)

#start voltage sweep
for step in np.arange(VMIN,VMAX+NTERVAL,NTERVAL):
		
	#turn on voltage to activate piezo sensor
	instr.write("VOLTAGE "+str(step)+"V")
	instr.write("OUTPUT ON")
	
	#get test data, store in dict entry
	testdata = [{
		'PIEZOID': PID, 
		'VOLTAGE': float(instr.ask("MEASURE:VOLTAGE?")), 
		'FREQUENCY': float(ser.readline()), 
		'TEMP': float(ser.readline()), 
		'CURRENT' : float(instr.ask("MEASURE:CURRENT?"))
	}]
	print testdata[0].values()
	tempdf = pd.DataFrame(testdata,columns = para)
	maindf = maindf.append(tempdf, ignore_index = True)
	instr.write("OUTPUT OFF")
	
print "SERIAL CLOSED"
print maindf


maindf.to_csv('piezotest.csv', index = False)

	
	
	
	






