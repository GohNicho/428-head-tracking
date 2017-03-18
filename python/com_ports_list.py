#source file is from
#http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python


'''

This program should list out the serial port names
to figure out what are the port names used to connect to mac (darwin), linux and windows.

port names are needed to connnect to bluetooth device, as once paired it 
is through a serial device (linux) or com port (windows)


how to detect the platform python is running on is also demonstrated.
we could possibly just hardcode the ports when we know what they are called on each machine for simplicity.

'''

import sys
import glob
import serial


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        print ('Windows detected -- takes a moment') # one of the ports must be the right one if this works.   I can't test don't have windows computer with bluetooth.
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        print ('Linux detected -- takes a moment')
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        print ('MAC detected-- takes a moment')
        ports = glob.glob('/dev/tty.*')  #ls /dev/tty.* on command line to see the same values
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    print(serial_ports())