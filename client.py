import socket
import random
import threading
import time
import psutil

PORT = 8017
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
MAX_LENGTH_SIZE = 64

def find_range(variable, ranges):
    return next((r for r in ranges if r[0] <= variable <= r[1]), None)

ranges = {
    'var1': [(float('-inf'), 10), (20, 30), (40, 50)],
    'var2': [(5, 15), (25, 35), (50, 60)],
    'var3': [(float('-inf'), 5), (30, 40), (60, 70)]
}

attributes = {
    'var1': 25,
    'var2': 12,
    'var3': 65
}

# for var, value in variables.items():
#     matching_range = find_range(value, ranges_dict[var])
#     print(f"Variable {var} (value {value}) is in range {matching_range}")


qos = 0
freq = 1 # in seconds
stdmax = None
stdmin = None
cases = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



# this is a simulation tracking weather and temperature over time, server should result with about 7 cases, with 

#attributes
timem = 0 # int
weather = 0 # int # rainy, sunny, cloudy, snowy
temperature = 0 # float

weather_cycles = 6 # weather should be the same for at least 3 hours, which is 6 cycles

def update(): # this function is NOT optimized, as it will not be included in the library and is just a simple test
    global timem, weather, temperature, weather_cycles
    while True:
        time.sleep(1)
        timem += 30
        if timem == 1440: # 24 hours
            timem = 0
        if 1260 <= timem < 1440 or 0 <= timem <= 360:

            if weather_cycles == 6:
                weather_rand = random.randint(0, 3)
                match(weather_rand):
                    case 0:
                        weather = 0 # rainy
                        temperature = random.uniform(30, 60)
                    case 1:
                        weather = 2 # cloudy
                        temperature = random.uniform(20, 50)
                    case 2:
                        weather = 2 # cloudy
                        temperature = random.uniform(20, 50)
                    case 3:
                        weather = 3 # snowy
                        temperature = random.uniform(-13, 0)
                weather_cycles = 0
            else:
                weather_cycles += 1
                match(weather):
                    case 0:
                        temperature = random.uniform(30, 60)
                    case 2:
                        temperature = random.uniform(20, 50)
                    case 3:
                        temperature = random.uniform(-13, 0)
        
        elif 360 < timem < 1260:
            if weather_cycles == 6:
                weather_rand = random.randint(0, 3)
                weather_rand2 = random.randint(0, 2)
                if weather_rand2 == 1: # make sure we have a standard case
                    weather_rand = 1
                match(weather_rand):
                    case 0:
                        weather = 0 # rainy
                        temperature = random.uniform(60, 80)
                    case 1:
                        weather = 1 # sunny
                        temperature = random.uniform(90, 100)

                    case 2:
                        weather = 2 # cloudy
                        temperature = random.uniform(50, 70)
                    case 3:
                        weather = 3 # snowy
                        temperature = random.uniform(0, 32)
                weather_cycles = 0
            else:
                match(weather_rand):
                    case 0:
                        temperature = random.uniform(60, 80)
                    case 1:
                        temperature = random.uniform(90, 100)

                    case 2:
                        temperature = random.uniform(50, 70)
                    case 3:
                        temperature = random.uniform(0, 32)
                weather_cycles += 1


def send(msg):
    message = int(msg, 2).to_bytes((int(msg, 2).bit_length() + 7) // 8, byteorder='big')
    client.send(message)


thread = threading.Thread(target=update)
thread.start()   

def outlier(timem, weather, temperature):
    message = (str(timem) + "," + str(weather) + "," + str(temperature)).encode('utf-8')
    msg_length = str(len(message)).encode('utf-8')
    msg_length += b' ' * (MAX_LENGTH_SIZE - len(msg_length))
    client.send(msg_length)
    client.send(message)
    return

while True:
    time.sleep(3)
    outlier(timem, weather, temperature)
