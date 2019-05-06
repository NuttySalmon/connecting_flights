from database import Database
from collections import OrderedDict


class ConnectingFlight:
    def __init__(self, database):
        self.db = database
        #self.floyd_warshal_shortest = {}

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
        #cri = criterion.name
        all_airports = self.db.all_airports_list()

        self.make_adj(all_airports, criterion)
        for thru in all_airports:   # intermediate point
            for orig in all_airports:
                if orig == thru:
                    continue  # continue if intermediate is same as origin
                for dest in all_airports:
                    if dest == thru or dest == orig:
                        # continue if intermediate or destination is origin
                        continue

                    orig_to_thru = self.db.get_adj(criterion, orig, thru)
                    thru_to_dest = self.db.get_adj(criterion, thru, dest)
                    if orig_to_thru is None or thru_to_dest is None:
                        continue

                    new_weight = orig_to_thru["weight"] + thru_to_dest["weight"]
                    last_path = thru_to_dest["thru"]
                    orig_adj = self.db.get_adj(criterion, orig, dest)
                    if orig_adj is None:
                        self.db.add_to_adj(criterion, orig, dest, last_path, new_weight)
                    else:
                        old_weight = orig_adj["weight"]
                        if new_weight < old_weight:
                            self.db.update_adj(criterion, orig, dest, last_path, new_weight)

        # print(adj)
        # self.floyd_warshal_shortest = adj

    def print_floyd_warshal(self, criterion):
        all_airports = self.db.all_airports_list()

        for orig in all_airports:
            for des in all_airports:
                shortest = []

                start = orig
                end = des
                while start != end:
                    adj = self.db.get_adj(criterion, start, end)
                    if adj is None:
                        break
                    mid = adj["thru"]
                    shortest.append((mid, end))
                    end = mid

                print("\nFrom {} to {}:".format(orig, des))
                if len(shortest) > 0:
                    total = 0
                    for start, end in shortest[::-1]:
                        weight = self.db.get_weight(criterion, start, end)
                        total += weight
                        weight = self.get_str_from_cri(criterion, weight)
                        print("{}->{}: {}".format(start, end, weight))

                    total = self.get_str_from_cri(criterion, total)
                    print("Total {}: {}".format(criterion.name, total))
                else:
                    print("Not connected")


    def get_str_from_cri(self, criterion, target):
        if criterion == Database.Criterion.price:
            return "${}".format('%.2f' % target)
        elif criterion == Database.Criterion.time:
            return "{}h {}m".format(target // 60, target % 60)



    def make_adj(self, all_airports, criterion):
        weight_name = criterion.name

        # adj key: origin destion pair
        # adj value: origin of last path and weight

        for orig in all_airports:
            connected = self.db.all_flights_from(orig)
            for flight in connected:
                dest = flight["dest"]
                self.db.add_to_adj(criterion, orig, dest, orig, flight[weight_name])
        # print(adj)
        #return adj

    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)
