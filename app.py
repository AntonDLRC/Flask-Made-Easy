# Every software or app need a database to store data.

from flask import Flask, g, render_template
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

#This query_db function combines getting the databse, cursor, executing and fetching the results

def query_db(sql, args=(), one=False):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results
    


#These are the routes for the app
#Each time there is new routes we need to write a query to get the data from the database

@app.route("/")
def home():
    #home page - just id, name, model, speed, price, and image
    #Use """ to write a multi-line string"
    sql = """SELECT Bikes.BikeID, Makers.Name, Bikes.Model, Bikes.TopSpeed, Bikes.Cost, Bikes.ImageURL FROM Bikes
             JOIN Makers ON Makers.MakerID = Bikes.MakerID;"""
    #quert_db function is used to let us query the database, using a string 
    results = query_db(sql)
    return render_template("home.html", results = results)

@app.route('/bike/<int:id>')
def bike(id):
    #just one bike based on id
    sql = "SELECT * FROM Bikes JOIN Makers ON Makers.MakerID = Bikes.MakerID WHERE BikeID = ?;"
    result = query_db(sql, args=(id,), one=True)
    return render_template("bike.html", bike = result)


if __name__ == "__main__":
    app.run(debug=True)

helohelohelohelohelo