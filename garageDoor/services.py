import RPI.GPIO as GPIO
from .models import door
GPIO.setmode(GPIO.BCM)

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
        return

    def close(door):
        """
        closes the door.
        also will check if the door is already closed.  If it is throw an error.  Pulse the signal on then off.
        """
        return status

    def forceClose(door):
        """
        closes the door.   This call is dangerous cause it could cause damage to anything in the way of the door.
        If the door is closed already this will throw a bloody tantrum.   It has to  hold the button down for X amount  of seconds.  Also checking to see if the door has made it to the
        closed state.
        """
        return status

    def statusCheck(door):

        return status
