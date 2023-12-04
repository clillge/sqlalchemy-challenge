# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement

station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

# Start at the homepage.
@app.route("/")
def homepage():
    return(
    #List all the available routes.
        f"Welcome to the Flask Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#################################################
# Flask Routes
#################################################

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():

    #Convert the query results from your precipitation analysis
    #(i.e. retrieve only the last 12 months of data) to a dictionary 
    #using date as the key and prcp as the value.
    end_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    date = date.date()
    
    start_date = date - dt.timedelta(days=365)

    final_year_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= start_date)

    dictionary = []
    for date,prcp in final_year_data:
        interim_dict = {}
        interim_dict[date] = prcp
        dictionary.append(interim_dict)


    #Return the JSON representation of your dictionary.
    return jsonify(dictionary)



#Stations
@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(measurement.station).distinct().all()

    #Return a JSON list of stations from the dataset.
    return jsonify(stations)


#TOBS
@app.route("/api/v1.0/tobs")
def tobs():

    #Query the dates and temperature observations of the 
    #most-active station for the previous year of data.

    #Return a JSON list of temperature observations for the previous year.


#Min/Max/Avg


session.close()