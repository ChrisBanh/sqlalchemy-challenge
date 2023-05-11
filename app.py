import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
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
    return (
        f"Welcome to the Challenge API!<br/>"
        f"Available Routes:<br/>"
        f"Precipitation data for the past year: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f"All active weather stations<a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"Temperature observations for the most active station, USC00519281, from the past 12 months:<a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"The Minimum, Maximum and Average Temperatures for a date range: /api/v1.0/range/yyyy-mm-dd/yyyy-mm-dd<br>"
        f"/Note:be sure to use date format YYYY-MM-DD for start and end. If no end date was provided, it will automatically default to 23/08/2017"   
    )
        
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = { date: prcp for date,prcp in session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "2016-08-23").all() }
    
    session.close()
    return jsonify(results)
    

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = { id: name for id,name in session.query(Station.station, Station.name).all()}
    
    session.close()
    return jsonify(results)
    

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = { date: temp for date,temp in session.query(Measurement.date, Measurement.tobs).filter((Measurement.date>="2016-08-23") & (Measurement.station == 'USC00519281')).all()}
    
    session.close()
    
    return jsonify(results)
    


@app.route("/api/v1.0/range/<start>/")
def start(start, end ='2017-08-23'):
    sel = [ func.avg(Measurement.tobs), 
            func.min(Measurement.tobs), 
            func.max(Measurement.tobs)] 
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    results = session.query(*sel).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
     
    results_list = []
    
    for min, avg, max in results:
        ranged_data = {}
        ranged_data["TMIN"] = min
        ranged_data["TAVG"] = avg
        ranged_data["TMAX"] = max
        results_list.append(ranged_data)
  
    session.close() 
    return jsonify(results_list) 



    

@app.route("/api/v1.0/range/<start>/<end>/")
def starttoend(start, end ='2017-08-23'):
    sel = [ func.avg(Measurement.tobs), 
            func.min(Measurement.tobs), 
            func.max(Measurement.tobs)] 
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    
    results_list = []
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    
    for min, avg, max in results:
        ranged_data = {}
        ranged_data["TMIN"] = min
        ranged_data["TAVG"] = avg
        ranged_data["TMAX"] = max
        results_list.append(ranged_data)
    
    session.close() 
    return jsonify(results_list) 
    
if __name__ == '__main__':
    app.run(debug=True)
