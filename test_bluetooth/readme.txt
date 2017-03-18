About the Files

REFERENCE URL:

from this website

https://dotslashnotes.wordpress.com/2013/09/21/how-to-setup-a-bluetooth-connection-between-arduino-and-a-pcmac/

=======================================================================================

test_bluetooth.pde

this is a sketch/program that runs in the "processing" language that runs on the computer
to test a bluetooth connection on arduino.  (see url)  

two boxes are drawn and if you click on them, one turns the arduino onboard light on
and the other turns it off.

for this to work a compatible sketch has to be installed on the arduino
——————————————————————————————————————————————————————————————————————————————————————

HC05_with_Computer_TEST

is the sketch that runs on the arduino, but didn’t work with the bluetooth shield that we are using.

-------------------------------------------------------------------------------------------
blue_tooth_slave.ino

this file works with our bluetooth shield, so this is the one that we use to test the lights, and the bluetooth connection.
-----------------------------------------------------------------------------------------------

To Run:

1)  upload sketch blue_tooth_slave.ino to Arduino

pair the arduino with computer through bluetooth (password 0000)

3) run test_bluetooth.pde

now you should be able to see the lights on the arduino go on and off when you click on the boxes.
