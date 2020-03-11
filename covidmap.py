import os
import json
import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from collecter import csvtojson

# CONFIG #

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covidmap.db'

db = SQLAlchemy(app)

# MODELS #

class Node(db.Model):
    """A single datapoint (usually a countries data)"""

    __tablename__ = "nodes"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String())
    confirmed = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    deceased = db.Column(db.Integer)
    created = db.Column(db.String())

    def __init__(self, country_name: str, items: dict):
        self.country_name = country_name
        self.confirmed = items["ConfirmedCases"]
        self.recovered = items["Recovered"]
        self.deceased = items["Deaths"]
        self.created = datetime.datetime.utcnow()

# ROUTES #

@app.route("/")
def index():
    return render_template("index.html", nodes=Node.query.all())

# UTILS #

def populate_db():
    """Top-level function for getting all csv data from github"""

    print("Populating database..")

    if os.path.exists("covidmap.db"):
        print("Database is already populated!")
        return

    db.create_all()
    csv_data = json.loads(csvtojson())

    for country_name in csv_data:
        new_node = Node(country_name, csv_data[country_name])
        
        db.session.add(new_node)
        db.session.commit()


if __name__ == "__main__":
    populate_db()
    app.run(debug=True)
