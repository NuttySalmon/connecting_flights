from shortest import Database, ConnectingFlights, main

if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlights(db)
    main.menu(db, cf)
    main.clear()
