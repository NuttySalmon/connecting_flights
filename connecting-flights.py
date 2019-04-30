from database import Database

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
        all_list = db.all_collections()
        for l in all_list:
            self.dijkstra(l["criterion"])   

    def dijkstra(self, criterion):
        print(criterion)
        





if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlight(db)
    cf.add_many_flight([["KLAX", "KSFO", {"price":203.34, "time":124}]])
    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)
