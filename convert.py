import csv

def convert():
    
    converted_data = []
    with open("./rawdata/routedata.csv") as routedata:
        routereader = csv.DictReader(routedata)
        for row in routereader:
            airline = row["OP_UNIQUE_CARRIER"]
            no = row["OP_CARRIER_FL_NUM"]
            orig = row["ORIGIN"]
            dest = row["DEST"]
            time = row["CRS_ELAPSED_TIME"]
            dist = row["DISTANCE"]
            converted_data.append({
                "airline": airline,
                "no": no,
                "orig": orig,
                "dest": dest,
                "time": time,
                "dist": dist,
                })
        print(converted_data)


if __name__ == '__main__':
    inFile = input("Input file name:")
    outFile = input("Output file name:")
    convert()

