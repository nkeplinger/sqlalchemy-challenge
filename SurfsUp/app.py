import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the tables
measurement = Base.classes.measurement
station = Base.classes.station

# Create session from Python to the DB
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    """List all available api routes to Hawaii Climate Data."""
    return (
        f"<p>Click on info you would like to learn about Hawaii Climate Data:<p>"
        f"/api/v1.0/precipitation<br/>"

        f"/api/v1.0/station<br/>"

        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitaiton():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns json with the date as the key and the value as the precipitation FOR LAST YEAR"""
    #define date threshold for query
    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    last_twelve_months = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    #perform Query
    twelve_month_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_twelve_months).all()
    
    
    # Convert list of tuples into normal list
    results = list(np.ravel(twelve_month_data))
    #make it JSON-ified
    return results

    #return jsonify(twelve_month_data)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns jsonified data of all of the stations in the database"""
    #perform Query
    stationss = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    # Convert list of tuples into normal list
    results_station = list(np.ravel(stationss))

    #make it JSON-ified
    return jsonify(results_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns jsonified data for the most active station (USC00519281) FOR LAST YEAR"""
    #define station and date threshold for query:
    most_active = 'USC00519281'
    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    last_twelve_months = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    #perform Query:
    twelve_month_temp_data = session.query(measurement.station, measurement.date, measurement.tobs).filter(measurement.date >= last_twelve_months, measurement.station == most_active).all()
    
    # Convert list of tuples into normal list
    results_tobs = list(np.ravel(twelve_month_temp_data))
    #make it JSON-ified:
    return jsonify(results_tobs)



if __name__ == '__main__':
    app.run(debug=True)
