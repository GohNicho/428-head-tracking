About the Files
========================================================================================================================
bluetooth_sensor_read.py 

is the current working file to read the sensors
used with the arduino program BlueTooth_sensor_combo.ino

to use

1)  upload BlueTooth_sensor_combo.ino sketch to Arduino via USB cable
2)  pair arduino with pc
3)  run bluetooth_sensor_read.py  (uses python 3.6)


this program attempts to move the mouse cursor, via the sensor data.


LIBRARIES NEEDED

import serial
import time
import pyautogui

-------------------------------------------------------------------------------------------------------------------------
com_ports_list.py 

is a program that lists out the com ports on your system.  I’m not sure which com ports are used by windows with arduino, this we’ll have to test as I don’t have bluetooth on my windows machine

LIBRARIES NEEDED

import sys
import glob
import serial

------------------------------------------------------------------------------------------------------------------------
python_test_bluetooth.py

this program is a simpler version of bluetooth_sensor_read, there is no mouse positioning software.


LIBRARIES NEEDED

import serial
import time
------------------------------------------------------------------------------------------------------------------------

