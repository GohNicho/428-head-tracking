This folder has Arduino libraries that I've used
it is probably simpler to follow the diyhacking website's instructions than to figure out what these files are for.


***** This is the tutorial on installing and setting up the arduino software here (using Arduino 1.8.1 software)

https://diyhacking.com/arduino-mpu-6050-imu-sensor-tutorial/


references included in the Bluetooth_sensor_combo.ino bluetooth sketch.

==============================================================================================================

// SEE starter python info connecting to Arduino to mac in python
//https://gist.github.com/geoom/99d1407992364c3f9553

==============================================================================================================
// Bluetooth Connection TEST
//https://dotslashnotes.wordpress.com/2013/09/21/how-to-setup-a-bluetooth-connection-between-arduino-and-a-pcmac/
// uses processing program.  Sample code here, processing program connects successfully with this sketch
// clicking the squares turns onboard light on and off, when paired with arduino and password entered.
// to reinitialize pairing need to turn off arduino for a few seconds.  when light flashes open to pairing.

=================================================================================================================
// SETTING UP IMU **** INCLUDES WIRING DIAGRAM AND WHAT LIBRARIES WE NEED
//https://diyhacking.com/arduino-mpu-6050-imu-sensor-tutorial/

/*
 * OUR WIRING DIAGRAM for the coloured wires attached to MPU 6050 sensor.
 * 
 * Digital pin 2 -- BLUE Wire 
 * 3v3  -- RED Wire
 * GND (Ground) -- DARK PURPLE Wire
 * A4 -- BROWN Wire
 * A5 -- ORANGE Wire
 * 
 * 
 */
 
==============================================================================================================
//bluetooth shield
//https://www.creatroninc.com/product/hc-05-bluetooth-shield/?search_query=ardbe+001108&results=1

//working software from:
//https://www.elecrow.com/bluetooth-shield-masterslave-p-332.html

//slave code works, master doesn't seem to.  ??? used slave code here.
===============================================================================================================