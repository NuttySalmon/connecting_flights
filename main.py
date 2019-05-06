from database import Database
from connecting_flights import ConnectingFlight


if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlight(db)
    cf.add_many_flight([["a", "b", {"price": 4, "time": 1}],
                        ["a", "c", {"price": 2, "time": 2}],
                        ["b", "c", {"price": 5, "time": 3}],
                        ["b", "d", {"price": 10, "time": 3}],
                        ["c", "e", {"price": 3, "time": 3}],
                        ["e", "d", {"price": 4, "time": 3}],
                        ["d", "f", {"price": 11, "time": 3}]])

    cf.floyd_warshal(Database.Criterion.price)
    # result = db.all_flights_from("KLAX")
    # for flight in result:
    #     print(flight)