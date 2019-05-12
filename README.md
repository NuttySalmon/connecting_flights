# Connecting Flights

Application to find lowest price, shortest distance, or duration of connecting flights through [Floyd-Warshall algorithm](http://www-math.mit.edu/~rothvoss/18.304.1PM/Presentations/1-Chandler-18.304lecture1.pdf). 
Presentation slides of the project can be found [here](https://docs.google.com/presentation/d/1rhBlG6i2Wh3xkYLhf-2lLqaB5DSqNwVw8vrsuk5ShGk/edit?usp=sharing).
<br /> The documentation of the project can be found [here](https://docs.google.com/document/d/1tE2CqcxogBARtdbCOhyfkIuOBmGlZkC9BPJquxmPqso/edit). 

![alt text](./screenshot.jpg "screenshot")


## Dependencies
Python version 3.7 is used.

Modules:
*  pymongo (3.8.0 or higher)
*  flask (0.14.2 or higher)
*  flask-wtf (0.14.2 or higher)
*  wtforms
*  pytest

__Install with pip:__ cd to project directory and run `pip install -r requirements.txt`

__Install with pipenv:__ cd to project directory and run `pipenv install`

## Running the program
Before running, make sure you have a __MongoDB v4 running__ on `localhost:27017` and all the dependencies installed.

__To run console interface:__
Run `python start.py` in directory

__To run web interface:__
Run `python run_webapp.py` and go to `localhost:5000` on your browser. _Note:_ no data will be shown before data are added or imported using the console interface.

## Importing CSV
Sample data `import_ready.csv` can be found in the `resources` directory and can be imported through the program's console interface `Use CSV` option.

`import_ready.csv` is a scaled down version of [US Bureau of Transportation](https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236)'s data `raw_data.csv`, processed using the script `scale_down_csv.py` we created. `raw_data.csv` is not recommended to be imported since the data size is too big and with no price information avaliable.

Sample quaries to try to get more than one flight in shortest-path:

*  SEA to ATL, price
*  SFO to MIA, price
*  SFO to ATL, distance, price

### More sample data
[US Bureau of Transportation Statistics's Reporting Carrier On-Time Performance data](https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236) can be downloaded as CSV to be used with the program. Check the fields `Reporting_Airline`, `Flight_Number_Reporting_Airline`, `Origin`, `Dest`, `CRSElapsedTime`, and `Distance` when downloading CSV. __The downloaded CSV is NOT ideally ready to be imported__ and manipulation to the data is required. 


__To make the raw data ready for import__, 
run `python ./shortest/scale_down_csv.py` to scale down the raw data and to add random price information. You can also do it manually by deleteing rows of data and populating a new `price` column in the CSV.
