from .context import Database
from .context import ConnectingFlights
import random
import itertools

IP = "localhost"
PORT = 27017
DB_NAME = "connecting_flight_test"


def setup():
    db = Database(IP, PORT, DB_NAME)
    db.drop_database()
    cf = ConnectingFlights(db)
    return cf


def test_add_one_flight():
    cf = setup()
    orig = "a"
    dest = "b"
    price = 224
    time = 1
    cf.add_one_flight(orig, dest, **{"price": price, "time": time})
    result = cf.db._flights.count_documents({"dest": dest, "orig": orig,
                                             "price": price, "time": time})
    assert result == 1


def test_add_many_flights():
    cf = setup()
    v_size = 10
    e_size = 50
    data = []
    pairs = list(itertools.permutations(range(v_size), 2))
    random.shuffle(pairs)
    for x in range(e_size):
        orig, dest = pairs[x]
        price = random.randint(200, 1000)
        time = random.randint(60, 500)

        data.append([orig, dest, {"price": price, "time": time}])

    cf.add_many_flights(data)

    sample = data[random.randrange(e_size)]
    orig1 = sample[0]
    dest1 = sample[1]
    price1 = int(sample[2]["price"])
    time1 = int(sample[2]["time"])
    print(sample)
    result = cf.db._flights.count_documents({"dest": dest1, "orig": orig1, 
                                            "price": price1, "time": time1})

    assert result == 1


def test_adj_init_with_duplication():
    cf = setup()
    orig = "a"
    dest = "b"
    cf.add_many_flights([[orig, dest, {"price": 4}],
                         [orig, dest, {"price": 1}],
                         [orig, dest, {"price": 5}]])

    result = list(cf.db._adj.find({"orig": orig, "dest": dest}))
    size = len(result)
    weight = result[0]["weight"]

    assert size == 1 and weight == 1


def test_shortest_path():
    # based on this graph: 
    #https://en.wikipedia.org/wiki/Shortest_path_problem#/media/File:Shortest_path_with_direct_weights.svg
    cf = setup()
    cf.add_many_flights([["a", "b", {"price": 4, "time": 1}],
                        ["a", "c", {"price": 2, "time": 2}],
                        ["b", "c", {"price": 5, "time": 3}],
                        ["b", "d", {"price": 10, "time": 3}],
                        ["c", "e", {"price": 3, "time": 3}],
                        ["e", "d", {"price": 4, "time": 3}],
                        ["d", "f", {"price": 11, "time": 3}]])
    result = cf.get_shortest_floyd_warshal(cf.db.Criterion.price, "a", "f")

    shortest = []
    for flight in result["path"]:
        shortest.append((flight[0], flight[1]))

    expected = [('a', 'c'), ('c', 'e'), ('e', 'd'), ('d', 'f')]
    print(result)
    assert expected == shortest
