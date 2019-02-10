#!/usr/bin/python
import os
import sys
import signal
import time
import traceback

from Phidget22.Devices.TemperatureSensor import *
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
        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between TemperatureChange events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        # Note: 1000 milliseconds = 1 second
        ph.setDataInterval(60000) # 60,000 ms = 60 s = 1 minute

        """
        * Set the TemperatureChangeTrigger inside of the attach handler to initialize the device with this value.
        * TemperatureChangeTrigger will affect the frequency of TemperatureChange events, by limiting them to only occur when
        * the temperature changes by at least the value set.
        """
        ph.setTemperatureChangeTrigger(0.0)

    except PhidgetException as e:
        sys.stderr.write("Phidget Error -> Registering TemperatureSensor: \n\t" + e)
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


class TemperatureSensorAccessObject:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TemperatureSensorAccessObject.__instance == None:
            TemperatureSensorAccessObject()
        return TemperatureSensorAccessObject.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TemperatureSensorAccessObject.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TemperatureSensorAccessObject.__instance = self

            try:
                TemperatureSensorAccessObject.__ch = TemperatureSensor()
            except PhidgetException as e:
                sys.stderr.write("Phidget Error -> Creating TemperatureSensor: \n\t" + e)
                raise
            except RuntimeError as e:
                sys.stderr.write("Runtime Error -> Creating TemperatureSensor: \n\t" + e)
                raise

            TEMPERATURE_SERIAL_NUMBER = int(os.getenv("TEMPERATURE_SERIAL_NUMBER"))
            TEMPERATURE_VINT_HUB_PORT_NUMBER = int(os.getenv("TEMPERATURE_VINT_HUB_PORT_NUMBER"))
            TEMPERATURE_CHANNEL_NUMBER = int(os.getenv("TEMPERATURE_CHANNEL_NUMBER"))

            TemperatureSensorAccessObject.__ch.setDeviceSerialNumber(TEMPERATURE_SERIAL_NUMBER)
            TemperatureSensorAccessObject.__ch.setHubPort(TEMPERATURE_VINT_HUB_PORT_NUMBER)
            TemperatureSensorAccessObject.__ch.setChannel(TEMPERATURE_CHANNEL_NUMBER)

            TemperatureSensorAccessObject.__ch.setOnAttachHandler(onAttachHandler)
            TemperatureSensorAccessObject.__ch.setOnDetachHandler(onDetachHandler)
            TemperatureSensorAccessObject.__ch.setOnErrorHandler(onErrorHandler)

    def setOnTemperatureChangeHandlerFunc(self, onTemperatureChangeHandler):
        """
        Set the callback function to the channel to be triggered when the
        event is fired by the temperature sensor with the value of the most recent
        reading.
        """
        self.__ch.setOnTemperatureChangeHandler(onTemperatureChangeHandler)

    def beginOperation(self):
        """
        Open the channel with temperature sensor along with a timeout.
        """
        try:
            self.__ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            sys.stderr.write("Phidget Error -> Waiting for Attachment: \n\t" + e)
            raise

    def terminateOperation(self):
        """
        Closes the channel with the temperature sensor.
        """
        #clear the TemperatureChange event handler
        self.__ch.setOnTemperatureChangeHandler(None)
        self.__ch.close()

    def getTemperature(self):
        """
        Returns the most recent temperature value that the channel has reported.
        """
        return self.__ch.getTemperature()
