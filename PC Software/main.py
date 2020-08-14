# NOTE the user must ensure that the serial port and SERIELL_BAUDRATE are correct
# SERIELL_PORT = "/dev/ttyS80"
SERIELL_PORT = "COM13"
SERIELL_BAUDRATE = 115200
SERIELL_STARTZEICHEN = 'c'
#VERZÖGERUNG = 0.1 #wartezeit in Sekunden
TASTATUR_AUSLÖSERZEICHEN = 'f'

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    print("Verfügbare Schnittstellen:")
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyUSB*') # ubuntu is /dev/ttyUSB0
    elif sys.platform.startswith('darwin'):
        # ports = glob.glob('/dev/tty.*')
        ports = glob.glob('/dev/tty.SLAB_USBtoUART*')
    else:
        print("Unbekanntes Betriebssystem")
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except serial.SerialException as e:
            if e.errno == 13:
                raise e
            pass
        except OSError:
            pass
    return result


def trigger_routine(delayVal, key):
    time.sleep(delayVal)
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    print("Tastaturbefehl ausgelöst")


import keyboard
import serial
import time
import sys
print ()
print ()
#with open('config.conf') as file:
#    file_contents = file.readline(1)
#    print(file_contents)
filepath = 'config.conf'
with open(filepath) as fp:
   line = fp.readline()
   
   cnt = 1
   while line:
       line = line.strip()
       val =  line.split(" = ")
       print("Line {}: {}".format(cnt, line))
       if(cnt == 2):
           SERIELL_PORT = val[1]
       elif(cnt == 3):
           SERIELL_BAUDRATE = val[1]
       elif(cnt == 4):
           SERIELL_STARTZEICHEN = val[1]
       elif(cnt == 5):
           VERZÖGERUNG = float(val[1])
       elif(cnt == 6):
           TASTATUR_AUSLÖSERZEICHEN = val[1]
       line = fp.readline()
       cnt += 1
print(VERZÖGERUNG)
print(serial_ports())
print("Verbinden mit: " + SERIELL_PORT + " mit SERIELL_BAUDRATE: " + str(SERIELL_BAUDRATE))

ser = serial.Serial(SERIELL_PORT, SERIELL_BAUDRATE)

print ("Serial port verbunden")


while (1):
    val = ser.read()
    val = str(val.decode("utf-8"))
    if (val == SERIELL_STARTZEICHEN):
        print("Auslöser erhalten, Auslösung in " + str(VERZÖGERUNG) + " Sekunden")
        trigger_routine(VERZÖGERUNG, TASTATUR_AUSLÖSERZEICHEN)



ser.close



#   val = ser.read()
#   val = str(val.decode("utf-8"))
#   if (val == '\n'):
#        print(text)
#        text = "";
#    else:
#        #text = text + val.decode("utf-8") # change for Python3
#        text = text + val