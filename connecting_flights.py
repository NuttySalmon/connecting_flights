from database import Database
from collections import OrderedDict


class ConnectingFlight:
    def __init__(self, database):
        self.db = database
        self.floyd_warshal_shortest = {}

    def add_one_flight(self, orig, dest, **kwargs):
        self.db.add_flight(orig, dest, kwargs)
        self.calc_all()

    def add_many_flight(self, arr):

        for new_flight in arr:
            self.db.add_flight(new_flight[0], new_flight[1], **new_flight[2])

        # self.calc_all()

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

        all_airports = self.db.all_airports_list()

        adj = self.make_adj(all_airports, criterion)
        for thru in all_airports:   # intermediate point
            for orig in all_airports:
                if orig == thru:
                    continue  # continue if intermediate is same as origin
                for dest in all_airports:
                    if dest == thru or dest == orig:
                        # continue if intermediate or destination is origin
                        continue

                    try:
                        new_weight = adj[(orig, thru)][1] + adj[(thru, dest)][1]
                        try:
                            old_weight = adj[(orig, dest)][1]
                            if new_weight < old_weight:
                                adj[orig, dest] = (adj[(thru, dest)][0], new_weight)
                        except KeyError:
                            adj[orig, dest] = (adj[(thru, dest)][0], new_weight)

                    except KeyError:
                        # do nothin if one of the intermediate paths not found
                        continue
        print(adj)
        self.floyd_warshal_shortest = adj

    def print_floyd_warshal(self):
        all_airports = self.db.all_airports_list()

        for orig in all_airports:
            for des in all_airports:
                shortest = []
                try:
                    start = orig
                    end = des
                    while start != end:
                        mid = self.floyd_warshal_shortest[(start, end)][0]
                        shortest.append((mid, end))
                        end = mid
                except KeyError:
                    pass

                print("\nFrom {} to {}:".format(orig, des))
                if len(shortest) > 0:
                    for start, end in shortest[::-1]:
                        print("{}->{}".format(start, end))
                else:
                    print("Not connected")


    def make_adj(self, all_airports, criterion):
        weight_name = criterion.name

        adj = {}
        # adj key: origin destion pair
        # adj value: origin of last path and weight

        for orig in all_airports:
            connected = self.db.all_flights_from(orig)
            for flight in connected:
                dest = flight["dest"]
                adj[(orig, dest)] = (orig, flight[weight_name])
        # print(adj)
        return adj


    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)
