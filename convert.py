import csv
import random

COST_FACTOR = 3.75
#CUTDOWN_INDEX = 50000

def convert(in_name, out_name, top_airports, top_airlines, cutdown):
    data = {}
    with open(in_name, 'r') as routedata:
        routereader = csv.DictReader(routedata)
        for row in routereader:
            orig = row["ORIGIN"]
            dest = row["DEST"]
            if orig not in top_airports or dest not in top_airports:
                # x = random.randint(0, cutdown)
                # if x != 0:
                continue

            airline = row["OP_UNIQUE_CARRIER"]
            # if airline not in top_airlines:
            #     continue
            no = row["OP_CARRIER_FL_NUM"]
            duration = int(float(row["CRS_ELAPSED_TIME"]))
            distance = int(float(row["DISTANCE"]))
            price = round(price_cal(distance), 2)  # calculate sample price
            flightinfo = [airline, no, orig, dest, duration, distance, price]


            if (airline, no) not in data:  # ignore duplication
                data[(airline, no)] = flightinfo
        routedata.close()

    with open(out_name, 'w') as outputcsv:
        csvwriter = csv.writer(outputcsv)
        csvwriter.writerow(["airline", "no", "orig", "dest", "duration",
                            "distance", "price"])
        flights = list(data.values())
        count = 0
        for i in range(0, len(flights), cutdown):
            csvwriter.writerow(flights[i])
            count += 1
        outputcsv.close()
    print("Successfully converted data at {}. Size: {}".format(out_name, count))


def price_cal(distance):
    return distance/COST_FACTOR * random.randint(5, 30)/10


if __name__ == '__main__':
    top_airports = []
    top_airlines = []
    with open("top.csv", 'r') as top:
        topreader = csv.reader(top)
        top_airports = next(topreader)  # read first row
        top_airlines = next(topreader)

    in_file = input("Input file name: ")
    cut = input("Cut down factor: ")
    convert(in_file, cut, top_airports, top_airlines, int(cut))

