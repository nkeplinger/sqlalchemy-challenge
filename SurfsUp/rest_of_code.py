app = Flask(__name__)


@app.route("/")
def home():
    """List all available api routes to Hawaii Climate Data."""
    return (
        f"Hawaii Climate Data:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/station"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/tobs"
    )

    )
@app.route("/api/v1.0/precipitaiton")
def precipitaiton():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns json with the date as the key and the value as the precipitation FOR LAST YEAR"""
    #define date threshold for query
    last_twelve_months = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    #perform Query
    twelve_month_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_twelve_months).all()
    
    #close session
    session.close()
    
    #make it JSON-ified
    return jsonify(twelve_month_data)

@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns jsonified data of all of the stations in the database"""
    #perform Query
    stations = session.query(stations.station, stations.name).all()

    #Close session  
    session.close()

    #make it JSON-ified
    return jsonify(stations)
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns jsonified data for the most active station (USC00519281) FOR LAST YEAR"""
    #define station and date threshold for query:
    most_active = 'USC00519281'
    last_twelve_months = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    #perform Query:
    twelve_month_temp_data = session.query(measurement.station, measurement.date, measurement.tobs).filter(measurement.date >= last_twelve_months, measurement.station == most_active).all()
    
    #Close session   
    session.close()

    #make it JSON-ified:
    return jsonify(twelve_month_temp_data)

    

if __name__ == '__main__':
    app.run(debug=True)