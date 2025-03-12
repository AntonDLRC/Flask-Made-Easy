# Every software or app need a database to store data.

from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

#Initialise App (Prepare the program to start working)
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#This query_db function combines getting the cursor, executing and fetching the results

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


#These are the routes for the app
#Each time there is new routes we need to write a query to get the data from the database

@app.route("/")
def home():
    #home page - just id, name, model, speed, and price
    #Use """ to write a multi-line string"
    sql = """SELECT Bikes.BikeID, Makers.Name, Bikes.Model, Bikes.TopSpeed, Bikes.Cost FROM Bikes
             JOIN Makers ON Makers.MakerID = Bikes.MakerID;"""
    results = query_db(sql)
    return str(results)

@app.route('/bike/<int:id>')
def bike(id):
    #just one bike based on id
    sql = "SELECT * FROM Bikes WHERE BikeID = ?;"
    result = query_db(sql, (id,), True)
    return str(result)


if __name__ == "__main__":
    app.run(debug=True)