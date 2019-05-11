"""db setup"""
from enum import IntEnum
from pymongo import MongoClient, errors


class Database():
    """Facilitate manipulation of data in database"""

    Criterion = IntEnum('Criterion', 'price duration distance')  # Criterions as weight for calulating shortest path

    def __init__(self, ip, port, db_name):
        """Constructor"""

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

        self.flights = self.db.flights
        self.airports = self.db.airports
        self.adj = self.db.adj

    def add_airport(self, airport):
        """Add airport if it does not exist already. Take airport id as string"""

        if self.airports.count_documents({"id": airport}) == 0:
            self.airports.insert_one({"id": airport})

    def add_flight(self, orig, dest, **kwargs):
        """Add flight to db"""

        self.add_airport(orig)
        self.add_airport(dest)

        new_flight = {"orig": orig,
                      "dest": dest}

        for key, val in kwargs.items():
            new_flight[key] = val

        return self.flights.insert_one(new_flight)

    def drop_database(self):
        """Drop db"""

        self.client.drop_database(self.name)

    def all_flights_from(self, orig):
        """Get all flights connected to give origin airport id"""
        return self.flights.find({"orig": orig})

    def all_airports(self):
        """Returns all airports"""

        return self.airports.find({})

    def all_airports_list(self):
        """Returns all airports as list of strings"""

        group = self.airports.aggregate([
            {"$group": {
                "_id": None,
                "ids": {"$push": "$id"}
            }}
        ])

        return list(group)[0]["ids"]

    def add_to_adj(self, criterion, orig, dest, thru, weight, last_flight):
        """Add entry to adj"""

        new_adj = {
            "criterion": criterion.name,
            "orig": orig,
            "dest": dest,
            "thru": thru,
            "last_flight": last_flight,
            "weight": float(weight)
        }
        self.adj.insert_one(new_adj)

    def get_adj(self, criterion, orig, dest):
        """Get adj entry"""

        target = {"criterion": criterion.name, "orig": orig, "dest": dest}
        return self.adj.find_one(target)

    def update_adj(self, criterion, orig, dest, thru, weight, last_flight):
        """Update adj entry"""
        query = {
            "criterion": criterion.name,
            "orig": orig,
            "dest": dest,
        }

        new_val = {"$set": {
            "thru": thru,
            "weight": float(weight),
            "last_flight": last_flight
            }
        }

        self.adj.update_one(query, new_val)

    def get_weight(self, criterion, orig, dest):
        """Get weight of given flight"""

        query = {
            "orig": orig,
            "dest": dest
        }
        target = self.flights.find_one(query)
        return float(target[criterion.name])  # return weight

    def clear_adj(self):
        """Drop adj"""

        self.adj.drop()

    def all_flights(self):
        """Return all flights"""

        return self.flights.find()