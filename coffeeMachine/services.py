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
        self.setTime(29)
        self.setWeight(36)
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
    def forceOFf():
        #everybody panic
        gpio.output(self.pumpPin, False)
        return
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
            sys.stdout.write(" weight: %dg   \n" % weightDif)
            sys.stdout.write("\r time: %ds   " % timeDif)
            sys.stdout.flush()
            if not self.timeStatus():
                break
        self._togglePump()
        while not self.timeStatus():
            print("let go fo the button")        
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
            sys.stdout.write("weight: %dg   \n" % weightDif)
            sys.stdout.write("\r time: %ds   " % timeDif)
            sys.stdout.flush()
            if not self.weightStatus():
                break
        self._togglePump()
        while not self.weightStatus():
            print("let go fo the button")
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
            sys.stdout.write("weight: %dg   \n" % weightDif)
            sys.stdout.write("\r time: %ds   " % timeDif)
            sys.stdout.flush()
            manStatus = self.manualStatus()
        self._togglePump()
        weightDif = self.getWeight()- startingWeight
        self.setWeight(weightDif)
        self.setTime(timeDif)
        print("The results are: Output = " + str(weightDif) + "g and time = "+ str(timeDif) +"s")
        return


if __name__ == "__main__":
    c = mrCoffee()
    print("Mr Coffee is ready to take your order.")
    while c.manualStatus():
        print("the manual button is on.  PLease flip it. thanks")
    while 1:
        try:
            if not c.timeStatus():
                print("Running a timed Pull")
                c.runTimed()
                sys.stdout.flush()
                print("done")
            if not c.weightStatus():
                print("Running a weighted pull")
                c.runWeighted()
                sys.stdout.flush()
                print("done")
            if c.manualStatus():
                print("Running Manual Pull")
                c.runManaul()
        except (KeyboardInterrupt, SystemExit):
            print ("Cleaning...")
            c.forceOff()
            gpio.cleanup()
            print ("Bye!")
            sys.exit()