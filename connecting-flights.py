from database import Database


if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    db.addFlight("KLAX", "KSFO", price=203.34, time=124)
    result = db.allFlightsFrom("KLAX")
    for flight in result:
        print(flight)
