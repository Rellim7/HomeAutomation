import RPi.GPIO as gpio
import time
import sys
gpio.setmode(gpio.BCM)

import thread, time

def input_thread(L):
    input()
    L.append(None)
    


class mrCoffee(object):
    """
    Mr coffee is here to serve up delicious coffee goodness.   He  can operate by timer or by measuring out the output.
    """

    def __init__(self):
        self.powerPin = 4
        self.pumpPin = 17
        self.scalePin1 = 14 #subject to change.  May have multiple scale pins
        self.powerStatus = False
        self.pumpStatus = False
        #setup pins for input/output

        gpio.setup(self.powerPin, gpio.OUT)
        gpio.setup(self.pumpPin, gpio.OUT)
        gpio.setup(self.scalePin1, gpio.IN, pull_up_down=gpio.PUD_UP)

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
        weight = 0
        return weight
    
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
            sys.stdout.write("weight: %d%%   \r" % str(weightDif))
            sys.stdout.write("time: %d%%   \r" % str(timeDif))
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
            sys.stdout.write("weight: %d%%   \r" % str(weightDif))
            sys.stdout.write("time: %d%%   \r" % str(timeDif))
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
        L = []
        thread.start_new_thread(input_thread, (L,))
        while 1:
            time.sleep(.1)
            if L: break
            weightDif = self.getWeight()- startingWeight
            timeDif = time.time() -startTime
            sys.stdout.write("weight: %d%%   \r" % str(weightDif))
            sys.stdout.write("time: %d%%   \r" % str(timeDif))
            sys.stdout.flush()      
        input("press Enter when done")
        self.setWeight(weightDif)
        self.setTime(timeDif)
        return 