import os
import glob
import time
import MySQLdb

# Database connection info
# Password is needed for it to work
# (host, user, password, database)
db = MySQLdb.connect("46.101.188.26","root","","brewsource")
# Used to execute commands
cursor = db.cursor()

# ID of the brewery of which the temperature is associated
breweryID = 1

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

def write_to_db():
    #insert to table
    try:
        cursor.execute("""INSERT INTO breweryTemperature(temperature, breweryID) VALUES (%s,%s)""",(read_temp(),breweryID))
        db.commit()
    except:
        db.rollback()
	
while True:
        # Print the read temperature to the console
	print(read_temp())
	# Insert the read temperature to the database
	write_to_db()
	# Pause for 3600 seconds (1 hour) until next reading
	time.sleep(3600)
