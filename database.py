"""db setup"""
from pymongo import MongoClient, errors
from enum import Enum

class Database(): 

    Criterion = Enum('Criterion', 'price time')

    def __init__(self, ip, port, db_name):
        self.client = MongoClient(ip, port)  # get client
        self.name = db_name
        self.db = self.client[db_name]
        self.drop_database()  # remove all data from db
        
        
        try:  #test if db is connected
            self.client.server_info()
            print("Connected to {}:{} - {}".format(ip, port, db_name))
        except:
            print("Failed to connect to database")

        self.flights = self.db.flights
        self.airports = self.db.airports
        
    def add_airort(self, airport):
        result = self.airports.find({"icao": airport})
        if result.count() == 0:
            self.airports.insert_one({"icao": airport})

    """Add flight to db"""
    def add_flight(self, orig, dest, **kwargs):

        self.add_airort(orig)
        self.add_airort(dest)

        new_flight = {"orig": orig,
                    "dest": dest}

        for key, val in kwargs.items():
            new_flight[key] = val

        return self.flights.insert_one(new_flight)

    """Drop db"""
    def drop_database(self):
        self.client.drop_database(self.name)

    def all_flights_from(self, orig):
        return self.flights.find({"orig": orig})

   