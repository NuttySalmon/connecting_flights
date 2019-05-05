from database import Database
import heapq

class ConnectingFlight:
    def __init__(self, database):
        self.db = database
        
    def add_one_flight(self, orig, dest, **kwargs):
        db.add_flight(orig, dest, kwargs)
        self.calc_all()

    def add_many_flight(self, arr):

        for new_flight in arr:
            db.add_flight(new_flight[0], new_flight[1], **new_flight[2])

        self.calc_all()

    def calc_all(self):
        for cri in Database.Criterion:
            print(cri)
            for airport in self.db.all_airports():
                print(airport)
                self.dijkstra(cri, airport)


    def dijkstra(self, criterion, airport):
        shortest_path = []
        weight_name = criterion.name
        pq  = []
        orig = airport["icao"]
        connected = self.db.all_flights_from(orig)
        for flight in connected:
            heapq.heappush(pq, (flight[weight_name], [flight["orig"], flight["dest"]]))
        print(pq)


if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlight(db)
    cf.add_many_flight([["KLAX", "KSFO", {"price":203.34, "time":124}]])
    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)
