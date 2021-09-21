# Config - file
# from configparser import ConfigParser
import pymongo

client = None
db = None


class Databaseconfig:
    """Used for managing interactions between worker process and mongo database"""
    @staticmethod
    def connect():
        """Connects to database"""
        global client, db
        # Read config.ini file
        # config_object = ConfigParser()

        try:
            # config_object.read("configfile.ini")
            # dataBase = config_object["DATABASE"]
            # connectionString = dataBase["localhost"]
            connectionString = 'mongodb://mongoAdmin:changeMe@127.0.0.1:27017/admin'
            client = pymongo.MongoClient(connectionString)
            print("Connecting to MongoDB ...")
            client.admin.command('isMaster')
            print("connected")
        except Exception as inst:
            print('Exception occurred while connecting to database', inst)
            if client is None:
                raise Exception('Mongo db not connected')
            db = client['admin']

