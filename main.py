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
    print("Welcome, Choose an option: \n 1. Add Airport \n 2. Find shortest path")
    option = input()
    if option == "1":
        origin_add = input("Enter an origin airport: ")
        dest_add = input("Enter a destination airport: ")
        cf.add_one_flight(origin_add, dest_add)
    if option == "2":
        origin_shortest = input("Enter an origin airport: ")
        dest_shortest = input("Enter a destination airport: ")
        crit = input("Enter criterion: ")
        cf.get_shortest_floyd_warshal(crit, origin_shortest, dest_shortest)
