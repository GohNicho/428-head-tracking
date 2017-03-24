from pymongo import MongoClient
from collections import OrderedDict
from analyzer import *
import json

class Database:
    # database to store all of the quaternions from the device
    
    def __init__(self):
        # connect to the client
        self.__client = MongoClient('mongodb://localhost:27017/')
        # get the corresponding db
        self.__db = self.__client['head_tracker']
        # get all collections
        self.__head_tracking = self.__db['head_tracking']
        self.__client_session = self.__db['client_session']
        
    def add_tracking(self, vals, gest):
        '''
        add the numerical values from the device to the db
        input:
        val - quaternion values which consist of [x_rot, y_rot, z_rot]
        '''
        try:
            self.__head_tracking.insert_one(
                    {
                    "x_rot": vals[0],
                    "y_rot": vals[1],
                    "z_rot": vals[2],
                    "gesture": gest
                    })
        except Exception as e:
            print (str(e))
            
    def add_client(self, client, choices):
        '''
        add the client information using the Client class and
        an array of tuples
        input:
        client - Client object with information
        choices - array of tuples where the first value is the choice made and
        the second is the head gesture time duration
        (ex. [("choice1a", 5.0), ("choice2a", 4.4)] )
        '''
        
        # works with any generic number of fields

        # create the document
        
        doc = OrderedDict()

        # get client info
        for item in client.get_info():
            doc[item[0]] = item[1]
        
        # get all the choice info
        for i in range (0, len(choices)):
            doc["choice"+str(i+1)] = choices[i][0]
            doc["choice"+str(i+1)+"time"] = choices[i][1]
        
        try:
            self.__client_session.insert_one(doc)
            self.list_clients()
        except Exception as e:
            print (str(e))       
        
    def list_clients(self):
        '''
        print all documents of clients
        '''
        try:
            for doc in self.__client_session.find({}):
                print (doc)
        except Exception as e:
            print (str(e))
        
    def list_tracking(self):
        '''
        print all documents of head_tracking info
        '''
        
        try:   
            for doc in self.__head_tracking.find({}):
                print (doc)
                
        except Exception as e:
            print (str(e))