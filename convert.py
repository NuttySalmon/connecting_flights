import csv


def convert(in_name, out_name):
    data = {}
    with open(in_name, 'r') as routedata:
        routereader = csv.DictReader(routedata)
        for row in routereader:
            airline = row["OP_UNIQUE_CARRIER"]
            no = row["OP_CARRIER_FL_NUM"]
            orig = row["ORIGIN"]
            dest = row["DEST"]
            time = int(float(row["CRS_ELAPSED_TIME"]))
            dist = int(float(row["DISTANCE"]))
            flightinfo = [airline, no, orig, dest, time, dist]
            if (airline, no) not in data:
                data[(airline, no)] = flightinfo
    
    with open(out_name, 'w') as outputcsv:
        csvwriter = csv.writer(outputcsv)
        for flight in data.values():
            csvwriter.writerow(flight)

    print("Converted data at: {}".format(out_name))


if __name__ == '__main__':
    in_file = input("Input file name: ")
    out_file = input("Output file name: ")
    convert(in_file, out_file)
