import datetime
import random
from time import sleep
import serial


class Featherweight:
    # GPS data format as 'data': index
    gps_format: dict = {
        'Year': 3, 'Month': 4, 'Day': 5, 'Time': 6,
        'Device': 8, 'Name': 9,
        'Altitude': 11, 'Latitude': 13, 'Longitude': 15,
        'Horizontal Velocity': 17, 'Heading': 18, 'Upward Velocity': 19,
        'Fix Type': 21, 'Fix #': 23
    }

    _ser: serial.Serial

    def __init__(self, port: str, log_name: str = 'gps_log.txt'):
        self._data_log: list = []
        self._data_log2: list = []

        self._pos_list: list = []
        self._pos_list2: list = []

        self._log_name: str  = log_name

        #readFile()
        with open('gps_log.txt', encoding='utf8') as f:
            # read all contents of a file
            content = f.readlines()[-1]

            # seperate content into data needed (each name and its value)
            data = content.split(',')
            name = []
            value = []

            # split the data further into a name array and value array
            for i in data:

                splited = i.split(':')

                name.append(splited[0])
                value.append(splited[1])
            
            # making sure value for fix # is just an integer and does not include characters 
            num = ""
            for c in value[13]:
                if c.isdigit():
                    num = num + c
            value[13] = num

            # print each name and its value seperately
            specificData = [7,8,10,12,13]

            for j in specificData:
                name[j] = name[j][2:-1]
                value[j]=eval(value[j])

            # close file
            f.close()
        #self._ser.print(content)
        #print(content)
        #close file before appending starts

        self._log_file = open(self._log_name, 'a')
        self._datetime = datetime.datetime
   
        if port == 'mock':
            self._is_mock = True
            self._ser = None
            return

        self._is_mock = False
        self._ser = serial.Serial(
            port, 115200,  stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
        self._ser.flushInput()

    #def readFile():

    def read_gps(self, retries: int = 10) -> dict:
        """
        summary: 
                reads data that starts with @GPS_stat, parses and then logs it into an array for futture use
        
        parameters: 
            retries: (an int) number of times it waits to try and read serial data
        
        return: 
           a copy of the last logged string
        
        """
        for i in range(retries):
            if self._is_mock:
                data = self._mock()
                
                break

            line = self._ser.readline()

            if line.startswith(b'@ GPS_STAT'):
                data = self._parse_gps(line)
                break
        else:
            return None

        self._log_data(data)
        return self._data_log[-1].copy()
    
    def _log_data(self, data: dict) -> None:
            """
            
        summary: 
                appends the incoming data string into an data log array  as well as its position 
        
        parameters: 
           data: (a dict) the logged serial data         
        return:

           none
            
            
            """
    
            self._data_log.append(data)
            self._pos_list.append([float(data['Latitude']), float(data['Longitude'])])




    def _parse_gps(self, line: bytes) -> dict:
        """
        summary: 
                decodes serial string data using utf-8,  and splits into key elements needed  
        
        parameters: 
           line: (bytes)         
        return: 
          data 
        
        """
        # decode line as utf-8 and split by ' ' and remove empty strings
        line = line.decode('utf-8').split(' ')
        line = [x for x in line if x != '']
        data = {}

        for key, index in self.gps_format.items():
            data[key] = line[index]
        return data

    def last_pos(self, long_first=False) -> list:
        if len(self._data_log) == 0:
            return [0, 0]
        pos = self._data_log[-1].copy()
        pos = [float(pos['Latitude']), float(pos['Longitude'])]
        if long_first:
            pos.reverse()
        return pos

    @staticmethod
    def print_gps(data: dict) -> None:
        """
         prints in format:
        
        year/month/day time 
        device name

        ALT:altitude, 
        LAT: latitude, 
        LON longitude
        VEL: horizontal velocity,
         HDG: heading, 
         Z_VEL: upward velocity
        FIX: fix type, FIX_NUM: fix number
        """
        print('GPS:')
        print(
            f'{data["Year"]}/{data["Month"]}/{data["Day"]} {data["Time"]} :: {data["Device"]} {data["Name"]}')
        print(
            f'LAT: {data["Latitude"]}, LON: {data["Longitude"]}, ALT: {data["Altitude"]}')
        print(
            f'VEL: {data["Horizontal Velocity"]}, HDG: {data["Heading"]}, Z_VEL: {data["Upward Velocity"]}')
        print(f'FIX: {data["Fix Type"]}, FIX_NUM: {data["Fix #"]}')
        print('\n')

    def _mock(self) -> dict:
        """
        summary: 
            generates mock data within appropriate ranges for application testing purposes 
        
        parameters: 
            
        
        return: 
            return a mock gps data with a radndom altitude, latitude, and longitude offset        
        """
        # get current time
        now = datetime.datetime.now()

        if self.last_pos() != [0, 0]:
            lat = self.last_pos()[0] + random.uniform(-0.01, 0.01)
            lon = self.last_pos()[1] + random.uniform(-0.01, 0.01)
        else:
            lat = 43.65
            lon = -79.38

        return {
            'Year': str(now.year),
            'Month': str(now.month),
            'Day': str(now.day),
            'Time': now.strftime('%H:%M:%S'),

            'Device': 'MOCK_GPS',
            'Name': 'MOCK_NAME',

            # altitude in meters (0.1m)
            'Altitude': str(random.randint(700, 800) / 10),
            # Toronto latitude
            'Latitude': str(lat),
            # Toronto longitude
            'Longitude': str(lon),

            'Heading': str(random.randint(0, 360)),
            'Horizontal Velocity': str(random.randint(0, 100)),
            'Upward Velocity': str(random.randint(0, 100)),

            'Fix Type': str(random.randint(0, 3)),
            'Fix #': str(random.randint(0, 100))
        }
    def _close(self) -> None:
        """
            closes serial port
        
        """
        if self._ser is not None:
            self._ser.close()
        print("dumping and closing log file\n")

        self.dump()
        self._log_file.close()

    def dump(self):
        """
        adds a timestamp to the .txt log file in isoformat and writes number of iterations as well 
        
        """
        self._log_file.write(f'\n - log generated on {self._datetime.now().isoformat()}:\n')
        for i in self._data_log:
            self._log_file.write(f'{i.__str__()}\n')

    @property
    def pos_list(self) -> list:
        """
        returns the position of elements in the list of GPS data
        """
        return self._pos_list.copy()
   

    def __del__(self):
        self._close()

    def __repr__(self):
        return f'{"MOCK " if self._is_mock else ""}Featherweight Interface Object {f"@ {self._ser.port}" if self._ser is not None else ""}'



if __name__ == '__main__':
    from sys import argv

    args = argv[1:]

    if args == []:
        print("Error: No command line arguments given")
        print("Usage: featherweight_interface.py <port | mock>")
        exit(1)

    try:
        fw = Featherweight(args[0])
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    while True:
        data = fw.read_gps()
        if data is not None:
            fw.print_gps(data)

        sleep(1)
