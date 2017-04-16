import os
import glob
import time
import MySQLdb
import threading
from time import gmtime, strftime

# Database connection info
# Password is needed for it to work
host = "host"
user = "brewer"
password = "password"
table = "brewsource"
# Establish connection
db = MySQLdb.connect(host,user,password,table)
cursor = db.cursor()

# ID of the brewery of which the temperature is associated
breweryID = 3

# Command run to start reading from the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Directory of the temperature readings
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Get the readings
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

"""
Strip the lines read from read_temp_raw(), look for error
Get the temperature reading, divide it by 1000 to get Celsius temperature
"""
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def get_datetime():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def write_to_db():
    #insert to table
    threading.Timer(600.0, write_to_db).start() # Called every 600 seconds (10 min)
    try:
        cursor.execute("""INSERT INTO brewerytemp(temperature, owner, createdAt, updatedAt) VALUES (%s,%s, %s, %s)""",(read_temp(),breweryID, get_datetime(), get_datetime()))
        db.commit()
        
    except:
        db.rollback()

def connect_to_db():
    # Connect to the database
    db = MySQLdb.connect(host,user,password,table)
    # Used to execute commands
    cursor = db.cursor()
        
write_to_db()
