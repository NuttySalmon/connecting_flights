from .context import Database
IP = "localhost"
PORT = 27017
DB_NAME = "connecting_flight_test"

def setup():
    db = Database(IP, PORT, DB_NAME)
    db.drop_database()
    return db

def test_add_airport():
    db = setup()
    id = "test"
    db.add_airport(id)

    result = db.airports.find_one({"id": id})
    assert result["id"] == id

def test_add_duplicate_airport():
    db = setup()
    id = "test"
    db.add_airport(id)
    db.add_airport(id)
    db.add_airport(id)

    result = db.airports.count_documents({"id": id})
    assert result == 1

def test_add_flight():
    db = setup()

    airline = "A"
    no = 123
    orig = "SFO"
    dest = "LAX"
    price = 200
    distance = 5000

    db.add_flight(orig, dest, airline=airline, no=no, price=price, distance=distance)
    result = db.flights.count_documents(
        {"orig": orig,
         "dest": dest,
         "no": no,
         "price": price,
         "distance": distance
         })
    assert result == 1

def test_auto_add_airport():
    db = setup()
    airline = "A"
    no = 123
    orig = "SFO"
    dest = "LAX"
    price = 200
    distance = 5000

    db.add_flight(orig, dest, airline=airline, no=no, price=price, distance=distance)
    result1 = db.airports.count_documents({"id": orig})
    result2 = db.airports.count_documents({"id": dest})
    
    assert result1 == 1 and result2 == 1
