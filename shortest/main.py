from . import Database, ConnectingFlights
from os import system, name
import csv

def import_route_csv(cf, filename):
    """Use data in given csv file"""
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

        cf.add_many_flights(routes_to_add)
        print("Successfully imported data")
        routedata.close()


def clear():
    '''Clear screen'''
    if name == 'nt':  # for windows
        _ = system('cls')
    else:  # for unix
        _ = system('clear')


def menu(db, cf):
    """Run console ui"""
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
            print("\nCount: {}".format(len(all_airports)))
            input("\nPress enter to continue")
            continue

        elif option == "3":

            airline = input("Enter airline (IATA): ")
            no = input("Enter flight number: ")
            origin_add = input("Enter an origin airport: ")
            dest_add = input("Enter a destination airport: ")
            price = input("Enter price: $")
            duration = input("Enter duration (minutes): ")
            distance = input("Enter distance (miles): ")
            cf.add_one_flight(origin_add.upper(), dest_add.upper(),
                              **{"price": float(price),
                                 "duration": int(round(duration)),
                                 "distance": int(round(distance)),
                                 "airline": airline.upper(),
                                 "no": no})
            continue

        elif option == "4":
            origin_shortest = input("Enter an origin airport: ").upper()
            dest_shortest = input("Enter a destination airport: ").upper()
            print("Choose criterion:")
            for c in Database.Criterion:  # list all avaliable weight criteria
                print("{}. {}".format(c.value, c.name))
            crit_no = input("Choice: ")
            crit = Database.Criterion(int(crit_no))
            try:

                short = cf.get_shortest_floyd_warshal(crit, origin_shortest,
                                                      dest_shortest)

                flights = short["path"]
                clear()
                if len(flights) == 0:
                    print("No data")
                else:
                    total = cf.get_str_from_cri(crit, short["total_weight"])
                    print("Total weight: {}".format(total))
                    for step, flight in enumerate(flights):
                        weight = cf.get_str_from_cri(crit, flight[2])
                        orig, dest, info = flight[0], flight[1], flight[3]
                        airline, no = info
                        print("{}. {}-{}  {} {}  {}"
                              .format(step+1, orig, dest, airline, no, weight))

            except ValueError:
                print("Invalid choice")
                continue

            #print(short)
            input("\nPress enter to continue")
            continue

        elif option == "q":
            break


if __name__ == '__main__':
    db = Database('localhost', 27017, "connecting_flight")
    cf = ConnectingFlights(db)
    menu(db, cf)
    clear()