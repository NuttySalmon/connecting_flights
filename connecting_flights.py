from database import Database
from collections import OrderedDict


class ConnectingFlight:
    def __init__(self, database):
        self.db = database

    def add_one_flight(self, orig, dest, **kwargs):
        self.db.add_flight(orig, dest, kwargs)
        self.calc_all()

    def add_many_flight(self, arr):

        for new_flight in arr:
            self.db.add_flight(new_flight[0], new_flight[1], **new_flight[2])

        self.calc_all()

    def calc_all(self):
        for cri in Database.Criterion:
            print("Criteron: {}".format(cri.name))
            for airport in self.db.all_airports():
                print("{}:".format(airport["id"]))
                self.dijkstra(cri, airport)

    def dijkstra(self, criterion, airport):
        shortest_path = []
        weight_name = criterion.name
        currWeight = 0
        pq = OrderedDict()
        orig = airport["id"]
        pq = self.add_connected(pq, orig, currWeight, weight_name)
        curr = None
        while(len(pq) != 0):
            curr = pq.popitem(last=False)
            shortest_path.append(curr)
            print("procressing {}".format(curr[0]))
            pq = self.add_connected(pq=pq, orig=curr[0], currWeight=curr[1][0],
                                    weight_name=weight_name)
        for p in shortest_path:
            print("{}->{}".format(p[1][1]["orig"], p[1][1]["dest"]))

    def add_connected(self, pq, orig, currWeight, weight_name):
        connected = self.db.all_flights_from(orig)
        for flight in connected:
            f_dest = flight["dest"]
            f_w = flight[weight_name]
            try:
                oldWeight = pq[f_dest][0]
                newWeight = f_w + currWeight
                if newWeight < oldWeight:
                    pq[f_dest] = (newWeight, flight)

            except KeyError:
                pq[f_dest] = (f_w, flight)

        return OrderedDict(sorted(pq.items(), key=lambda x: x[1][0]))

    def floyd_warshal(self, criterion):
        weight_name = criterion.name
        adj = {}
        for airport in self.db.all_airports():
            orig = airport["id"]
            connected = self.db.all_flights_from(orig)
            for flight in connected:
                dest = flight["dest"]
                adj[(orig, dest)] = flight[weight_name]
        print(adj)
    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)
