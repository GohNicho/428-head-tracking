Bluetooth_Sensor_combo.ino

is the sketch that we load into the arduino to read the sensors
that works with the python code

python_sensor_read.py, python_test_bluetooth.py
------------------------------------------------------------------------------------------------------

HC-05 Bluetooth Shield Demo folder is the sketch libraries to connect to
the arduino via bluetooth.

The only one that I could get to work was the bluetooth slave example.

code is used in Bluetooth_Sensor_combo.ino
 
------------------------------------------------------------------------------------------------------

mpu6050Calibration

each mpu has specific manufacturing defects or characteristics.  the calibration sketch is ran on
the arduino to calibrate and adjust for these features.  We copy these values into our Bluetooth_Sensor_combo program.

------------------------------------------------------------------------------------------------------

6050 sensor

files needed to read and set up the sensor libraries for the arduino.
see the readme.txt file for more information on how to setup.

-------------------------------------------------------------------------------------------------------

