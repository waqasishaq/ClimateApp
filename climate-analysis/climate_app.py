#import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session from Python to the DB
session = Session(engine)

#Flask Setup
app = Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br>"
        
        f"/api/v1.0/precipitation - List of precipitation totals from last year"
        f"<br>"
        
        f"/api/v1.0/stations - List of stations from dataset"
        f"<br>"
        
        f"/api/v1.0/tobs - List of temperature observations from previous year"
        f"<br>"
        
        f"/api/v1.0/start - Given a start date, calculates the min/max/avg temperature for all dates\
        greater than or equal to the start date"
        f"<br>"

        f"/api/v1.0/start/end - Given a start and end date, calculates the min/max/avg temperature\
        for dates between the start and end date inclusive"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    starting_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date>starting_date).\
                order_by(Measurement.date).all()

    precipitation_list = []
    for result in precipitation_data:
        p_dict = {"date": [], "prcp": []}
        p_dict["date"] = result[0]
        p_dict["prcp"] = result[1]
        precipitation_list.append(p_dict)
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations_list = []
    for result in stations_query:
        stations_list.append(result)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    starting_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date>starting_date).\
                order_by(Measurement.date).all()
    tobs_list = []
    for result in tobs_data:
        tobs_list.append(result)
    return jsonify(tobs_list)

@app.route("/api/v1.0/start")
def start():
    def calc_temps_start(start_date):
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    start_example = dt.date(2016, 3, 1)
    temp_data = calc_temps_start(start_example)
    return jsonify(temp_data)

@app.route("/api/v1.0/start/end")
def start_end():
    def calc_temps(starting_date, ending_date):
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= starting_date).filter(Measurement.date <=ending_date).all()
    starting_ex = dt.date(2016, 3, 1)
    ending_ex = dt.date(2016, 3, 9)
    temp_dataa = calc_temps(starting_ex, ending_ex)
    return jsonify(temp_dataa)

if __name__ == "__main__":
	app.run(debug = True)




