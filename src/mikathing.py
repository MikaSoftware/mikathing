#!/usr/bin/python
import datetime
import os
import sys
import signal
from datetime import timezone
from dotenv import load_dotenv
load_dotenv(verbose=True)

from humidity import *
from temperature import *
from persistent_storage import *


class MikaThingRuntimeOperation:
    """
    Class runs the continous operation of polling the attached Phidget devices
    and submits the instruments readings to a remote logging serverself.

    When the Unix environment sends a `SIGINT` or `SIGTERM` signal, this class
    will gracefully shutdown by shutting down the Phidgets first before closing.
    """
    app_data_interval = 0
    humidity_dao = None
    temperature_dao = None
    storage_dao = None
    is_running = False

    def __init__(self):
        # Setup all our instrument's sensor(s).
        self.humidity_dao = HumiditySensorAccessObject.getInstance()
        self.humidity_dao.setOnHumidityChangeHandlerFunc(None)
        self.humidity_dao.beginOperation()
        self.temperature_dao = TemperatureSensorAccessObject.getInstance()
        self.temperature_dao.setOnTemperatureChangeHandlerFunc(None)
        self.temperature_dao.beginOperation()
        self.storage_dao = PersistentStorageDataAccessObject.getInstance()
        self.storage_dao.beginOperation()

        # Variable controls what time the application will start on, for example if
        # this value will be 5 then the acceptable times could be: 1:00 AM, 1:05 AM,
        # 1:10 AM, etc.
        self.app_data_interval = int(os.getenv("APPLICATION_DATA_INTERVAL_IN_MINUTES"))

        # Integrate this code with our Unix environment so when a kill command
        # is sent to this application then our code will gracefully exit.
        signal.signal(signal.SIGINT, self.exitGracefully)
        signal.signal(signal.SIGTERM, self.exitGracefully)

    def exitGracefully(self,signum, frame):
        self.is_running = False

    def start(self):
        self.is_running = True

    def shutdown(self):
        # Gracefully disconnect our application with the hardware devices.
        self.humidity_dao.terminateOperation()
        self.temperature_dao.terminateOperation()
        self.storage_dao.terminateOperation()

    def runOnMainLoop(self):
        # We will continue running the mainloop until our class indicates we
        # should stop with the `is_running` value set to `False`. This valuse
        # will be set to `False` if the class detects a `SIGINT` or `SIGTERM`
        # signal from the ``Linux environment.
        while self.is_running:
            # The following code block will get the current UTC datetime and
            # make sure the fetched datatime is in sync with our applications
            # fetch interval clock. For example, if our fetch interval is "5"
            # then the application will poll the sensors at time intervals of
            # 1:00, 1:05, 1:10, 1:15, 1:20, etc.
            now_dt = datetime.datetime.utcnow()
            now_ts = now_dt.replace(tzinfo=timezone.utc).timestamp()
            if now_dt.second == 0:
                if now_dt.minute % self.app_data_interval == 0 or now_dt.minute == 0:
                    try:
                        humidity_value = self.humidity_dao.getRelativeHumidity()
                        temperature_value = self.temperature_dao.getTemperature()
                        print("Saving at:", now_dt)
                        print("Humidity", humidity_value, "%")
                        print("Temperature", temperature_value," degree C\n")
                        self.storage_dao.insertTimeSeriesData(1, humidity_value, now_ts)
                        self.storage_dao.insertTimeSeriesData(2, temperature_value, now_ts)
                    except Exception as e:
                        self.is_running = False
                        sys.stderr.write("Phidget Error -> Runtime Error: \n\t" + e)

            # Block the mainloop for 1 second
            time.sleep(1) # 1 second

            # The following block of code will fetch all the time-series data
            # we have stored in our local persistent storage and if there is
            # any data stored then we will submit the data to our remote data
            # storage service. Afterwords we will delete the data that was
            # submitted.
            tsd_records = self.storage_dao.fetchAllTimeSeriesData()
            if tsd_records.count() > 0:
                #TODO: IMPLEMENT SUBMITTING DATA TO MIKAPOST.COM
                self.storage_dao.deleteSelectedTimeSeriesData(tsd_records)


if __name__ == "__main__":
    """
    Main entry into the application.
    """
    operation = MikaThingRuntimeOperation()
    operation.start()
    operation.runOnMainLoop()
    operation.shutdown()
