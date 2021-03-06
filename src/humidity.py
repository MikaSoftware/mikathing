#!/usr/bin/python
import os
import sys
import signal
import time
import traceback
from dotenv import load_dotenv
load_dotenv()

from Phidget22.Devices.HumiditySensor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *


"""
* Configures the device's DataInterval and ChangeTrigger.
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
"""
def onAttachHandler(self):

    ph = self
    try:
        # Fetch this devices maximum data interval.
        maxDataInterval = ph.getMaxDataInterval() # 60000

        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between HumidityChange events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        # Note: 1,000 milliseconds = 1 second
        #       60,000 ms = 60 s = 1 minute (Max allowed by Phidget)
        #       300,000 ms = 5 minutes
        ph.setDataInterval(maxDataInterval)

        """
        * Set the HumidityChangeTrigger inside of the attach handler to initialize the device with this value.
        * HumidityChangeTrigger will affect the frequency of HumidityChange events, by limiting them to only occur when
        * the humidity changes by at least the value set.
        """
        ph.setHumidityChangeTrigger(0.0)

    except PhidgetException as e:
        sys.stderr.write("Phidget Error -> Registering HumiditySensor: \n\t" + str(e))
        traceback.print_exc()
        return


"""
Fired when a Phidget channel with onDetachHandler registered detaches. Will
send the shutdown signal to the application because our sensor went offline.

@param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):
    sys.stderr.write("One of the Phidgets has been disconnected, shutting down application now..")
    os.kill(os.getpid(), signal.SIGHUP) # Unix version only...


"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):
    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")
    os.kill(os.getpid(), signal.SIGHUP) # Unix version only...


class HumiditySensorAccessObject:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if HumiditySensorAccessObject.__instance == None:
            HumiditySensorAccessObject()
        return HumiditySensorAccessObject.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if HumiditySensorAccessObject.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            HumiditySensorAccessObject.__instance = self

            try:
                HumiditySensorAccessObject.__ch = HumiditySensor()
            except PhidgetException as e:
                sys.stderr.write("Phidget Error -> Creating HumiditySensor: \n\t" + str(e))
                raise
            except RuntimeError as e:
                sys.stderr.write("Runtime Error -> Creating HumiditySensor: \n\t" + str(e))
                raise

            HUMIDITY_SERIAL_NUMBER = int(os.getenv("HUMIDITY_SERIAL_NUMBER"))
            HUMIDITY_VINT_HUB_PORT_NUMBER = int(os.getenv("HUMIDITY_VINT_HUB_PORT_NUMBER"))
            HUMIDITY_CHANNEL_NUMBER = int(os.getenv("HUMIDITY_CHANNEL_NUMBER"))

            HumiditySensorAccessObject.__ch.setDeviceSerialNumber(HUMIDITY_SERIAL_NUMBER)
            HumiditySensorAccessObject.__ch.setHubPort(HUMIDITY_VINT_HUB_PORT_NUMBER)
            HumiditySensorAccessObject.__ch.setChannel(HUMIDITY_CHANNEL_NUMBER)

            HumiditySensorAccessObject.__ch.setOnAttachHandler(onAttachHandler)
            HumiditySensorAccessObject.__ch.setOnDetachHandler(onDetachHandler)
            HumiditySensorAccessObject.__ch.setOnErrorHandler(onErrorHandler)

    def setOnHumidityChangeHandlerFunc(self, onHumidityChangeHandler):
        """
        Set the callback function to the channel to be triggered when the
        event is fired by the humidity sensor with the value of the most recent
        reading.
        """
        self.__ch.setOnHumidityChangeHandler(onHumidityChangeHandler)

    def beginOperation(self):
        """
        Open the channel with humidity sensor along with a timeout.
        """
        try:
            self.__ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            sys.stderr.write("Phidget Error -> Waiting for Attachment but received error ID: \n\t" + str(e))
            os.kill(os.getpid(), signal.SIGHUP) # Unix version only...

    def terminateOperation(self):
        """
        Closes the channel with the humidity sensor.
        """
        #clear the HumidityChange event handler
        self.__ch.setOnHumidityChangeHandler(None)
        self.__ch.close()

    def getRelativeHumidity(self):
        """
        Returns the most recent humidity value that the channel has reported.
        """
        return self.__ch.getHumidity()
