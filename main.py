from database import Database
from connecting_flights import ConnectingFlight
import tkinter
from tkinter import *
from tkinter.ttk import *

if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlight(db)

    # data from: https://en.wikipedia.org/wiki/Shortest_path_problem#/media/File:Shortest_path_with_direct_weights.svg
    """cf.add_many_flight([["a", "b", {"price": 4, "time": 1}],
                        ["a", "c", {"price": 2, "time": 2}],
                        ["b", "c", {"price": 5, "time": 3}],
                        ["b", "d", {"price": 10, "time": 3}],
                        ["c", "e", {"price": 3, "time": 3}],
                        ["e", "d", {"price": 4, "time": 3}],
                        ["d", "f", {"price": 11, "time": 3}]])
                        """
    # cf.print_floyd_warshal(Database.Criterion.price)

    def menu():
        print("Welcome, choose an option (Enter 'q' to quit) : \n 1. Add Airport \n 2. Add  flight \n 3. Find shortest path")
        price = db.Criterion.price
        time = db.Criterion.time
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
                origin_add = input("Enter an origin airport: ")
                dest_add = input("Enter a destination airport: ")
                price = input("Enter price: ")
                time = input("Enter time: ")
                distance = input("Enter distance: ")
                cf.add_many_flight([[origin_add, dest_add, {"price": price, "time": time, "distance": distance}]])
                loop = False
                menu()
            elif option == "3":
                origin_shortest = input("Enter an origin airport: ")
                dest_shortest = input("Enter a destination airport: ")
                print("Choose criterion: \n 1. Time \n 2. Price \n 3. Distance ")
                crit = input()
                if crit == "1":
                    crit = time
                elif crit == "2":
                    crit = price
                elif crit == "3":
                    crit = distance
                short = cf.get_shortest_floyd_warshal(crit, origin_shortest, dest_shortest)
                print(short)
                loop = False
                menu()
            elif option == "q":
                break
            else:
                break
    menu()