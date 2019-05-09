from database import Database
from connecting_flights import ConnectingFlight
import tkinter
from tkinter import *
from tkinter.ttk import *
import csv

def import_route_csv(cf, filename):
    with open(filename, 'r') as routedata:
        routes_to_add = []
        routereader = csv.DictReader(routedata)
        for route in routereader:
            orig = route["orig"]
            dest = route["dest"]
            airline = route["airline"]
            no = route["no"]
            price = route["price"]
            duration = route["duration"]
            distance = route["distance"]
            routes_to_add.append([
                orig,
                dest,
                {"airline": airline, "no": no, "price": price,
                 "duration": duration, "distance": distance}
            ])

        cf.add_many_flight(routes_to_add)
        print("Successfully imported data")


if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    db.drop_database()
    cf = ConnectingFlight(db)
    import_route_csv(cf, "1")
    # data from: https://en.wikipedia.org/wiki/Shortest_path_problem#/media/File:Shortest_path_with_direct_weights.svg
    '''
    cf.add_one_flight("a", "b", price=4, time=1)
    cf.add_many_flight([["a", "b", {"price": 4, "time": 1}],
                        ["a", "c", {"price": 2, "time": 2}],
                        ["b", "c", {"price": 5, "time": 3}],
                        ["b", "d", {"price": 10, "time": 3}],
                        ["c", "e", {"price": 3, "time": 3}],
                        ["e", "d", {"price": 4, "time": 3}],
                        ["d", "f", {"price": 11, "time": 3}]])
    
    # cf.print_floyd_warshal(Database.Criterion.price)
    '''

    def menu():
        print("Welcome, choose an option (Enter 'q' to quit) : \n 1. Add Airport \n 2. Add  flight \n 3. Find shortest path")
        price = db.Criterion.price
        duration = db.Criterion.duration
        distance = db.Criterion.distance
        option = input()
        loop = True
        while loop is True:
            if option == "1":
                airport_add = input("Enter an airport: ")
                db.add_airport(airport_add)
                loop = False
                menu()
            elif option == "2":

                airline = input("Enter airline (IATA): ")
                no = input("Enter flight number: ")
                origin_add = input("Enter an origin airport: ")
                dest_add = input("Enter a destination airport: ")
                price = input("Enter price: ")
                duration = input("Enter duration: ")
                distance = input("Enter distance: ")
                cf.add_one_flight(origin_add, dest_add,
                                  **{"price": price,
                                   "duration": duration,
                                   "distance": distance,
                                   "airline": airline,
                                   "no": no})
                loop = False
                menu()
            elif option == "3":
                origin_shortest = input("Enter an origin airport: ")
                dest_shortest = input("Enter a destination airport: ")
                print("Choose criterion:")
                for c in Database.Criterion:
                    print("{}. {}".format(c.value, c.name))
                crit = input()

                try:
                    cf.get_shortest_floyd_warshal(crit, origin_shortest, dest_shortest)
                except ValueError:
                    print("Invalid choice")
                    break

                print(short)
                loop = False
                menu()
            elif option == "q":
                break
            else:
                break
    menu()