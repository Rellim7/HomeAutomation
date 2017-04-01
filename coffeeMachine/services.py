import RPi.GPIO as gpio
import time
import sys
gpio.setmode(gpio.BCM)
from hx711 import HX711
import threading as thread



class mrCoffee(object):
    """
    Mr coffee is here to serve up delicious coffee goodness.   He  can operate by timer or by measuring out the output.
    """

    def __init__(self):
        self.powerPin = 17
        self.pumpPin = 4
        self.scalePin1 = 5 #subject to change.  May have multiple scale pins
        self.scalePin2 = 6
        self.timeButton = 19
        self.weightButton = 13
        self.manualButton = 18
        self.powerStatus = False
        self.pumpStatus = False

        #setup scale 
        self.hx = HX711(self.scalePin1, self.scalePin2)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(4030)  #Tweak this to tune the scale.
        self.hx.reset()
        self.hx.tare() 

        #setup pins for input/output        
        gpio.setup(self.powerPin, gpio.OUT)
        gpio.setup(self.pumpPin, gpio.OUT)
        gpio.setup(self.timeButton, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.weightButton, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.manualButton, gpio.IN, pull_up_down=gpio.PUD_UP)

    def togglePower(self):
        """
        Turns the machine on or off.   Need a sensor incase in manual mode to dectect power status
        """
        if self.powerStatus == False:
            gpio.output(self.powerPin, True)
            self.powerStatus = True
        elif self.powerStatus == True:
            gpio.output(self.powerPin, False)
            self.powerStatus = False
        return self.powerStatus

    def _togglePump(self):
        """
        Turns the pump on or off to pump coffee or not.    
        """
        if self.pumpStatus == False:
            gpio.output(self.pumpPin, True)
            self.pumpStatus = True
        elif self.pumpStatus == True:
            gpio.output(self.pumpPin, False)
            self.pumpStatus = False
        return self.pumpStatus

    def setWeight(self,weight):
        self.weightOutput = weight
        return self.weightOutput

    def getWeight(self):
        #measure stuff
        self.hx.reset()
        weight = self.hx.get_weight(4)
        return weight

    def timeStatus(self):
        #check the time button to see if it is being pressed
        status = gpio.input(self.timeButton)
        return status

    def weightStatus(self):
        #check the weight button to see if it is being pressed
        status = gpio.input(self.weightButton)
        return status

    def manualStatus(self):
        #check the manual button to see if it is being pressed
        status = gpio.input(self.manualButton)
        return status

    def setTime(self, runTime):
        self.runningTime = runTime
        return self.runningTime

    def runTimed(self):
        """
        Run a timed run based on the runningTime
        """
        startTime =time.time()
        self._togglePump()
        timeDif = time.time() - startTime
        startingWeight = self.getWeight()
        weightDif = self.getWeight()- startingWeight
        while timeDif <= self.runningTime:
            weightDif = self.getWeight()- startingWeight
            timeDif = time.time() -startTime
            sys.stdout.write(" weight: %d%%   \n" % weightDif)
            sys.stdout.write("\r time: %d%%   " % timeDif)
            sys.stdout.flush()
        self._togglePump()
        return

    def runWeighted(self):
        """
        run a weighted run based on weightOutput
        """
        startTime =time.time()
        self._togglePump()
        timeDif = time.time() -startTime
        startingWeight = self.getWeight()
        weightDif = self.getWeight()- startingWeight 
        while weightDif <= self.weightOutput:
            timeDif = time.time() -startTime
            weightDif = self.getWeight()- startingWeight
            sys.stdout.write("weight: %d%%   \n" % weightDif)
            sys.stdout.write("\r time: %d%%   " % timeDif)
            sys.stdout.flush()
        self._togglePump()
        return
    
    def runManaul(self):
        """
        run a pull without automation to set or find the time or weight. Then set both of those values
        """
        startTime =time.time()
        self._togglePump()
        timeDif = time.time() -startTime
        startingWeight = self.getWeight()
        weightDif = self.getWeight()- startingWeight 
        manStatus = self.manualStatus()
        while manStatus:
            weightDif = self.getWeight()- startingWeight
            timeDif = time.time() -startTime
            sys.stdout.write(" weight: %d%%   \n" % weightDif)
            sys.stdout.write("\r time: %d%%   " % timeDif)
            sys.stdout.flush()
            manStatus = self.manualStatus()
        self.setWeight(weightDif)
        self.setTime(timeDif)
        print("The results are: Output = " + weightDif + "g and time = "+ timeDif +"s")
        return


if __name__ == "__main__":
    c = mrCoffee()
    while 1:
        try:
            if c.timeStatus():
                c.runTimed()
            if c.weightStatus():
                c.runWeighted()
            if c.manualStatus():
                c.runManaul()
        except (KeyboardInterrupt, SystemExit):
            print ("Cleaning...")
            gpio.cleanup()
            print ("Bye!")
            sys.exit()