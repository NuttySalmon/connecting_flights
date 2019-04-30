from database import Database

class ConnectingFlight:
    def __init__(self, database):
        self.db = database
        

        





if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlight(db)
    cf.add_many_flight([["KLAX", "KSFO", {"price":203.34, "time":124}]])
    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)
