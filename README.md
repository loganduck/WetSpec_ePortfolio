# WetSpec 
WetSpec is a project from _CS 350 Emerging Sys Arch & Tech_ that was created to monitor changing weather conditions in remote environments. This repo was created to add the project to CS499 ePortfolio.

### Prerequisites
* [Raspberry Pi 3 B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)  
* [GrovePi+ Starter Kit](https://www.seeedstudio.com/GrovePi-Starter-Kit-for-Raspberry-Pi-A-B-B-2-3-CE-certified.html)  

### Parts used from kit:
* GrovePi+
* Temp&Humi Sensor (DHT)
* Green LED
* Blue LED
* Red LED
* Light Sensor
* Cables (x5)

### Additional items needed:
* Monitor with HDMI input
* HDMI cable
* 2.5A micro USB power supply
* USB keyboard and mouse
* Micro SD card with [N00BS](https://www.raspberrypi.org/documentation/installation/noobs.md) installed

## Specifications
### Light Sensor:
Temperature and humidity is only monitored during daytime hours and daytime conditions; sensor readings must not be recorded outside these times or conditions, or there might risk skewing the data the platform collects.

### Database
* File name: **weather.db**  
* Table name: **data**  
* Table schema:  
```
_id INTEGER NOT NULL PRIMARY KEY,
date TEXT NOT NULL,
time TEXT NOT NULL,
temperature TEXT NOT NULL,
humidity TEXT NOT NULL
```

### Frequency of Data:
During operating hours, readings are taken once every 30 minutes and stored in the `data` table in `weather.db`.

### Output Visual Using LEDs:
* Green LED lights up when the last conditions are: **temperature > 60 and < 85, and humidity is < 80%**
* Blue LED lights up when the last conditions are: **temperature > 85 and < 95, and humidity is < 80%**
* Red LED lights up when the last conditions are: **temperature > 95**
* Green and Blue LED light up when the last conditions are: **humidity > 80%**

## Installation  
Specific modifications must be made to successfully operate the GrovePi.

It is important to carefully follow this [tutorial](https://www.dexterindustries.com/grovepi-tutorials-documentation/) to configure software and update firmware so the RPi can successfully communicate with the Grove.

From the Raspberry Pi Terminal:

1. **Update** your system's package list using:  
`sudo apt update`
2. **Upgrade** all your installed packages to their latest versions with:  
`sudo apt full-upgrade`
3. **Install** SQLite3 for data storage:  
`sudo apt-get install sqlite3`

## Running WetSpec
1. Connect the Grove to RPi
2. Add sensors to the following ports:  
Light Sensor = 0  
Temp&Hum Sensor (DHT) = 7  
Green LED = 2  
Blue LED = 3  
Red LED = 4  
3. Connect USB keyboard and mouse to RPi.  
4. Connect HDMI to RPi and monitor.  
5. Connect power supply to Raspberry Pi and power on
6. Create a folder called `WetSpec` in `~/Dexter/GrovePi/Software/Python/` and clone repository.
7. Open `WetSpec.py` and run it. There should be no errors if everything was followed in the [tutorial](https://www.dexterindustries.com/grovepi-tutorials-documentation/) above. As long as it is daytime, let the system run for a a few hours.
8. End the program and view data in `weather.db`.

## Viewing data
1. Open Terminal
2. Enter the following:
```
cd /Dexter/GrovePi/Software/Python/WetSpec/
sqlite3 weather.db
.headers on
SELECT * FROM data;
```
