"""db setup"""
from enum import IntEnum
from pymongo import MongoClient, errors


class Database():
    """Facilitate manipulation of data in database"""

    Criterion = IntEnum('Criterion', 'price duration distance')  # Criterions as weight for calulating shortest path

    def __init__(self, ip, port, db_name):
        """Constructor"""

        self._client = MongoClient(ip, port)  # get client
        self._name = db_name
        self._db = self._client[db_name]

        # check if database is connected
        try:
            self._client.server_info()
            print("Connected to {}:{} - {}".format(ip, port, db_name))
        except errors.ServerSelectionTimeoutError:
            print("Failed to connect to database")
            exit()

        self._flights = self._db.flights
        self._airports = self._db.airports
        self._adj = self._db.adj

    def add_airport(self, airport):
        """Add airport if it does not exist already. Take airport id as string"""

        if self._airports.count_documents({"id": airport}) == 0:
            self._airports.insert_one({"id": airport})

    def add_flight(self, orig, dest, **kwargs):
        """Add flight to db"""

        self.add_airport(orig)
        self.add_airport(dest)

        new_flight = {"orig": orig,
                      "dest": dest}

        for key, val in kwargs.items():
            new_flight[key] = val

        return self._flights.insert_one(new_flight)

    def drop_database(self):
        """Drop db"""

        self._client.drop_database(self._name)

    def all_flights_from(self, orig):
        """Get all flights connected to give origin airport id"""
        return self._flights.find({"orig": orig})

    @property
    def all_airports(self):
        """Returns all airports as list of strings"""

        group = self._airports.aggregate([
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
        self._adj.insert_one(new_adj)

    def get_adj(self, criterion, orig, dest):
        """Get adj entry"""

        target = {"criterion": criterion.name, "orig": orig, "dest": dest}
        return self._adj.find_one(target)

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

        self._adj.update_one(query, new_val)

    def get_weight(self, criterion, orig, dest):
        """Get weight of given flight"""

        query = {
            "orig": orig,
            "dest": dest
        }
        target = self._flights.find_one(query)
        return float(target[criterion.name])  # return weight

    def clear_adj(self):
        """Drop adj"""

        self._adj.drop()

    @property
    def all_flights(self):
        """Return all flights"""

        return self._flights.find()