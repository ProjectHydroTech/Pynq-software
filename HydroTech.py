from pynq.lib import Wifi
port = Wifi()
port.connect('eee-iot', '1Q2w3E4r5T6y')

import datetime
import decimal
import time
try:
    import pytz
except:
    pytz = None

from django.conf import settings

from pynq.overlays.base import BaseOverlay
from pynq_peripherals import ArduinoSEEEDGroveAdapter, PmodGroveAdapter
base = BaseOverlay('base.bit')
from pynq import gpio
from time import sleep

import threading

from datetime import datetime
import pytz

adapter=ArduinoSEEEDGroveAdapter(base.ARDUINO, D2='gpio', D3='gpio', D4='gpio', D5='gpio', D6='gpio', D7='grove_servo', A0='grove_light', I2C='grove_envsensor')
adapter1 = PmodGroveAdapter(base.PMODA, G1='grove_servo', G2='gpio', G3='gpio', G4='gpio')
LED0=adapter.D2
LED1=adapter.D3
LED2=adapter.D4
LED3=adapter.D5
PUMP=adapter.D6
SERVOEC = adapter.D7
LIGHTSENSOR = adapter.A0
ENVSENSOR = adapter.I2C
SERVOPH = adapter1.G1
FLOATLOW = adapter1.G2
FLOATHIGH = adapter1.G3
SWITCH = adapter1.G4

LED0.set_direction(0)
LED1.set_direction(0)
LED2.set_direction(0)
LED3.set_direction(0)
PUMP.set_direction(0)
FLOATLOW.set_direction(1)
FLOATHIGH.set_direction(1)
SWITCH.set_direction(1)

floatnowater = int
floatfullwater = int
dosingswitch = int
checkingec = int
ecmotor = int
dosingdone = int
checkingph = int
phmotor = int

floatnowater = 0
floatfullwater = 0
dosingswitch = 0
checkingec = 0
ecmotor = 0
dosingdone = 0
checkingph = 0
phmotor = 0

def clock():
    while True:
        
        tz_IN = pytz.timezone('Asia/Singapore') 

        datetime_IN = datetime.now(tz_IN)

        time = datetime_IN.strftime("%H:%M:%S")
        print(time)
        
        sleep(1);
        
def ledpump():
    while True:
        
        tz_IN = pytz.timezone('Asia/Singapore') 

        datetime_IN = datetime.now(tz_IN)
        
        hour = int(datetime_IN.strftime("%H"))
        minute = int(datetime_IN.strftime("%M"))
        second = int(datetime_IN.strftime("%S"))
        
        if hour < 9:
            LED0.write(0)
        else:
            LED0.write(1)

        if hour < 6 or (hour > 11 and hour < 18):
            LED1.write(0)
        else:
            LED1.write(1)

        if hour < 6 or (hour > 11 and hour < 18):
            LED2.write(0)
        else:
            LED2.write(1)

        if hour < 6 or (hour > 11 and hour < 18):
            LED3.write(0)
        else:
            LED3.write(1)
      
        if checkingec == 1 or checkingph == 1:
            PUMP.write(0)
        else:
            if (minute >= 0 and minute < 5) or (minute >= 20 and minute < 25) or (minute >= 40 and minute < 45):
                PUMP.write(0)
            else:
                PUMP.write(1) 
            
        sleep(1)
        
def floatsensors():

    while True:
        floatnowater = FLOATLOW.read()
        floatfullwater = FLOATHIGH.read()
        dosingswitch = SWITCH.read()
        
def servo():
    
    while True:

        tz_IN = pytz.timezone('Asia/Singapore') 

        datetime_IN = datetime.now(tz_IN)

        hour = int(datetime_IN.strftime("%H"))
        minute = int(datetime_IN.strftime("%M"))
        second = int(datetime_IN.strftime("%S"))

        if hour == 0 or dosingswitch == 0:
            checkingec = 1
        else:
            checkingec = 0

        if checkingec == 1:
            
            if (minute >= 0 and minute < 5) or (minute >= 15 and minute < 20) or (minute >= 30 and minute < 35) or (minute >= 45 and minute < 50):
                ecmotor = 1
                dosingdone = 0
                SERVOEC.set_angular_position(70)
            else:
                ecmotor = 0
                SERVOEC.set_angular_position(0)
        else:
            ecmotor = 0
            SERVOEC.set_angular_position(0)
            
        if checkingec == 0:
        
            if hour == 11 or hour == 23:
                checkingph = 1
            else:
                checkingph = 0

            if checkingph == 1:

                if minute >= 0 and minute < 30:
                    phmotor = 1
                    SERVOPH.set_angular_position(70)
                else:
                    phmotor = 0
                    SERVOPH.set_angular_position(0)
            else:
                phmotor = 0
                SERVOPH.set_angular_position(0)
            
        sleep(1)
        
def envsensor():

    while True:
        
        #read temperature
        temp = ENVSENSOR.read_temperature() 
        #read pressure
        pres = ENVSENSOR.read_pressure() 
        #read humidity
        humd = ENVSENSOR.read_humidity() 
        #read gas
        #gas = envsensor.read_gas()
        print(f"Temperature = {temp} °C, Pressure = {pres/100} hPa, Humidity = {humd} % r.H.")
        
        sleep(1)
        
def lightsensor():
        
    while True:

        print('percentage: %.2f%%' % LIGHTSENSOR.get_intensity())

        sleep(1)
        
clockthread = threading.Thread(target=clock)
ledpumpthread = threading.Thread(target=ledpump)
floatsensorsthread = threading.Thread(target=floatsensors)
servothread = threading.Thread(target=servo)
envsensorthread = threading.Thread(target=envsensor)
lightsensorthread = threading.Thread(target=lightsensor)

clockthread.start()
ledpumpthread.start()
floatsensorsthread.start()
servothread.start()
envsensorthread.start()
lightsensorthread.start()
