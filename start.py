from shortest import Database, ConnectingFlights, console

if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlights(db)
    console.menu(db, cf)
    console.clear()
