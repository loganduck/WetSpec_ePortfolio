import grovepi
from datetime import datetime
import sqlite3
from os import path
import math
import time

'''
WetSpec is used to monitor changing weather conditions in remote environments.

Review README for project specification.
'''

# SQLite database containing weather data.
database = 'weather.db'

# defines port allocations of sensors on GrovePi
light_sensor = 0
dht_sensor = 7
led_green = 2
led_blue = 3
led_red = 4

'''
[threshold] is compared to a calculated [resistance] to determine daytime.
When [resistance] is less than [threshold], enough light is present to be considered day.
'''
threshold = 10

# sets the pin mode on the various sensors on the GrovePi
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led_green,"OUTPUT")
grovepi.pinMode(led_blue,"OUTPUT")
grovepi.pinMode(led_red,"OUTPUT")

'''
Attempts to open a connection to the provided [database]. If the [database] path exists,
an attempt to a connection will be made and is returned, else the path to the [database]
does not exist or a connection could not be made and [None] is returned.
'''
def open(database):
    connection = None
    if path.exists(database):
        try:
            connection = sqlite3.connect(database)
        except sqlite3.Error:
            print("Unable to open connection to '{}'.".format(database))
    else:
        # path does not exist
        print("'{}' does not exist.".format(database))
    return connection

def insertData(connection, data):
    sql = "INSERT INTO data (date, time, temperature, humidity) VALUES (?,?,?,?)"
    try:
        connection.cursor().execute(sql, data)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

'''
Used to update the statuses of the LEDs where each parameter will either be 0 (off) or 1 (on).
'''
def update_led(g_val, b_val, r_val):
    grovepi.digitalWrite(led_green, g_val)
    grovepi.digitalWrite(led_blue, b_val)
    grovepi.digitalWrite(led_red, r_val)

'''
Attempts to convert the input [temperature] from celcius to fahrenheit. If the [temperature]
value is [None], 'error' is returned to indicate an error occured during the initial reading.
'''
def convertTemperature(temperature):
    if temperature is not None:
        # convert to fahrenheit
        return float((temperature * (9/5)) + 32)
    else:
        print('temperature value does not exist to convert.')
        return 'error'

'''
Attempts to convert the input [humidity] to one decimal place. If the [humidity] value is
[None], 'error' is returned to indicate an error occured during the initial reading.
'''
def convertHumidity(humidity):
    _h = ''
    if humidity is not None:
        return '{0:0.1f}'.format(humidity)
    else:
        print('humidity value does not exist to convert.')
        return 'error'

def main():
    # initialize LEDs off for program start
    update_led(0,0,0)

    while True:
        # get light sensor reading from port allocated with [light_sensor]
        light_sensor_value = grovepi.analogRead(light_sensor)

        # calculate resistance of sensor in K
        try:
            resistance = (float)(1023 - light_sensor_value) * 10 / light_sensor_value
            if resistance < threshold: # daytime
                try:
                    # open a connection to the database file
                    connection = open(database)
                    if (connection != None):
                        with connection:
                            # get current date
                            currDate = datetime.now().strftime('%m-%d-%y')

                            # get current time
                            currTime = datetime.now().strftime('%H:%M')

                            '''
                            gets and sets the temperature and humidity values by calling 
                            [grovepi.dht(dht_sensor, 0)]. The first parameter in the method is the
                            port for the sensor and the second parameter is the type of sensor.
                            0 for the type is the blue chip DHT and the white chip would use 1 for
                            its type.
                            '''
                            [temperature, humidity] = grovepi.dht(dht_sensor, 0) #0=blue chip

                            # calls the convert function for temperature
                            temperature = convertTemperature(temperature)

                            # calls the convert function for humidity
                            humidity = convertHumidity(humidity)

                            # creates a tuple to store the data for insertion
                            data = (currDate, currTime, temperature, humidity)
                            insertData(connection, data)
                            print('data: {} {} | T: {}, H: {}'.format(currDate, currTime, temperature, humidity))

                            if temperature > 60 and temperature < 85 and humidity < 80:
                                update_led(1,0,0)   # green on, blue off, red off
                            elif temperature > 85 and temperature < 95 and humidity < 80:
                                update_led(0,1,0)   # green off, blue on, red off
                            elif temperature > 95:
                                update_led(0,0,1)   # green off, blue off, red on
                            elif humidity > 80:
                                update_led(1,1,0)   # green on, blue on, red off
                    else:
                        print('Unable to establish a connection to the database.')
                except IOError:
                    print('An IOError has occurred.')
            else:
                print('{} {} | Current state is night. Sleeping for 30 minutes.')
                update_led(0,0,0) # turn LEDs off when dark
        except ZeroDivisionError:
            print('Unable to determine resistance value. A division by zero error has occured.')
        time.sleep(30*60)

if __name__ == '__main__':
    main()