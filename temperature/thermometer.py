import os
import glob
import time
import threading
from time import gmtime, strftime
from pymongo import MongoClient

# Database connection info
# Password is needed for it to work
host = "46.101.188.26"
port = ""
user = "brewer"
password = ""
database = "brewsource"
authSrc = "admin"

# ID of the brewery of which the temperature is associated
batchID = "592c5404f9182cd80c389227"

"""
MONGO
"""
# Define the client with user, password, host:port, database and authentication source
# "mongodb://user:password@HOST:PORT/database?authSource=authenticationDatabase"
client = MongoClient("mongodb://" + user + ":" + password + "@" + host + ":" + port + "/" + database + "?authSource=" + authSrc + "")
# set the database to be used
db = client.brewsource

# Command run to start reading from the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Directory of the temperature readings
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

"""
Get the temperature readings
"""
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
"""
Get the current datetime
"""
def get_datetime():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

"""
Write the temperature, owner, dates to the collection (table)
"""
def write_to_db():
    # insert into collection
    threading.Timer(600.0, write_to_db).start() # Called every 600 seconds (10 min)
    try:
        db.brewerytemp.insert_one(
            {
                "temperature": read_temp(),
                "owner": batchID,
                "createdAt": get_datetime(),
                "updatedAt": get_datetime()
            }
        )
        print 'great success'

    except Exception, e:
        print str(e)

"""
Connection to the database
"""
def connect_to_db():
    # Connect to the DB
    # Define the client with user, password, host:port, database and authentication source
    client = MongoClient("mongodb://" + user + ":" + password + "@" + host + ":" + port + "/" + database + "?authSource=" + authSrc + "")
    # set the database to be used
    db = client.brewsource

# Run the write method
write_to_db()
