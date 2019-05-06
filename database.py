"""db setup"""
from enum import Enum
from pymongo import MongoClient, errors


class Database():

    Criterion = Enum('Criterion', 'price time')

    def __init__(self, ip, port, db_name):
        self.client = MongoClient(ip, port)  # get client
        self.name = db_name
        self.db = self.client[db_name]

        # check if database is connected
        try:
            self.client.server_info()
            print("Connected to {}:{} - {}".format(ip, port, db_name))
        except errors.ServerSelectionTimeoutError:
            print("Failed to connect to database")
            exit()

        self.drop_database()  # remove all data from db
        self.flights = self.db.flights
        self.airports = self.db.airports

    def add_airport(self, airport):
        result = self.airports.find({"id": airport})
        if result.count() == 0:
            self.airports.insert_one({"id": airport})

    """Add flight to db"""
    def add_flight(self, orig, dest, **kwargs):

        self.add_airport(orig)
        self.add_airport(dest)

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

    def all_airports(self):
        return self.airports.find({})

    def all_airports_list(self):
        group = self.db.airports.aggregate([
            {"$group": {
                "_id": None,
                "ids": {"$push": "$id"}
            }}
        ])

        return list(group)[0]["ids"]

    def get_shortest_path(self, orig, dest):
        return 1

    # TODO: Function get shortest path for dest orig pair

    # TODO: Create a shortest path document/entry from array
    # of dest orig string pair
