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
    date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
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
    end_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
    start_date = date - dt.timedelta(days=365)

    final_year_station_data = session.query(measurement.date, measurement.tobs)\
    .filter(measurement.date >= start_date).filter(measurement.station == 'USC00519281')\
    .all()

    #Return a JSON list of temperature observations for the previous year.
    dictionary = []
    for date,tobs in final_year_station_data:
        interim_dict = {}
        interim_dict[date] = tobs
        dictionary.append(interim_dict)

    return jsonify(dictionary)

#Min/Max/Avg

# Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start or start-end range.

@app.route('/api/v1.0/<start>')
def start(start_date):
# For a specified start, calculate TMIN, TAVG, and TMAX for 
# all the dates greater than or equal to the start date.

    first_date = session.query(measurement.date).order_by(measurement.date.asc()).first()[0]
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]

    if start_date >= first_date and start_date <= last_date:

        return session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()


@app.route('/api/v1.0/<start>/<end>')
def start_end(start_date, end_date):

# For a specified start date and end date, calculate TMIN, TAVG, 
# and TMAX for the dates from the start date to the end date, inclusive.

    first_date = session.query(measurement.date).order_by(measurement.date.asc()).first()[0]
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]

    if start_date >= first_date and end_date <= last_date:

        return session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()


if __name__ == "__main__":
    app.run(debug=True)
