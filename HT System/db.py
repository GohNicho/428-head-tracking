from pymongo import MongoClient

class Database:
    # database to store all of the quaternions from the device
    
    def __init__(self):
        # connect to the client
        self.__client = MongoClient('mongodb://localhost:27017/')
        # get the corresponding db
        self.__db = client.head_tracker
        # get all collections
        self.__head_tracking = self.__db['head_tracking']
        self.__client_session = self.__db['client_session']
        
    def add_tracking(self, val):
        '''
        add the numerical values from the device to the db
        input:
        val - quaternion values which consist of [gravity, x_rot, y_rot, z_rot]
        '''
        self.__head_tracking.insert_one(
                {
                "grav": val[0],
                "x_rot": val[1],
                "y_rot": val[2],
                "z_rot": val[3]
                })        