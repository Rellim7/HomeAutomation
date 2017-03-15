import RPi.GPIO as gpio
import time
from .models import *


gpio.setmode(gpio.BCM)

class controller(object):
    """
    send the door object though each function so that the whole program can handle multiple doors.
    This module only handles the door functions.
    """
    def __init__(self):
        self.relayPin = 17
        self.sensorPin = 4
        gpio.setup(self.sensorPin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.relayPin, gpio.OUT)
        return 

    def open(self):
        """
        opens the door.
        also will check if the door is already open.  If it is throw an error.
        """
        #gather the info about the door to do the checks
        #doorName = door.doorName
        #userName = user.userName

        status =1 # gpio.input(self.sensorPin)
        if status == 1:
            #print("opening")
            self.toggle(self.relayPin)
            return True
        else:
            #print("it's already open you idiot")
            return False
        

    def close(self):
        """
        closes the door.
        also will check if the door is already closed.  If it is throw an error.  Pulse the signal on then off.
        """
        #gather the info about the door to do the checks
        #doorName = door.doorName
        #userName = user.userName

        status = 1 #gpio.input(self.sensorPin)
        if status == 1:
            #print("closing")
            self.toggle(self.relayPin)
            return True
        else:
            #print("it's already closed you idiot")
            return False

    def forceClose(self):
        """
        closes the door.   This call is dangerous cause it could cause damage to anything in the way of the door.
        If the door is closed already this will throw a bloody tantrum.   It has to  hold the button down for X amount  of seconds.  Also checking to see if the door has made it to the
        closed state.
        """
        #gather the info about the door to do the checks
        #doorName = door.doorName
        #userName = user.userName

        status = gpio.input(self.sensorPin)
        if status == 1:
            #print("closing")
            gpio.output(self.relayPin,True)
            while status == 1:              
                status = gpio.input(self.sensorPin)
                time.sleep(12.2) #manual timing till i install sensor
                status = 0
            gpio.output(self.relayPin, False)
        else:
           # print("it's already closed you idiot")
        return status

    def toggle(self,pin):  # a "button Press"
        gpio.output(pin, True)
        time.sleep(0.2)
        gpio.output(pin, False)
        return

    def statusCheck(self):
        status = gpio.input(self.sensorPin)
        return status
