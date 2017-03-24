import serial
import time

from  analyzer import *  
from collections import deque

import pyautogui

import os


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


def running_average (value_queue, angles, maxQueueSize):
    
    '''
    return the average of all of the values in the queue

    the queue is assumed to be a list of lists, with in our case 3 elements per item                

    each item is a triple of numbers made up of[x_angle, y_angle, z_angle]

    '''    
    result=angles
    
    value_queue.append(angles)
    sizeOfQueue = len(value_queue) #current size of queue.
    
    if sizeOfQueue == 1:  #skip any calculations
        return result    
    
    if sizeOfQueue > maxQueueSize:  #remove oldest item
        value_queue.popleft()
        sizeOfQueue = len(value_queue)
    
    for i in range(len(value_queue)):  #sum up the queue    
        for j in range(len(value_queue[i])):
            result[j] = result[j] + value_queue[i][j]
    
    for j in range(len(result)):  #get average
        result[j] = result[j] / sizeOfQueue
        
    return result #return the average of the values on the queue       
    
    
#----------------------------------------------------------------------------------    

if __name__ == '__main__':
    
    first_name = input("What is your first_name? ")
    last_name = input ("What is your last_name? ")
    
    print ("Hello", first_name, last_name, ".")
    
    ###########################################
    
    # change user name before running
    system = HTSystem()
    system.add_client( first_name, last_name ) 
    ###########################################   
    
    
    #os.system("say 8, 9, 2, 55, 127, 69, 80, 223, 6, 88, 512, 44, 3, 1")
    
    #os.system("say Hi, welcome to the pizzeria. Would you like to order a pizza, or sides?")
    #os.system("say What size? Small, medium, or large?")
    #os.system("say Okay, would you like to order sides as well?")
    #os.system("say okay, your order is being processed.")
    #os.system("say Which side? Wings, or potato wedges?")
    #os.system("say Okay, would you like to order a pizza as well?")
        
    screen_size = pyautogui.size()
    pyautogui.FAILSAFE = False
    
    heading_flag = False # heading flag == False when local direction isn't measured at start.
    
    cur_mouse_coordinates = pyautogui.position()
    new_x_coordinate = (cur_mouse_coordinates[0])
    new_y_coordinate = (cur_mouse_coordinates[1])
    
    ###########################################
    
    #set to false to stop cursor movment
    move_cursor_flag = False
    
    #to stop local printing set to false
    local_printing = False
    
    ###########################################

    movement = False
    movement_prev = False
    
    move_amt_max = 20
    cnt = 0
    
    move_amt = 10 
    
    heading = [0,0,0]  #the heading that the person is originally facing, need to update
    
    calibrate_size = 100 # the number of values averaged for calibration.
    
    gest = "None" #The current value of the gesture that was performed
    
    value_queue = deque([])  #the queue of the sizeOfQueue most recent readings  (sizeofQueue <= Max_size)
    
    maxQueueSize = 10  # max number of elements in the queue
    
    print ("conecting to serial port ...\n")
    ser = serial.Serial(serial_port, serial_speed, timeout=1)
    
    
    
    
    while True:
        
        ser.write(b"H") #make built in Arduino light turn on
    
        #time.sleep(4)
        
        
        if local_printing:
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
            if (heading_flag == False ):  #get starting orientation of person/hat
                
                print ("getting starting heading")
                
                heading = running_average(value_queue, data_list, 100)
                #value_queue.clear()
                heading_flag = True 
                print ("heading aligned.")   
            
            if local_printing:
                print("x_value, y_value, z_value:")  # yaw, pitch and roll            
                #data_list = running_average(value_queue, data_list, 100)
                print (data_list)
                print (heading)
            
            cur_mouse_coordinates = pyautogui.position()
           
            if (movement_prev == True):
                move_amt = move_amt *1 #scale speed of mouse movement not using right now
                if move_amt > 20:
                    move_amt_max=20
            else:
                move_amt = 10
                move_amt_max = 20
            
            #look left
            if (data_list[0] < (heading[0] -20) ):  
                new_x_coordinate = (cur_mouse_coordinates[0] - move_amt)
                if (new_x_coordinate < 0):
                    new_x_coordinate = 0
                movement = True
                gest = "left"  
                  
            
            #look right    
            if (data_list[0] > (heading[0] + 20) ):  
                new_x_coordinate = (cur_mouse_coordinates[0] + move_amt)
                if (new_x_coordinate > screen_size[0]):
                    new_x_coordinate = screen_size[0]
                movement = True
                gest = "right"    
            
            #look up    
            if (data_list[1] > (heading[1] + 15) ):  
                new_y_coordinate = (cur_mouse_coordinates[1] - move_amt)
                if (new_y_coordinate < 0):
                    new_y_coordinate = 0
                movement = True     
                gest = "up"
                
            #look down    
            if (data_list[1] < (heading[1] -15) ):  
                new_y_coordinate = (cur_mouse_coordinates[1] + move_amt)
                if (new_y_coordinate > screen_size[1]):
                    new_y_coordinate = screen_size[1]
                movement = True
                gest ="down"
            
            
            if move_cursor_flag:     
                pyautogui.moveTo(new_x_coordinate, new_y_coordinate)
            ser.write(b"L") #make built in Arduino light turn off
            
            if movement == False:
                gest = "None"
                
            system.read(data_list, gest)
            
            if local_printing:
                print (gest)
            
            movement_prev = movement
            movement = False
            
  
        
print ("finish program and close connection!")