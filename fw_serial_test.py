from time import sleep
import serial
import sys
# this is where python stores modules, yours could be different

sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")
port = "COM12"
baud  = 115200


    
while True:

    try:
        radio = serial.Serial(port=port,baudrate=baud,stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
        radio_connect = True
        break
    except Exception as e:
        print(e)
        radio_connect = False
        exit(-1)

print("Connected")
while(radio_connect == True):
    '''
    line = radio.readline()
    radio.flushInput()#pushes flowed input data out serial port 
    #print(line)
    
    if (line.startswith(b'@ GS_STAT')):
        line_gps_stat = radio.readline().strip().decode('utf-8').split(' ')
        print("GPS STAT BLOCK\n")
        #print(line_gps_stat)
    '''
    #radio.close()
    #radio.open()
    #sleep(1)

    gps_w=radio.write('set freq 915000000'.encode('utf-8'))
    radio.flushInput()#pushes flowed input data out serial port 
    gps_w = radio.readline().strip().decode('utf-8').split(' ')
    print(gps_w)
    sleep(1)
    
            
        



sleep(1)
