import serial
import time
'''
#installing serial library python if not installed howto
#http://stackoverflow.com/questions/33267070/no-module-named-serial

--------------------------------------------------------------------------
Purpose:  


this program shoud make the onboaard arduino light turn on and off 10 times
when arduino sketch is listening for 'H' and 'L' characters.  (if all goes well)

trying to prove that connection was successful


need to pair arduino before running this program.
current password is '0000' enter when asked


Serial port parameters how to get on mac

Enter in command window :  ls /dev/tty.*

listing is on my machine:  (4 possible devices)

/dev/tty.Bluetooth-Incoming-Port	  /dev/tty.CrowBTSlave-DevB
/dev/tty.Bluetooth-Modem		/dev/tty.CrowBTSlave-DevB-1

# one of these is the bluetooth shield that is connected
# probably this one /dev/tty.CrowBTSlave-DevB

--------------------------------------------------------------------------


If we send 'M' to the Arduino it sends a reading of the gyroscope
If we send 'L' to the Arduino it turns the on board light LOW (off)
If we send 'H' to the Arduino it turns the on board light HIGH (on)

'''


serial_speed = 38400
#serial_port = '/dev/tty.HC-06-DevB' # bluetooth shield hc-06
serial_port = '/dev/tty.CrowBTSlave-DevB' # bluetooth shield?? need to test

if __name__ == '__main__':
    
    print ("conecting to serial port ...\n")
    ser = serial.Serial(serial_port, serial_speed, timeout=1)
        
    while (1):
        
        ser.write(b"H") #make built in light turn on
    
        #time.sleep(4)
        
        ser.write(b"M") #send ready message for data
    
        print ("recieving message from arduino ...\n") # data comes as a string
        data = ser.readline()
    
        text = str(data)
        text = text[2:-5] # strip off leading and trailing cr/lf
        
        data_list = text.split(",")  #separate string into separate items by the comma.
        
        #convert the string to a list of floats.  (drop errors, from the occasional bad data/ slow connections)
        
        try:
            for i in range(len(data_list)):
                data_list[i] = float(data_list[i])
        except ValueError:
            print ("Getting Ready, Data Error")
            continue
        else:
            print("x_value, y_value, z_value:")  # yaw, pitch and roll
            for i in range (0,3):
                print (data_list[i])
            
            print("ax_value, ay_value, az_value:")  # accel_x, accel_y, accel_z
            for i in range (3,7):
                print (data_list[i]) 
                
                               
            ser.write(b"L") #make built in light turn off
  
        
print ("finish program and close connection!")