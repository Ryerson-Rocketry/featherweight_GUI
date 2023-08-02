from time import sleep
import serial
import sys
# this is where python stores modules, yours could be different

sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")
port1 = "COM6" #Tracker
port2 = "COM9" #Groundstation
baud  = 115200


    
while True:

    try:
        radio1 = serial.Serial(port=port1,baudrate=baud,stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE) #Tracker
        radio2 = serial.Serial(port=port2,baudrate=baud,stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE) #Groundstation
        radio_connect = True
        break
    except Exception as e:
        print(e)
        radio_connect = False
        exit(-1)

print("Connected")
while(radio_connect == True):
    
    line = radio1.readline()
    radio1.flushInput()#pushes flowed input data out serial port 

    line2 = radio2.readline()
    radio2.flushInput()#pushes flowed input data out serial port 
    
    #print(line)
    ''' 
    if (line.startswith(b'@ GS_STAT')):
        line_gps_stat = radio.readline().strip().decode('utf-8').split(' ')
        print("GPS STAT BLOCK\n")
        print(line_gps_stat)
    
    #radio.close()
    #radio.open()
    #sleep(1)
    '''
    gps_w=radio1.write('set freq 915000000'.encode('utf-8'))
    radio1.flushInput()#pushes flowed input data out serial port
    gps_w = radio1.readline().strip().decode('utf-8').split(' ')
    print(gps_w)

    gps_w2=radio2.write('set freq 915000000'.encode('utf-8'))
    radio2.flushInput()#pushes flowed input data out serial port
    gps_w2 = radio2.readline().strip().decode('utf-8').split(' ')
    print(gps_w2)

    sleep(1)
    
            
        



sleep(1)
