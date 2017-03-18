import serial
import time

import pyautogui

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
/dev/tty.usbmodem1421

# one of these is the bluetooth shield that is connected
# probably this one /dev/tty.CrowBTSlave-DevB

--------------------------------------------------------------------------


If we send 'M' to the Arduino it sends a reading of the gyroscope
If we send 'L' to the Arduino it turns the on board light LOW (off)
If we send 'H' to the Arduino it turns the on board light HIGH (on)

'''

#serial_speed = 115200 # for usb connection
#serial_port = '/dev/tty.usbmodem1421' # usb connection

#serial_port = '/dev/tty.HC-06-DevB' # bluetooth shield hc-06

serial_speed = 38400
serial_port = '/dev/tty.CrowBTSlave-DevB' # bluetooth shield?? need to test


if __name__ == '__main__':
    
    screen_size = pyautogui.size()
    pyautogui.FAILSAFE = False
    
    
    cur_mouse_coordinates = pyautogui.position()
    new_x_coordinate = (cur_mouse_coordinates[0])
    new_y_coordinate = (cur_mouse_coordinates[1])

    movement = False
    movement_prev = False
    
    move_amt_max = 20
    cnt = 0
    
    move_amt = 10   
    
    print ("conecting to serial port ...\n")
    ser = serial.Serial(serial_port, serial_speed, timeout=1)
        
    while (1):
        
        ser.write(b"H") #make built in Arduino light turn on
    
        #time.sleep(4)
        
        print ("recieving message from arduino ...\n") # data comes as a string
        
        ser.write(b"M") #send ready message for data
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
            print (data_list)
            
            cur_mouse_coordinates = pyautogui.position()
           
            if (movement_prev == True):
                move_amt = move_amt *1
                if move_amt > 20:
                    move_amt_max=20
            else:
                move_amt = 10
                move_amt_max = 20
            
            #look left
            if (data_list[0] < 80 ):  
                new_x_coordinate = (cur_mouse_coordinates[0] - move_amt)
                if (new_x_coordinate < 0):
                    new_x_coordinate = 0
                movement = True    
            
            #look right    
            if (data_list[0] > 110 ):  
                new_x_coordinate = (cur_mouse_coordinates[0] + move_amt)
                if (new_x_coordinate > screen_size[0]):
                    new_x_coordinate = screen_size[0]
                movement = True    
            
            #look up    
            if (data_list[1] > -37 ):  
                new_y_coordinate = (cur_mouse_coordinates[1] - move_amt)
                if (new_y_coordinate < 0):
                    new_y_coordinate = 0
                movement = True     
                
            #look down    
            if (data_list[1] < -50 ):  
                new_y_coordinate = (cur_mouse_coordinates[1] + move_amt)
                if (new_y_coordinate > screen_size[1]):
                    new_y_coordinate = screen_size[1]
                movement = True
                 
            pyautogui.moveTo(new_x_coordinate, new_y_coordinate)
            ser.write(b"L") #make built in Arduino ight turn off
            
            movement_prev = movement
            movement = False
            
  
        
print ("finish program and close connection!")