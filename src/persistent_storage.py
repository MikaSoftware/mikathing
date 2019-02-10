import os
from dotenv import load_dotenv
from peewee import *
load_dotenv(verbose=True)


"""
The following code will provide an interface with the local persistent storage
singleton class. The storage will be used to store time-series data in a SQL
database using the``peewee`` library. The application will call this interface
to store, list, retrieve and delete time-series data which we have locally.
"""


# create a peewee database instance -- our models will use this database to
# persist information
DATABASE = os.getenv("APPLICATION_DATABASE")
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database

class TimeSeriesData(BaseModel):
    id = BigAutoField(unique=True)
    thing_id = SmallIntegerField()
    value = FloatField()
    timestamp = TimestampField()

class PersistentStorageDataAccessObject:
    """
    Singleton class used to provide a single point of access with our local
    persistent storage with the application.
    """
    __instance = None
    __db = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PersistentStorageDataAccessObject.__instance == None:
            PersistentStorageDataAccessObject()
        return PersistentStorageDataAccessObject.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if PersistentStorageDataAccessObject.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            PersistentStorageDataAccessObject.__instance = self
            PersistentStorageDataAccessObject.__db = database

    def beginOperation(self):
        """
        Connect with our persistent storage.
        """
        self.__db.connect()
        self.__db.create_tables([TimeSeriesData])

    def terminateOperation(self):
        """
        Close our connection with the persistent storage.
        """
        self.__db.close()

    def insertTimeSeriesData(self, thing_id, value, timestamp):
        """
        Function will insert a new ``TimeSeriesData`` record into our
        persistent storage.
        """
        with database.atomic():
            tsd = TimeSeriesData(thing_id = thing_id, value=value, timestamp=timestamp)
            tsd.save()

    def fetchAllTimeSeriesData(self):
        """
        Function will return all the ``TimeSeriesData`` objects we have in the
        persistent storage.
        """
        with database.atomic():
            return TimeSeriesData.select()

    def deleteSelectedTimeSeriesData(self, tsd_records):
        with database.atomic():
            for tsd in tsd_records:
                pass
                # tsd.delete_instance() #TODO: Uncomment when remote upload works.
