# Connecting Flights
Application to finding shortest "path" of connecting flights through Floyd-Warshall algorithm.

Presentation slides of the project can be found [here](https://docs.google.com/presentation/d/1rhBlG6i2Wh3xkYLhf-2lLqaB5DSqNwVw8vrsuk5ShGk/edit?usp=sharing)
## Dependencies
Python version 3.7 is used.

Modules:
* pymongo
* flask
* flask-wtf
* wtforms

Make sure you have a __MongoDB running on `localhost:27017`__
## Running the program
#### To run console interface
Run `python launch_console_interface.py` in directory

#### To run web interface
Run `python start_webapp.py` and go to `localhost:5000` on your browser. _Note:_ data have to be imported or added using the console interface.
<br/>
#### To use csv
Sample data is provided in the `resources` directory 
Data from [US Bureau of Transportation](https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236) can be imported to the program using the console interface. Make sure to check the fields `Reporting_Airline`, `Flight_Number_Reporting_Airline`, `Origin`, `Dest`, `CRSElapsedTime`, and `Distance` when downloading CSV.

_Highly recommend_ to scale down the data to only include routes connecting major airport by using the script provided: `python ./shortest/scale_down_csv.py`

