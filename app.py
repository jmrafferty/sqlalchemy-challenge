import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
postgresStr = "postgresql://postgres:password@localhost:5432/Hawaii"
engine = create_engine(postgresStr)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation by date"""
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into dictionary
    
    all_precipitation = []
    
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station, Station.name).all()

    session.close()

    all_stations = []

    for station, name in results:
        station_dict = {}
        station_dict[name]= station
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

   

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).all()

    session.close()

    temp_obs = []
    # Create a dictionary from the row data and append to a list of all_passengers
    
    for date, tobs, station in results:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["Date"] = date
        temp_dict["Temp"] = tobs
        temp_obs.append(temp_dict)

    return jsonify(temp_obs)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    start_temps = []
    for date, tobs, station in results:
        startTemp_dict = {}
        startTemp_dict["Min Temp"] = TMIN
        startTemp_dict["Max Temp"] = TMAX
        startTemp_dict["Average Temp"] = TAVG
        start_temps.append(startTemp_dict)

    return jsonify(start_temps)

@app.route("/api/v1.0/start/end")
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    def calc_temps(start_date, end_date):
        """TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        """


    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    end_temps = []
    for date, tobs, station in results:
        endTemp_dict = {}
        endTemp_dict[""] = date
        endTemp_dict[""] = tobs
        endTemp_dict[""] = station
        end_temps.append(endTemp_dict)

    return jsonify(end_temps)


if __name__ == '__main__':
    app.run(debug=True)
