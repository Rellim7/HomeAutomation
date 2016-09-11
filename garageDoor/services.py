import RPi.GPIO as gpio
import time
from .models import *


gpio.setmode(GPIO.BCM)

class controller():
    """
    send the door object though each function so that the whole program can handle multiple doors.
    This module only handles the door functions.
    """
    def __init__():
        return

    def open(door, user):
        """
        opens the door.
        also will check if the door is already open.  If it is throw an error.
        """
        #gather the info about the door to do the checks
        doorName = door.doorName
        userName = user.userName
        sensorPin = door.sensorPin
        relayPin = door.relayPin

        gpio.setup(sensorPin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(relayPin, gpio.OUT)

        status = gpio.input(sensorPin)
        if status == 0:
            print("opening")
            trigger(relayPin)
        else:
            print("its already open you idiot")

        return

    def close(door, user):
        """
        closes the door.
        also will check if the door is already closed.  If it is throw an error.  Pulse the signal on then off.
        """
        #gather the info about the door to do the checks
        doorName = door.doorName
        userName = user.userName
        sensorPin = door.sensorPin
        relayPin = door.relayPin

        gpio.setup(sensorPin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(relayPin, gpio.OUT)

        status = gpio.input(sensorPin)
        if status == 1:
            print("closing")
            trigger(relayPin)
        else:
            print("its already closed you idiot")

        return status

    def forceClose(door, user):
        """
        closes the door.   This call is dangerous cause it could cause damage to anything in the way of the door.
        If the door is closed already this will throw a bloody tantrum.   It has to  hold the button down for X amount  of seconds.  Also checking to see if the door has made it to the
        closed state.
        """
        #gather the info about the door to do the checks
        doorName = door.doorName
        userName = user.userName
        sensorPin = door.sensorPin
        relayPin = door.relayPin

        gpio.setup(sensorPin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(relayPin, gpio.OUT)

        status = gpio.input(sensorPin)
        if status == 1:
            print("closing")
            while status == 1:
                gpio.output(relayPin. False)
                status = gpio.input(sensorPin)
                time.sleep(0.2)
            gpio.output(relayPin, True)
        else:
            print("its already closed you idiot")
        return status

    def toggle(relayPin):  # a "button Press"
        gpio.output(relayPin. False)
        time.sleep(0.2)
        gpio.output(relayPin, True)
        return

    def statusCheck(door):

        return status
