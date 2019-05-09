"""db setup"""
from enum import Enum
from pymongo import MongoClient, errors


class Database():

    Criterion = Enum('Criterion', 'price time distance')

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
        self.adj = self.db.adj

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
            new_flight[key] = float(val)

        return self.flights.insert_one(new_flight)

    """Drop db"""
    def drop_database(self):
        self.client.drop_database(self.name)

    def all_flights_from(self, orig):
        return self.flights.find({"orig": orig})

    def all_airports(self):
        return self.airports.find({})

    def all_airports_list(self):
        group = self.airports.aggregate([
            {"$group": {
                "_id": None,
                "ids": {"$push": "$id"}
            }}
        ])

        return list(group)[0]["ids"]


    def add_to_adj(self, criterion, orig, dest, thru, weight):
        new_adj = {
            "criterion": criterion.name,
            "orig": orig,
            "dest": dest,
            "thru": thru,
            "weight": weight
        }
        self.adj.insert_one(new_adj)

    def get_adj(self, criterion, orig, dest):
        target = {"criterion": criterion.name, "orig": orig, "dest": dest}
        return self.adj.find_one(target)

    def update_adj(self, criterion, orig, dest, thru, weight):
        query = {
            "criterion": criterion.name,
            "orig": orig,
            "dest": dest,
        }

        new_val = {"$set": {
            "thru": thru,
            "weight": weight
            }
        }

        self.adj.update_one(query, new_val)

    def get_weight(self, criterion, orig, dest):
        query = {
            "orig": orig,
            "dest": dest
        }
        target = self.flights.find_one(query)
        return target[criterion.name]  # return weight

    def clear_adj(self):
        self.adj.drop()
