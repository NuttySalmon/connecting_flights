from database import Database
from connecting_flights import ConnectingFlight


if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlight(db)
    cf.add_many_flight([["SFO", "LAX", {"price": 130.34, "time": 90}],
                        ["SFO", "SAN", {"price": 152.07, "time": 121}],
                        ["SFO", "PDX", {"price": 329.11, "time": 643}],
                        ["SFO", "DEN", {"price": 170.21, "time": 183}]])
    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)