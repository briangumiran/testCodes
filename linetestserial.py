import serial
import usbtmc
import usb.core
import usb.util

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
"""

#device set configuration
dev = usb.core.find(idVendor = 0x0699, idProduct =0x0392)

# was it found?
if dev is None:
    raise ValueError('Device not found')

#dev.set_configuration()
#usb.util.claim_interface(dev, interface)

#Connect Tektronix PW4305 DC power supply
instr = usbtmc.Instrument("USB::0x0699::0x0392::C011164::INSTR")
print(instr.ask("*IDN?"))



# # open serial port 9600 baud
# ser = serial.Serial(PORT,BAUDRATE)

# vin = raw_input("Set source voltage:")
# PORT = 'COM4'
# BAUDRATE = 9600
