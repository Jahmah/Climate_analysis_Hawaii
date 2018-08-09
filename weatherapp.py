##################################################
# FLASK app for generating Hawaii Weather data
#################################################

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup and connection
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Query and return dates and precipitation values in json from the last year.
#
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of dates and precipitation measurements for the last 12 months """
     # Query all dates and prcp and filter for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list
    precipitation_last12mths = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_last12mths.append(prcp_dict)

    return jsonify(precipitation_last12mths)


# Return a json list of stations from the dataset.
#
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)


# Return a Json list of temperature Observations (tobs) for the previous year
#
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations for the previous year"""
    # Query all tobs
    results = session.query(Measurement.tobs).filter(Measurement.tobs >= '2016-08-23').\
              order_by(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_last12mths = list(np.ravel(results))

    return jsonify(tobs_last12mths)


# Return a Json list of the minimum, average and the max temperatures from a given start date
@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """ Calculate TMIN, TAVG, and TMAX for all dates from start date."""
    # Query tobs for dates starting from
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
              func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    temperatures_start_date = list(np.ravel(results))

    return jsonify(temperatures_start_date)


# Given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates
# between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    """ calculate the TMIN, TAVG,and TMAX from start and to end date inclusive."""
    # Query all tobs and filter for dates given
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)


if __name__ == "__main__":
    app.run(debug=True)
