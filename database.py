"""db setup"""
from pymongo import MongoClient, errors
from enum import Enum

class Database(): 

    Criterion = Enum('Criterion', 'price time')

    def __init__(self, ip, port, db_name):
        self.client = MongoClient(ip, port)  # get client
        self.name = db_name
        self.db = self.client[db_name]
        self.dropDatabase()  # remove all data from db
        
        #
        try:  #test if db is connected
            self.client.server_info()
            print("Connected to {}:{} - {}".format(ip, port, db_name))
        except:
            print("Failed to connect to database")

        self.flights = self.db.flights
        self.grouped_shortest = self.db.shortestListList
        self.initGroupedShortest()


    """Add flight to db"""
    def addFlight(self, orig, dest, **kwargs):
        new_flight = {"orig": orig,
                    "dest": dest}

        for key, val in kwargs.items():
            new_flight[key] = val

        return self.flights.insert_one(new_flight)

    """Drop db"""
    def dropDatabase(self):
        self.client.drop_database(self.name)

    def initGroupedShortest(self):
        for x in Database.Criterion:
            self.grouped_shortest.insert_one({"Criterion": x.name, "shortestList": []})


