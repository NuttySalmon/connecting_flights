from database import Database
from connecting_flights import ConnectingFlight
from os import system, name 
#import tkinter
#from tkinter import *
#from tkinter.ttk import *
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
        routedata.close()

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlight(db)
    clear()
    
    while True:
        clear()
        print(
        """
        Welcome, choose an option (Enter 'q' to quit) :
        1. Use CSV
        2. Print all airports
        3. Add flight
        4. Find shortest path
        """)

        option = input("Choice: ")
        clear()
        if option == "1":
            filename = input("File name: ")
            db.drop_database()
            import_route_csv(cf, filename)
            input("\nPress enter to continue")
            continue

        elif option == "2":
            all_airports = db.all_airports_list()
            for airport in all_airports:
                print(airport)

            input("\nPress enter to continue")
            continue

        elif option == "3":

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
            continue

        elif option == "4":
            origin_shortest = input("Enter an origin airport: ")
            dest_shortest = input("Enter a destination airport: ")
            print("Choose criterion:")
            for c in Database.Criterion:
                print("{}. {}".format(c.value, c.name))
            crit_no = input("Choice: ")
            crit = Database.Criterion(int(crit_no))
            try:

                short = cf.get_shortest_floyd_warshal(crit, origin_shortest, dest_shortest)
            except ValueError:
                print("Invalid choice")
                break

            print(short)
            input("\nPress enter to continue")
            continue

        elif option == "q":
            break

